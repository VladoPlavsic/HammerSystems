from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer, VerifySerializer, TokensSerializer, UserValidationError, FriendsSerailizer
from .models import User
from .auth import AuthService
from .utils import create_token_pair, refresh_token_pair, check_access_token
import time

@api_view(["POST"])
def auth(request):
    time.sleep(1)
    serialized = UserSerializer(data=request.data)
    if serialized.is_valid():
        created = serialized.check_phone_number_exists_or_save(request.data["phone_number"])
        code = serialized.generate_confirmation_code_for_login(request.data["phone_number"])
        return Response({"created": created, "code": code})

@api_view(["POST"])
def verify(request):
    serialized = VerifySerializer(data=request.data)
    if serialized.is_valid():
        user = serialized.get_user(data=request.data)
        tokens = create_token_pair(user)
        serialized = TokensSerializer(data={"refresh_token": tokens.refresh_token, "access_token": tokens.access_token})
        if serialized.is_valid():
            return Response(serialized.data)
        
@api_view(["POST"])
def refresh_token(request):
    serialized = TokensSerializer(data=request.data)
    if serialized.is_valid():
        refreshed = refresh_token_pair(serialized)
        serialized = TokensSerializer(data={"refresh_token": refreshed.refresh_token, "access_token": refreshed.access_token})
        if serialized.is_valid():
            return Response(serialized.data)

@api_view(["GET"])
def profile(request):
    access_token = request.COOKIES['access_token']
    user = check_access_token(access_token)
    serialized = FriendsSerailizer(data={"user": user.id})
    if serialized.is_valid():
        friends = serialized.get_all_friends_that_added_me(user.id)
        return Response({"friends": friends, "user_identifier": user.identifier})

@api_view(["POST"])
def add_friend(request):
    access_token = request.COOKIES['access_token']
    user = check_access_token(access_token)
    serialized = FriendsSerailizer(data={"user": user.id})

    if serialized.is_valid():
        friend = serialized.add_friend(user_id=user.id, friend_identifier=request.data["friend_identifier"])
        return Response(friend)
