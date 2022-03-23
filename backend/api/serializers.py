from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.exceptions import APIException
from .models import User, Codes, Friends, Tokens
import re
import random

class InvalidPhoneFormat(APIException):
    status_code = 400
    default_detail = 'Invalid value in phone number'

class InvalidCode(APIException):
    status_code = 403
    default_detail = 'Invalid confirmation code'

class UserValidationError(APIException):
    status_code = 403
    default_detail = 'Invalid access token'

class AddFriendError(APIException):
    status_code = 400
    default_detail = 'Failed to add friend'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number']

    def to_internal_value(self, data):
        self.__validate_phone_number(data)
        return super().to_internal_value(data)

    def __validate_phone_number(self, data):
        self.__check_phone_number_regex(data["phone_number"])

    def __check_phone_number_regex(self, phone_number):
        pattern = re.compile("\+[0-9]+")
        if not bool(pattern.match(phone_number)):
            raise InvalidPhoneFormat()

    def check_phone_number_exists_or_save(self, phone_number):
        if not User.objects.filter(phone_number=phone_number).exists():
            self.save()
            return True
        return False

    def generate_confirmation_code_for_login(self, phone_number):
        user = User.objects.filter(phone_number=phone_number).first()
        new_code = random.randint(1000,9999)
        code = Codes.objects.filter(user=user).first()
        if not code:
            code = Codes(code=new_code, user=user)
            code.save()
        else:
            code.code = new_code
            code.save(update_fields=["code"])
        return code.code


class VerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = Codes
        fields = ["code"]

    def to_internal_value(self, data):
        self.__validate_code(data)
        return super().to_internal_value(data)

    def get_user(self, data):
        return User.objects.filter(phone_number=data["phone_number"]).first()

    def __validate_code(self, data):
        user = User.objects.filter(phone_number=data["phone_number"]).first()
        code = Codes.objects.filter(user=user, code=data["code"]).first()
        if not code:
            raise InvalidCode
        code.delete()

class TokensSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tokens
        fields = ["refresh_token", "access_token"]

    def to_internal_value(self, data):
        return super().to_internal_value(data)

class AddFriend(serializers.ModelSerializer):
	friend = serializers.CharField(max_length=6)


class FriendsSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Friends
        fields = ["user"]

    def get_all_friends_that_added_me(self, user_id):
        friends = Friends.objects.filter(friend_id=user_id).values_list("user", flat=True)
        return User.objects.filter(id__in=friends).values_list("phone_number", flat=True)


    def add_friend(self, user_id, friend_identifier):
        friend = User.objects.filter(identifier=friend_identifier).first()
        user = User.objects.filter(id=user_id).first()
        exists = Friends.objects.filter(friend=friend, user=user).first()
        if not exists:
            try:
                if user != friend:
                    return Friends(user=user, friend=friend).save()
                return None
            except Exception as e:
                raise AddFriendError()