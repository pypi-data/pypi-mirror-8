import copy
import types
import numbers

import cherrypy

from .authentication import is_authenticated
from .utils import redirect
from ._constants import (
    AUTH_CLAIMS,
    AUTH_REQUIRED,
    DEFAULT_LOGIN_PAGE,
    REQUEST_USER,
    USER_SESSION_KEY,
    AUTHORIZER,
    LOGIN_PAGE,
    UNAUTHORIZED_REDIRECT,
)

_auth_required_cache = {}


try:  # Python 2
    from types import ClassType as classtype
except ImportError:  # Python 3
    classtype = type


def authorize(*args):
    """
    Decorator for marking the controller or action to require authentication and setting the authorization requirements
    """

    def authorize_(target=None, claims=None):
        if not claims:
            claims = {}

        def closure(t):
            t._auth_required = True
            t._auth_claims = claims
            return t

        if target is None:
            return closure
        else:
            return closure(target)

    def allow(t):
        t._auth_required = False
        if hasattr(t, '_auth_claims'):
            delattr(t, '_auth_claims')
        return t

    target = args[0] if len(args) > 0 else None

    # @authorize
    # classtype is `types.ClassType` in Python2 and `type` in Python3
    if isinstance(target, (classtype, types.FunctionType, types.MethodType)):
        return authorize_(target)
    # @authorize({'action': 'object'}) OR @authorize({'action': ('object1', 'object2')})
    elif isinstance(target, dict):
        return authorize_(claims=target)
    # @authorize()
    elif target is None:
        return authorize_()
    # @authorize(False)  # allow anonymous access
    elif target is False:
        return allow


def _get_hierarchy(handler, hierarchy):
    """
    Returns the hierarchy of the given handler in the application tree

    :param handler: The handler to look for
    :param hierarchy: The current branch in the application tree beeing examined
    :type hierarchy: list
    :return: A list with the hierarchy up to the given handler
    :rtype: list
    """
    root = hierarchy[-1]

    ftypes = (types.MethodType, types.FunctionType)
    ntypes = ftypes + (numbers.Number, str, bool, list, set, tuple, dict)

    condition = lambda x: not x.startswith('__') and isinstance(getattr(root, x), ftypes)

    if handler in [getattr(root, m) for m in dir(root) if condition]:
        return hierarchy

    members = [getattr(root, m) for m in dir(root)
               if not m.startswith('__')
               and not isinstance(getattr(root, m), ntypes)
               and m is not None]

    for m in members:
        temp = copy.copy(hierarchy)
        temp.append(m)
        result = _get_hierarchy(handler, temp)

        if result:
            return result

    return []


def _get_auth_required(handler):
    """
    Verifies whether the given handler has authentication required by looking into the handler itself o by iterating
    over the hierarchy
    :param handler: The handler to be verified
    :return: Whether the handler requires authentication
    :rtype: bool
    """
    hierarchy = _get_hierarchy(handler, [cherrypy.request.app.root])
    cache_key = str(hierarchy + [handler])

    if cache_key in _auth_required_cache:
        return _auth_required_cache[cache_key]

    hierarchy.reverse()  # iterate from leaf to root
    for obj in hierarchy:
        auth_required = getattr(obj, AUTH_REQUIRED, None)
        if auth_required:
            _auth_required_cache[cache_key] = auth_required
            return auth_required

    return False


def _check_authentication(handler):
    """
    Verifies whether the handler requires authentication and checks if the user is logged in

    :param handler: The handler to be verified
    """
    auth_required = getattr(handler, AUTH_REQUIRED, None)

    # check auth required on class
    if auth_required is None:
        auth_required = _get_auth_required(handler)

    if auth_required and not is_authenticated():
        login_page = cherrypy.request.config.get(LOGIN_PAGE, DEFAULT_LOGIN_PAGE)
        redirect(login_page)


def _check_authorization(handler):
    """
    Verifies whether the user has the required permissions based on the provided authorizer function

    :param handler: The handler to be verified
    """
    auth_claims = _get_auth_claims(handler)

    authorizer = cherrypy.request.config.get(AUTHORIZER, None)

    if auth_claims and not authorizer:
        raise Exception('Missing Authorizer')

    if auth_claims and not authorizer(auth_claims):
        unauthorized_page = cherrypy.request.config.get(UNAUTHORIZED_REDIRECT, False)

        # if we have an unauthorized error page
        if unauthorized_page:
            redirect(unauthorized_page)

        # otherwise, show http 403
        raise cherrypy.HTTPError(403)


def _get_auth_claims(handler):
    """
    Return the authorization claims for the given handler that the user must satisfy

    :param handler: The handler to be verified
    :return: dict containing the authorization claims
    :rtype: dict
    """
    auth_claims = {}
    # get auth claims from handler
    handler_auth_claims = getattr(handler, AUTH_CLAIMS, {})

    if isinstance(handler, types.MethodType):
        # get auth claims from class
        auth_claims.update(getattr(handler.__self__, AUTH_CLAIMS, {}))

    # merge claims from class with claims from handler, overwriting claims from class
    auth_claims.update(handler_auth_claims)

    return auth_claims


def authorizer_tool():
    """
    Tool to verifying authentication and authorization
    """
    try:
        handler = cherrypy.request.handler.callable
    except AttributeError:  # something wrong happened, leave it to cherrypy
        return

    _check_authentication(handler)

    if USER_SESSION_KEY in cherrypy.session:
        setattr(cherrypy.request, REQUEST_USER, cherrypy.session[USER_SESSION_KEY])

    _check_authorization(handler)