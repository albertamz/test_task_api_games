from rest_framework import serializers
from .models import User, UserToken


class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    phone_number = serializers.CharField(max_length=20)

    def validate(self, attrs):
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError("Username already exists")
        if User.objects.filter(phone_number=attrs['phone_number']).exists():
            raise serializers.ValidationError("Phone number already exists")
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            phone_number=validated_data['phone_number']
        )
        token = UserToken.objects.create(user=user)
        return {
            'user_id': user.id,
            'token': token.token,
            'token_expires_at': token.expires_at
        }
