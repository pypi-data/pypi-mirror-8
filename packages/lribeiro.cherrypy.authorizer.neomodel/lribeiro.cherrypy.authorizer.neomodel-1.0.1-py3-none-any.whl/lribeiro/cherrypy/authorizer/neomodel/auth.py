import bcrypt
import cherrypy
from lribeiro.cherrypy.authorizer.authentication import Identity, AuthenticationError

from lribeiro.cherrypy.authorizer.neomodel.models import User


def authenticator(email: str, password: str) -> Identity:
    try:
        user = User.nodes.get(email=email)
    except User.DoesNotExist:
        raise AuthenticationError()

    hashed = user.password.encode('utf-8')

    if not bcrypt.hashpw(password.encode('utf-8'), hashed) == hashed:
        raise AuthenticationError()

    return Identity(user.email, user.name, user)


def authorizer(claims: dict) -> bool:
    identity = cherrypy.request.auth_user
    try:
        user = User.nodes.get(email=identity.id)
    except User.DoesNotExist:
        return False

    for action, resource in claims.items():
        satisfied = False
        user.permissions.filters.clear()

        if isinstance(resource, str):
            for res in user.permissions.match(action=action):
                if res.name == resource:
                    satisfied = True

        elif isinstance(resource, list):
            found_permissions = list()

            for res in user.permissions.match(action=action):
                if res.name in resource:
                    found_permissions.append(res)

            satisfied = len(found_permissions) == len(resource)

        if not satisfied:
            return False

    return True