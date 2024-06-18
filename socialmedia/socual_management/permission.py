# myapp/permissions.py
from rest_framework.permissions import BasePermission

from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore



class IsJWTAuthenticated(BasePermission):
    """
    Allows access only to users authenticated via JWT authentication.
    """
    def has_permission(self, request, view):
       
        return (
            request.user and 
            request.user.is_authenticated and 
            isinstance(request.successful_authenticator, JWTAuthentication)
        )
