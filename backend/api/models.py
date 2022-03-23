from django.db import models
from django.db.models import Index, UniqueConstraint

class User(models.Model):
    phone_number = models.CharField(max_length=15)
    identifier = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users"
        constraints = [
            UniqueConstraint(
                name="unique_phone_number",
                fields=["phone_number"],
            ),
            UniqueConstraint(
                name="unique_identifier",
                fields=["identifier"],
            )
        ]
        indexes = [
            Index(fields=['phone_number', 'identifier',]),
        ]
        

class Codes(models.Model):
    code = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "codes"
        constraints = [
            UniqueConstraint(
                name="unique_user",
                fields=["user"],
            ),
        ]
        indexes = [
            Index(fields=['user',]),
        ]

class Friends(models.Model):
    user = models.ForeignKey(User, related_name="me", on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name="my_friend", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "friends"
        constraints = [
            UniqueConstraint(
                name="unique_friend",
                fields=["user", "friend"],
            ),
        ]
        indexes = [
            Index(fields=['user', 'friend']),
        ]

class Tokens(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_token = models.TextField()
    refresh_token = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tokens"
        constraints = [
            UniqueConstraint(
                name="unique_user_token",
                fields=["user"],
            ),
        ]
        indexes = [
            Index(fields=['user']),
        ]


