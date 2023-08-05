# -*- coding: utf-8 -*-

try:
    import urlparse # python2
except ImportError:
    import urllib.parse as urlparse # renamed in python3
try:
    from urllib import urlencode # python2
except ImportError:
    from urllib.parse import urlencode # moved in python3

from pyramid.httpexceptions import HTTPFound
from pyramid.interfaces import IAuthenticationPolicy
from pyramid.security import Everyone, Authenticated
from zope.interface import implementer

from .interfaces import *


def get_user_from_session(request):
    """Create a helper function for getting the user profile from request.user
    """
    return request.session.get('profile')


@implementer(IAuthenticationPolicy)
class OpenstaxAccountsAuthenticationPolicy(object):

    def __init__(self, client_factory, client_args, application_url,
            login_path, callback_path, logout_path):
        self.client_factory = client_factory
        self.client_args = client_args
        self.application_url = application_url
        self.login_path = login_path
        self.callback_path = callback_path
        self.logout_path = logout_path

    def _login(self, request):
        client = self.client_factory(*self.client_args)
        raise HTTPFound(location=client.auth_uri())

    def authenticated_userid(self, request):
        if request.path == self.login_path:
            return self._login(request)
        if request.path == self.callback_path:
            code = request.params['code']
            client = self.client_factory(*self.client_args)
            client.request_token_with_code(code)
            me = client.request('/api/user.json')
            request.session.update({
                'profile': me,
                'username': me.get('username'),
                })
            request.session.changed()
            return me.get('username')
        return self.unauthenticated_userid(request)

    def unauthenticated_userid(self, request):
        return request.session.get('username')

    def effective_principals(self, request):
        groups = [Everyone]
        userid = self.authenticated_userid(request)
        if userid:
            groups.append(Authenticated)
            groups.append(userid)
        return groups

    def remember(self, request, principal, **kw):
        pass

    def forget(self, request):
        if self.unauthenticated_userid(request):
            client = self.client_factory(*self.client_args)
            logout_url = urlparse.urljoin(client.server_url, '/logout')
            return_to = urlparse.urljoin(self.application_url, self.logout_path)
            params = urlencode({'return_to': return_to})
            request.session.clear()
            raise HTTPFound(location='?'.join([logout_url, params]))


def main(config):
    config.add_request_method(get_user_from_session, 'user', reify=True)
    settings = config.registry.settings
    config.registry.registerUtility(OpenstaxAccountsAuthenticationPolicy(
        client_factory=config.registry.getUtility(IOpenstaxAccounts, 'factory'),
        client_args=(settings['openstax_accounts.server_url'],
                     settings['openstax_accounts.application_id'],
                     settings['openstax_accounts.application_secret'],
                     settings['openstax_accounts.application_url']),
        application_url=settings['openstax_accounts.application_url'],
        login_path=settings['openstax_accounts.login_path'],
        callback_path=settings['openstax_accounts.callback_path'],
        logout_path=settings['openstax_accounts.logout_path'],
        ), IOpenstaxAccountsAuthenticationPolicy)
