"""
Middleware for FastAPI that supports authenticating users against Keycloak
"""

__version__ = "0.0.1"

from famiware.middleware import KeycloakMiddleware
from famiware.schemas.keycloak_configuration import (
    KeycloakConfiguration,
)

__all__ = [KeycloakMiddleware.__name__, KeycloakConfiguration.__name__]
