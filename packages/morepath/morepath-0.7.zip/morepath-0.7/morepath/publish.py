from morepath import generic
from .app import App
from .traject import create_path
from webob.exc import HTTPNotFound


DEFAULT_NAME = u''


class ResponseSentinel(object):
    pass


RESPONSE_SENTINEL = ResponseSentinel()


def resolve_model(request):
    """Resolve path to a model using consumers.
    """
    lookup = request.lookup  # XXX can get this from argument too
    model = request.app
    model.set_implicit()
    while request.unconsumed:
        next_model = generic.consume(request, model, lookup=lookup)
        if next_model is None:
            return model
        model = next_model
        if isinstance(model, App):
            model.set_implicit()
            model.parent = request.app
            request.app = model
            request.lookup = model.lookup
    # if there is nothing (left), we consume toward a root model
    if not request.unconsumed and isinstance(model, App):
        root_model = generic.consume(request, model, lookup=lookup)
        if root_model is not None:
            model = root_model
        # XXX handling mounting? lookups? write test cases
    return model


def resolve_response(request, model):
    request.view_name = get_view_name(request.unconsumed)

    response = generic.response(request, model, default=RESPONSE_SENTINEL,
                                lookup=request.lookup)
    if response is RESPONSE_SENTINEL:
        raise HTTPNotFound()
    return response


def get_view_name(stack):
    unconsumed_amount = len(stack)
    if unconsumed_amount > 1:
        raise HTTPNotFound()
    elif unconsumed_amount == 0:
        return DEFAULT_NAME
    elif unconsumed_amount == 1:
        return stack[0].lstrip('+')
    assert False, ("Unconsumed stack: %s" %
                   create_path(stack))  # pragma: nocoverage


def publish(request):
    model = resolve_model(request)
    return resolve_response(request, model)
