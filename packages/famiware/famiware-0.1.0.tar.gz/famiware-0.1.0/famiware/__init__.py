"""
Middleware for FastAPI that supports authenticating users against Keycloak
"""

__version__ = "0.1.0"

import logging

from famiware.decorators.require_permission import require_permission
from famiware.decorators.strip_request import strip_request
from famiware.dependencies.get_authorization_result import (
    get_authorization_result,
)
from famiware.dependencies.get_user import get_user
from famiware.fast_api_user import FastApiUser
from famiware.middleware import KeycloakMiddleware
from famiware.schemas.authorization_methods import (
    AuthorizationMethod,
)
from famiware.schemas.authorization_result import AuthorizationResult
from famiware.schemas.keycloak_configuration import (
    KeycloakConfiguration,
)
from famiware.schemas.match_strategy import MatchStrategy

logging.getLogger(__name__).addHandler(logging.NullHandler())

__all__ = [
    AuthorizationResult.__name__,
    KeycloakMiddleware.__name__,
    KeycloakConfiguration.__name__,
    AuthorizationMethod.__name__,
    MatchStrategy.__name__,
    FastApiUser.__name__,
    get_user.__name__,
    get_authorization_result.__name__,
    require_permission.__name__,
    strip_request.__name__,
]
