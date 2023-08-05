import cherrypy

from .exceptions import AuthenticationError, MissingAuthenticatorError, WrongIdentityClassError
from .utils import redirect
from ._constants import (
    AUTHENTICATOR,
    LOGIN_REDIRECT,
    LOGOUT_REDIRECT,
    USER_SESSION_KEY,
)


class Identity(object):
    """
    Provides an abstraction for the logged in user data to be stored in the session
    """

    def __init__(self, id_, display=None, data=None):
        """
        :param id_: Any value used to uniquely identify the user, like a primary key or email address
        :param display: A display name for the logged in user
        :param data: Any additional data related to the user
        """
        self.id = id_
        self.display = display
        self.data = data


def is_authenticated():
    """
    Tells whether the user is authenticated or not

    :rtype: bool
    """
    if not USER_SESSION_KEY in cherrypy.session:
        return False

    user = cherrypy.session[USER_SESSION_KEY]

    if not user:
        return False

    if not isinstance(user, Identity):
        raise WrongIdentityClassError()

    return True


def authenticate(**credentials):
    """
    Performs the authentication using the provided authenticator function

    :param credentials: The user credentials
    :return: The user data as Identity
    :rtype: Identity
    :raises: AuthenticationError
    """
    authenticator = cherrypy.request.config.get(AUTHENTICATOR, None)

    if not authenticator:
        raise MissingAuthenticatorError()

    user = authenticator(**credentials)

    if not isinstance(user, Identity):
        raise WrongIdentityClassError()

    if not user:
        raise AuthenticationError()

    cherrypy.session[USER_SESSION_KEY] = user
    return user


class AuthControllerDefaultDispatcher(object):
    """
    Provides a default authentication controller for the default dispatcher
    """

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    def login(self, _next=None, **credentials):
        authenticate(**credentials)
        redirect(_next, LOGIN_REDIRECT)

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    def logout(self, _next=None):
        del cherrypy.session[USER_SESSION_KEY]
        cherrypy.lib.sessions.expire()

        redirect(_next, LOGOUT_REDIRECT)


import sys
if sys.version_info < (3,):  # Python2
    class _Login(object):
        exposed = True

        def POST(self, _next=None, **credentials):
            authenticate(**credentials)
            redirect(_next, LOGIN_REDIRECT)

    class _Logout(object):
        exposed = True

        def POST(self, _next=None):
            del cherrypy.session[USER_SESSION_KEY]
            cherrypy.lib.sessions.expire()

            redirect(_next, LOGOUT_REDIRECT)

else:  # Python3
    class _Login:
        exposed = True
        POST = AuthControllerDefaultDispatcher.login

    class _Logout:
        exposed = True
        POST = AuthControllerDefaultDispatcher.logout


class AuthControllerMethodDispatcher(object):
    """
    Provides a default authentication controller for the method dispatcher
    """
    exposed = True
    login = _Login()
    logout = _Logout()