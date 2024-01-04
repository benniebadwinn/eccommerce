# backends.py

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class CaseInsensitiveModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            # Case-insensitive lookup for the username
            user = UserModel._default_manager.get(username__iexact=username)
        except UserModel.DoesNotExist:
            return None

        if user.check_password(password):
            return user
