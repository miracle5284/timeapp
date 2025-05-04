from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model


User = get_user_model()

class RegisterUserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, validators=[])
    confirm_password = serializers.CharField(write_only=True, validators=[])
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'confirm_password', 'first_name', 'last_name']
        extra_kwargs = {
            "confirm_password": {"write_only": True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        attrs.pop('confirm_password')
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserTokenSerializer(TokenObtainPairSerializer):

    pass


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'account_id']
        extra_kwargs = {
            'password': {'write_only': True},
            'account_id': {'read_only': True}
        }