from rest_framework.views import exception_handler
from .models import Tokens
from .serializers import TokensSerializer
from .auth import AuthService

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data['status_code'] = response.status_code

    return response

def create_token_pair(user):
        tokens = Tokens.objects.filter(user=user).first()
        access_token = AuthService().create_access_token_for_user(user)
        refresh_token = AuthService().create_refresh_token_for_user(user)
        if tokens:
            tokens.access_token = access_token
            tokens.refresh_token = refresh_token
            tokens.save(update_fields=["access_token", "refresh_token"])
        else:
            tokens = Tokens(access_token=access_token, refresh_token=refresh_token, user=user)
            tokens.save()            
        return tokens

def refresh_token_pair(tokens: TokensSerializer):
    user = AuthService().get_user_from_token(token=tokens.data["refresh_token"])
    tokens = Tokens.objects.filter(user=user).first()
    access_token = AuthService().create_access_token_for_user(user)
    refresh_token = AuthService().create_refresh_token_for_user(user)
    if tokens:
        tokens.access_token = access_token
        tokens.refresh_token = refresh_token
        tokens.save(update_fields=["access_token", "refresh_token"])
    else:
        tokens = Tokens(access_token=access_token, refresh_token=refresh_token, user=user)
        tokens.save()            
    return tokens

def check_access_token(token):
    return AuthService().get_user_from_token(token=token)
