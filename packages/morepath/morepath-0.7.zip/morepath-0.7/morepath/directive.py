from .app import App
from .config import Directive as ConfigDirective
from .settings import register_setting
from .error import ConfigError
from .view import (register_view, render_json, render_html,
                   register_predicate, register_predicate_fallback,
                   get_predicates_with_defaults)
from .security import (register_permission_checker,
                       Identity, NoIdentity)
from .path import register_path
from .traject import Path
from reg import KeyIndex
from .request import Request, Response
from morepath import generic


class Directive(ConfigDirective):
    def __init__(self, app):
        super(Directive, self).__init__(app.registry)
        self.app = app


@App.directive('setting')
class SettingDirective(Directive):
    def __init__(self, app, section, name):
        """Register application setting.

        An application setting is registered under the ``settings``
        attribute of :class:`morepath.app.Registry`. It will
        be executed early in configuration so other configuration
        directives can depend on the settings being there.

        The decorated function returns the setting value when executed.

        :param section: the name of the section the setting should go
          under.
        :param name: the name of the setting in its section.
        """

        super(SettingDirective, self).__init__(app)
        self.section = section
        self.name = name

    def identifier(self, registry):
        return self.section, self.name

    def perform(self, registry, obj):
        register_setting(registry, self.section, self.name, obj)


class SettingValue(object):
    def __init__(self, value):
        self.value = value

    def __call__(self):
        return self.value


@App.directive('setting_section')
class SettingSectionDirective(Directive):
    def __init__(self, app, section):
        """Register application setting in a section.

        An application settings are registered under the ``settings``
        attribute of :class:`morepath.app.Registry`. It will
        be executed early in configuration so other configuration
        directives can depend on the settings being there.

        The decorated function returns a dictionary with as keys the
        setting names and as values the settings.

        :param section: the name of the section the setting should go
          under.
        """

        super(SettingSectionDirective, self).__init__(app)
        self.section = section

    def prepare(self, obj):
        section = obj()
        app = self.app
        for name, value in section.items():
            yield (app.setting(section=self.section, name=name),
                   SettingValue(value))


@App.directive('converter')
class ConverterDirective(Directive):
    depends = [SettingDirective]

    def __init__(self, app, type):
        """Register custom converter for type.

        :param type: the Python type for which to register the
          converter.  Morepath uses converters when converting path
          variables and URL parameters when decoding or encoding
          URLs. Morepath looks up the converter using the
          type. The type is either given explicitly as the value in
          the ``converters`` dictionary in the
          :meth:`morepath.App.path` directive, or is deduced from
          the value of the default argument of the decorated model
          function or class using ``type()``.
        """
        super(ConverterDirective, self).__init__(app)
        self.type = type

    def identifier(self, registry):
        return ('converter', self.type)

    def perform(self, registry, obj):
        registry.register_converter(self.type, obj())


@App.directive('path')
class PathDirective(Directive):
    depends = [SettingDirective, ConverterDirective]

    def __init__(self, app, path, model=None,
                 variables=None, converters=None, required=None,
                 get_converters=None, absorb=False):
        """Register a model for a path.

        Decorate a function or a class (constructor). The function
        should return an instance of the model class, for instance by
        querying it from the database, or ``None`` if the model does
        not exist.

        The decorated function gets as arguments any variables
        specified in the path as well as URL parameters.

        If you declare a ``request`` parameter the function is
        able to use that information too.

        :param path: the route for which the model is registered.
        :param model: the class of the model that the decorated function
          should return. If the directive is used on a class instead of a
          function, the model should not be provided.
        :param variables: a function that given a model object can construct
          the variables used in the path (including any URL parameters).
          If omitted, variables are retrieved from the model by using
          the arguments of the decorated function.
        :param converters: a dictionary containing converters for variables.
          The key is the variable name, the value is a
          :class:`morepath.Converter` instance.
        :param required: list or set of names of those URL parameters which
          should be required, i.e. if missing a 400 Bad Request response is
          given. Any default value is ignored. Has no effect on path
          variables. Optional.
        :param get_converters: a function that returns a converter dictionary.
          This function is called once during configuration time. It can
          be used to programmatically supply converters. It is merged
          with the ``converters`` dictionary, if supplied. Optional.
        :param absorb: If set to ``True``, matches any subpath that
          matches this path as well. This is passed into the decorated
          function as the ``remaining`` variable.
        """
        super(PathDirective, self).__init__(app)
        self.model = model
        self.path = path
        self.variables = variables
        self.converters = converters
        self.required = required
        self.get_converters = get_converters
        self.absorb = absorb

    def identifier(self, registry):
        return ('path', Path(self.path).discriminator())

    def discriminators(self, registry):
        return [('model', self.model)]

    def prepare(self, obj):
        model = self.model
        if isinstance(obj, type):
            if model is not None:
                raise ConfigError(
                    "@path decorates class so cannot "
                    "have explicit model: %s" % model)
            model = obj
        if model is None:
            raise ConfigError(
                "@path does not decorate class and has no explicit model")
        yield self.clone(model=model), obj

    def perform(self, registry, obj):
        register_path(registry, self.model, self.path,
                      self.variables, self.converters, self.required,
                      self.get_converters, self.absorb,
                      obj)


@App.directive('permission_rule')
class PermissionRuleDirective(Directive):
    depends = [SettingDirective]

    def __init__(self, app, model, permission, identity=Identity):
        """Declare whether a model has a permission.

        The decorated function receives ``model``, `permission``
        (instance of any permission object) and ``identity``
        (:class:`morepath.security.Identity`) parameters. The
        decorated function should return ``True`` only if the given
        identity exists and has that permission on the model.

        :param model: the model class
        :param permission: permission class
        :param identity: identity class to check permission for. If ``None``,
          the identity to check for is the special
          :data:`morepath.security.NO_IDENTITY`.
        """
        super(PermissionRuleDirective, self).__init__(app)
        self.model = model
        self.permission = permission
        if identity is None:
            identity = NoIdentity
        self.identity = identity

    def identifier(self, registry):
        return (self.model, self.permission, self.identity)

    def perform(self, registry, obj):
        register_permission_checker(
            registry, self.identity, self.model, self.permission, obj)


@App.directive('predicate')
class PredicateDirective(Directive):
    depends = [SettingDirective]

    def __init__(self, app, name, order, default, index=KeyIndex):
        """Register custom view predicate.

        The decorated function gets ``model`` and ``request`` (a
        :class:`morepath.Request` object) parameters.

        From this information it should calculate a predicate value
        and return it. You can then pass these extra predicate
        arguments to :meth:`morepath.App.view` and this view is
        only found if the predicate matches.

        :param name: the name of the view predicate.
        :param order: when this custom view predicate should be checked
          compared to the others. A lower order means a higher importance.
        :type order: int
        :param default: the default value for this view predicate.
          This is used when the predicate is omitted or ``None`` when
          supplied to the :meth:`morepath.App.view` directive.
          This is also used when using :meth:`Request.view` to render
          a view.
        :param index: the predicate index to use. Default is
          :class:`reg.KeyIndex` which matches by name.

        """
        super(PredicateDirective, self).__init__(app)
        self.name = name
        self.order = order
        self.default = default
        self.index = index

    def identifier(self, registry):
        return self.name

    def perform(self, registry, obj):
        register_predicate(registry, self.name, self.order, self.default,
                           self.index, obj)


@App.directive('predicate_fallback')
class PredicateFallbackDirective(Directive):
    depends = [SettingDirective, PredicateDirective]

    def __init__(self, app, name):
        """For a given predicate name, register fallback view.

        The decorated function gets ``self`` and ``request`` parameters.

        The fallback view is a view that gets called when the
        named predicate does not match and no view has been registered
        that can handle that case.

        :param name: the name of the predicate.
        """
        super(PredicateFallbackDirective, self).__init__(app)
        self.name = name

    def identifier(self, registry):
        return self.name

    def perform(self, registry, obj):
        register_predicate_fallback(registry, self.name, obj)


@App.directive('view')
class ViewDirective(Directive):
    depends = [SettingDirective, PredicateDirective,
               PredicateFallbackDirective]

    def __init__(self, app, model, render=None, permission=None,
                 internal=False,
                 **predicates):
        '''Register a view for a model.

        The decorated function gets ``self`` (model instance) and
        ``request`` (:class:`morepath.Request`) parameters. The
        function should return either a (unicode) string that is
        the response body, or a :class:`morepath.Response` object.

        If a specific ``render`` function is given the output of the
        function is passed to this first, and the function could
        return whatever the ``render`` parameter expects as input.
        This function should take the object to render and the
        request.  func:`morepath.render_json` for instance expects as
        its first argument a Python object such as a dict that can be
        serialized to JSON.

        See also :meth:`morepath.App.json` and
        :meth:`morepath.App.html`.

        :param model: the class of the model for which this view is registered.
          The ``self`` passed into the view function is an instance
          of the model (or of a subclass).
        :param render: an optional function that can render the output of the
          view function to a response, and possibly set headers such as
          ``Content-Type``, etc. This function takes ``self`` and
          ``request`` parameters as input.
        :param permission: a permission class. The model should have this
          permission, otherwise access to this view is forbidden. If omitted,
          the view function is public.
        :param internal: Whether this view is internal only. If
          ``True``, the view is only useful programmatically using
          :meth:`morepath.Request.view`, but will not be published on
          the web. It will be as if the view is not there.
          By default a view is ``False``, so not internal.
        :param name: the name of the view as it appears in the URL. If omitted,
          it is the empty string, meaning the default view for the model.
          This is a predicate.
        :param request_method: the request method to which this view should
          answer, i.e. GET, POST, etc. If omitted, this view responds to
          GET requests only. This is a predicate.
        :param predicates: predicates to match this view on. Use
          :data:`morepath.ANY` for a predicate if you don't care what
          the value is. If you don't specify a predicate, the default
          value is used. Standard predicate values are
          ``name`` and ``request_method``, but you can install your
          own using the :meth:`morepath.App.predicate` directive.

        '''
        super(ViewDirective, self).__init__(app)
        self.model = model
        self.render = render
        self.permission = permission
        self.internal = internal
        self.predicates = predicates

    def clone(self, **kw):
        # XXX standard clone doesn't work due to use of predicates
        # non-immutable in __init__. move this to another phase so
        # that this more complex clone isn't needed?
        args = dict(
            app=self.app,
            model=self.model,
            render=self.render,
            permission=self.permission)
        args.update(self.predicates)
        args.update(kw)
        return ViewDirective(**args)

    def identifier(self, registry):
        predicates = get_predicates_with_defaults(
            self.predicates, registry.exact('predicate_info', ()))
        predicates_discriminator = tuple(sorted(predicates.items()))
        return (self.model, predicates_discriminator)

    def perform(self, registry, obj):
        register_view(registry, self.model, obj, self.render, self.permission,
                      self.internal, self.predicates)


@App.directive('json')
class JsonDirective(ViewDirective):
    def __init__(self, app, model, render=None, permission=None,
                 internal=False, **predicates):
        """Register JSON view.

        This is like :meth:`morepath.App.view`, but with
        :func:`morepath.render_json` as default for the `render`
        function.

        Transforms the view output to JSON and sets the content type to
        ``application/json``.

        :param model: the class of the model for which this view is registered.
        :param name: the name of the view as it appears in the URL. If omitted,
          it is the empty string, meaning the default view for the model.
        :param render: an optional function that can render the output
          of the view function to a response, and possibly set headers
          such as ``Content-Type``, etc. Renders as JSON by
          default. This function takes ``self`` and
          ``request`` parameters as input.
        :param permission: a permission class. The model should have this
          permission, otherwise access to this view is forbidden. If omitted,
          the view function is public.
        :param internal: Whether this view is internal only. If
          ``True``, the view is only useful programmatically using
          :meth:`morepath.Request.view`, but will not be published on
          the web. It will be as if the view is not there.
          By default a view is ``False``, so not internal.
        :param name: the name of the view as it appears in the URL. If omitted,
          it is the empty string, meaning the default view for the model.
          This is a predicate.
        :param request_method: the request method to which this view should
          answer, i.e. GET, POST, etc. If omitted, this view will respond to
          GET requests only. This is a predicate.
        :param predicates: predicates to match this view on. See the
          documentation of :meth:`App.view` for more information.
        """
        render = render or render_json
        super(JsonDirective, self).__init__(app, model, render, permission,
                                            internal, **predicates)

    def group_key(self):
        return ViewDirective


@App.directive('html')
class HtmlDirective(ViewDirective):
    def __init__(self, app, model, render=None, permission=None,
                 internal=False, **predicates):
        """Register HTML view.

        This is like :meth:`morepath.App.view`, but with
        :func:`morepath.render_html` as default for the `render`
        function.

        Sets the content type to ``text/html``.

        :param model: the class of the model for which this view is registered.
        :param name: the name of the view as it appears in the URL. If omitted,
          it is the empty string, meaning the default view for the model.
        :param render: an optional function that can render the output
          of the view function to a response, and possibly set headers
          such as ``Content-Type``, etc. Renders as HTML by
          default. This function takes ``self`` and
          ``request`` parameters as input.
        :param permission: a permission class. The model should have this
          permission, otherwise access to this view is forbidden. If omitted,
          the view function is public.
        :param internal: Whether this view is internal only. If
          ``True``, the view is only useful programmatically using
          :meth:`morepath.Request.view`, but will not be published on
          the web. It will be as if the view is not there.
          By default a view is ``False``, so not internal.
        :param name: the name of the view as it appears in the URL. If omitted,
          it is the empty string, meaning the default view for the model.
          This is a predicate.
        :param request_method: the request method to which this view should
          answer, i.e. GET, POST, etc. If omitted, this view will respond to
          GET requests only. This is a predicate.
        :param predicates: predicates to match this view on. See the
          documentation of :meth:`App.view` for more information.
        """
        render = render or render_html
        super(HtmlDirective, self).__init__(app, model, render, permission,
                                            internal, **predicates)

    def group_key(self):
        return ViewDirective


@App.directive('mount')
class MountDirective(PathDirective):
    depends = [SettingDirective, ConverterDirective]

    def __init__(self, base_app, path, app, variables=None, converters=None,
                 required=None, get_converters=None, name=None):
        """Mount sub application on path.

        The decorated function gets the variables specified in path as
        parameters. It should return a new instance of an application
        class.

        :param path: the path to mount the application on.
        :param app: the :class:`morepath.App` subclass to mount.
        :param variables: a function that given an app instance can construct
          the variables used in the path (including any URL parameters).
          If omitted, variables are retrieved from the app by using
          the arguments of the decorated function.
        :param converters: converters as for the
          :meth:`morepath.App.path` directive.
        :param required: list or set of names of those URL parameters which
          should be required, i.e. if missing a 400 Bad Request response is
          given. Any default value is ignored. Has no effect on path
          variables. Optional.
        :param get_converters: a function that returns a converter dictionary.
          This function is called once during configuration time. It can
          be used to programmatically supply converters. It is merged
          with the ``converters`` dictionary, if supplied. Optional.
        :param name: name of the mount. This name can be used with
          :meth:`Request.child` to allow loose coupling between mounting
          application and mounted application. Optional, and if not supplied
          the ``path`` argument is taken as the name.

        """
        super(MountDirective, self).__init__(base_app, path,
                                             variables=variables,
                                             converters=converters,
                                             required=required,
                                             get_converters=get_converters)
        self.name = name or path
        self.mounted_app = app

    def group_key(self):
        return PathDirective

    # XXX it's a bit of a hack to make the mount directive
    # group with the path directive so we get conflicts,
    # we need to override prepare to shut it up again
    def prepare(self, obj):
        yield self.clone(), obj

    def discriminators(self, app):
        return [('mount', self.mounted_app)]

    def perform(self, registry, obj):
        registry.register_mount(
            self.mounted_app, self.path, self.variables,
            self.converters, self.required,
            self.get_converters, self.name, obj)


@App.directive('defer_links')
class DeferLinksDirective(Directive):

    depends = [SettingDirective, MountDirective]

    def __init__(self, base_app, model):
        """Defer link generation for model to mounted app.

        With ``defer_links`` you can specify that link generation for
        instances of ``model`` is to be handled by a returned mounted
        app it cannot be handled by the given app
        itself. :meth:`Request.link` and :meth:`Request.view` are
        affected by this directive.

        The decorated function gets an instance of the application and
        object to link to. It should return another application that
        it knows can create links for this object. The function uses
        navigation methods on :class:`App` to do so like
        :meth:`App.parent` and :meth:`App.child`.

        :param model: the class for which we want to defer linking.
        """
        super(DeferLinksDirective, self).__init__(base_app)
        self.model = model

    def group_key(self):
        return PathDirective

    def identifier(self, registry):
        return ('defer_links', self.model)

    def discriminators(self, registry):
        return [('model', self.model)]

    def perform(self, registry, obj):
        registry.register_defer_links(self.model, obj)


tween_factory_id = 0


@App.directive('tween_factory')
class TweenFactoryDirective(Directive):
    depends = [SettingDirective]

    def __init__(self, app, under=None, over=None, name=None):
        '''Register tween factory.

        The tween system allows the creation of lightweight middleware
        for Morepath that is aware of the request and the application.

        The decorated function is a tween factory. It should return a tween.
        It gets two arguments: the app for which this tween is in use,
        and another tween that this tween can wrap.

        A tween is a function that takes a request and a mounted
        application as arguments.

        Tween factories can be set to be over or under each other to
        control the order in which the produced tweens are wrapped.

        :param under: This tween factory produces a tween that wants to
          be wrapped by the tween produced by the ``under`` tween factory.
          Optional.
        :param over: This tween factory produces a tween that wants to
          wrap the tween produced by the over ``tween`` factory. Optional.
        :param name: The name under which to register this tween factory,
          so that it can be overridden by applications that extend this one.
          If no name is supplied a default name is generated.
        '''
        super(TweenFactoryDirective, self).__init__(app)
        global tween_factory_id
        self.under = under
        self.over = over
        if name is None:
            name = u'tween_factory_%s' % tween_factory_id
            tween_factory_id += 1
        self.name = name

    def identifier(self, registry):
        return self.name

    def perform(self, registry, obj):
        registry.register_tween_factory(obj, over=self.over, under=self.under)


@App.directive('identity_policy')
class IdentityPolicyDirective(Directive):
    depends = [SettingDirective]

    def __init__(self, app):
        '''Register identity policy.

        The decorated function should return an instance of an
        identity policy, which should have ``identify``, ``remember``
        and ``forget`` methods.
        '''
        super(IdentityPolicyDirective, self).__init__(app)

    def prepare(self, obj):
        policy = obj()
        app = self.app
        yield app.function(
            generic.identify, Request), policy.identify
        yield (app.function(
            generic.remember_identity, Response, Request, object),
            policy.remember)
        yield app.function(
            generic.forget_identity, Response, Request), policy.forget


@App.directive('verify_identity')
class VerifyIdentityDirective(Directive):
    def __init__(self, app, identity=object):
        '''Verify claimed identity.

        The decorated function gives a single ``identity`` argument which
        contains the claimed identity. It should return ``True`` only if the
        identity can be verified with the system.

        This is particularly useful with identity policies such as
        basic authentication and cookie-based authentication where the
        identity information (username/password) is repeatedly sent to
        the the server and needs to be verified.

        For some identity policies (auth tkt, session) this can always
        return ``True`` as the act of establishing the identity means
        the identity is verified.

        The default behavior is to always return ``False``.

        :param identity: identity class to verify. Optional.
        '''
        super(VerifyIdentityDirective, self).__init__(app)
        self.identity = identity

    def prepare(self, obj):
        yield self.app.function(
            generic.verify_identity, self.identity), obj


@App.directive('function')
class FunctionDirective(Directive):
    depends = [SettingDirective]

    def __init__(self, app, target, *sources):
        '''Register function as implementation of generic function

        The decorated function is an implementation of the generic
        function supplied to the decorator. This way you can override
        parts of the Morepath framework, or create new hookable
        functions of your own. This is a layer over
        :meth:`reg.IRegistry.register`.

        The ``target`` argument is a generic function, so a Python
        function marked with either :func:`reg.generic` or
        with :func:`reg.classgeneric`.

        :param target: the generic function to register an implementation for.
        :type target: function object
        :param sources: classes of parameters to register for.

        '''
        super(FunctionDirective, self).__init__(app)
        self.target = target
        self.sources = tuple(sources)

    def identifier(self, registry):
        return (self.target, self.sources)

    def perform(self, registry, obj):
        registry.register(self.target, self.sources, obj)


@App.directive('dump_json')
class DumpJsonDirective(Directive):
    def __init__(self, app, model=object):
        '''Register a function that converts model to JSON.

        The decorated function gets ``self`` (model instance) and
        ``request`` (:class:`morepath.Request`) parameters. The
        function should return an JSON object. That is, a Python
        object that can be dumped to a JSON string using
        ``json.dump``.

        :param model: the class of the model for which this function is
          registered. The ``self`` passed into the function is an instance
          of the model (or of a subclass). By default the model is ``object``,
          meaning we register a function for all model classes.
        '''
        super(DumpJsonDirective, self).__init__(app)
        self.model = model

    def identifier(self, registry):
        return self.model

    def perform(self, registry, obj):
        # reverse parameters
        def dump(request, self):
            return obj(self, request)
        registry.register(generic.dump_json, (Request, self.model), dump)


@App.directive('load_json')
class LoadJsonDirective(Directive):
    def __init__(self, app):
        '''Register a function that converts JSON to an object.

        The decorated function gets ``json`` and ``request``
        (:class:`morepath.Request`) parameters. The function should
        return a Python object based on the given JSON.
        '''
        super(LoadJsonDirective, self).__init__(app)

    def identifier(self, registry):
        return ()

    def perform(self, registry, obj):
        # reverse parameters
        def load(request, json):
            return obj(json, request)
        registry.register(generic.load_json, (Request, object), load)
