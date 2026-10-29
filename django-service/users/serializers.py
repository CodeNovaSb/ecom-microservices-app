from rest_framework import serializers

from .models import Users

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = [
            "id",
            "name",
            "mail",
            "address",
            "phone_no",

        ]
        read_only_fields = ["id"]