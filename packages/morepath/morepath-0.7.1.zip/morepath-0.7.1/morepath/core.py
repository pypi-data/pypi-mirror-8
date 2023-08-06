from .config import Config
import morepath.directive
from morepath import generic
from .app import App
from .request import Request, Response
from .converter import Converter, IDENTITY_CONVERTER
from webob import Response as BaseResponse
from webob.exc import HTTPException, HTTPForbidden, HTTPMethodNotAllowed
import morepath
from reg import mapply, KeyIndex
from datetime import datetime, date
from time import mktime, strptime


assert morepath.directive  # we need to make the function directive work


def setup():
    """Set up core Morepath framework configuration.

    Returns a :class:`Config` object; you can then :meth:`Config.scan`
    the configuration of other packages you want to load and then
    :meth:`Config.commit` it.

    See also :func:`autoconfig` and :func:`autosetup`.

    :returns: :class:`Config` object.
    """
    config = Config()
    config.scan(morepath, ignore=['.tests'])
    return config


@App.function(generic.consume, Request, App)
def traject_consume(request, app, lookup):
    traject = app.traject
    value, stack, traject_variables = traject.consume(request.unconsumed)
    if value is None:
        return None
    get_obj, get_parameters = value
    variables = get_parameters(request.GET)
    variables['request'] = request
    variables['app'] = app
    variables.update(traject_variables)
    next_obj = mapply(get_obj, **variables)
    if next_obj is None:
        return None
    request.unconsumed = stack
    return next_obj


@App.function(generic.link, Request, object, object)
def link(request, model, mounted):
    result = []
    parameters = {}
    while mounted is not None:
        path_info = generic.path(model, lookup=mounted.lookup)
        if path_info is None:
            return None
        path, params = path_info
        result.append(path)
        parameters.update(params)
        model = mounted
        mounted = mounted.parent
    result.append(request.script_name)
    result.reverse()
    return '/'.join(result).strip('/'), parameters


@App.function(generic.response, Request, object)
def get_response(request, model, predicates=None):
    view = generic.view.component(
        request, model, lookup=request.lookup,
        predicates=predicates,
        default=None)
    if view is None or view.internal:
        return None
    if (view.permission is not None and
        not generic.permits(request.identity, model, view.permission,
                            lookup=request.lookup)):
        raise HTTPForbidden()
    content = view(request, model)
    if isinstance(content, BaseResponse):
        # the view took full control over the response
        return content
    # XXX consider always setting a default render so that view.render
    # can never be None
    if view.render is not None:
        response = view.render(content, request)
    else:
        response = Response(content, content_type='text/plain')
    request.run_after(response)
    return response


@App.function(generic.permits, object, object, object)
def has_permission(identity, model, permission):
    return False


@App.predicate(name='name', index=KeyIndex, order=0,
               default='')
def name_predicate(self, request):
    return request.view_name


@App.predicate(name='request_method', index=KeyIndex, order=1,
               default='GET')
def request_method_predicate(self, request):
    return request.method


@App.predicate_fallback(name='request_method')
def method_not_allowed(self, request):
    raise HTTPMethodNotAllowed()


@App.converter(type=int)
def int_converter():
    return Converter(int)


@App.converter(type=type(u""))
def unicode_converter():
    return IDENTITY_CONVERTER


# Python 2
if type(u"") != type(""): # flake8: noqa
    @App.converter(type=type(""))
    def str_converter():
        # XXX do we want to decode/encode unicode?
        return IDENTITY_CONVERTER


def date_decode(s):
    return date.fromtimestamp(mktime(strptime(s, '%Y%m%d')))


def date_encode(d):
    return d.strftime('%Y%m%d')


@App.converter(type=date)
def date_converter():
    return Converter(date_decode, date_encode)


def datetime_decode(s):
    return datetime.fromtimestamp(mktime(strptime(s, '%Y%m%dT%H%M%S')))


def datetime_encode(d):
    return d.strftime('%Y%m%dT%H%M%S')


@App.converter(type=datetime)
def datetime_converter():
    return Converter(datetime_decode, datetime_encode)


@App.tween_factory()
def excview_tween_factory(app, handler):
    def excview_tween(request):
        try:
            response = handler(request)
        except Exception as exc:
            # override predicates so that they aren't taken from request;
            # default name and GET is correct for exception views.
            response = generic.response(request, exc, lookup=app.lookup,
                                        default=None, predicates={})
            if response is None:
                raise
            return response
        return response
    return excview_tween


@App.view(model=HTTPException)
def standard_exception_view(self, model):
    # webob HTTPException is a response already
    return self
