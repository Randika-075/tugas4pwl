from pyramid.config import Configurator
from pyramid.authorization import ACLAuthorizationPolicy

from pyramid.security import ALL_PERMISSIONS

from pyramid.authorization import Allow


def add_role_principals(userid, request):
    return [f'{request.jwt_claims.get("role", [])}']


class RootACL(object):
    __acl__ = [
        (Allow, "admin", ALL_PERMISSIONS),
        (Allow, "user", "view"),
    ]

    def __init__(self, request):
        pass


def main(global_config, **settings):
    """This function returns a Pyramid WSGI application."""
    with Configurator(settings=settings) as config:
        config.include("pyramid_jinja2")
        config.set_root_factory(RootACL)
        config.set_authorization_policy(ACLAuthorizationPolicy())
        config.include("pyramid_jwt")
        config.set_jwt_authentication_policy(
            "secret",
            expiration=3600,
            auth_type="Bearer",
            callback=add_role_principals,
        )
        config.include(".routes")
        config.include(".models")
        config.scan()
    return config.make_wsgi_app()
