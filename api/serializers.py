from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from .models import Member, Token


class MessageSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=200)
    timestamp = serializers.DateTimeField(read_only=True)


class MemberSerializer(serializers.ModelSerializer):
    """
    Serializer for Member model - returns user data.
    """
    class Meta:
        model = Member
        fields = ['id', 'username']
        read_only_fields = ['id']


class RegisterSerializer(serializers.Serializer):
    """
    Serializer for user registration.
    """
    username = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    def validate_username(self, value):
        if Member.objects.filter(username=value).exists():
            raise serializers.ValidationError("User with this username already exists.")
        return value

    def create(self, validated_data):
        member = Member.objects.create(
            username=validated_data['username'],
            password=make_password(validated_data['password'])
        )
        return member


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """
    username = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        try:
            member = Member.objects.get(username=username)
        except Member.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials.")

        if not check_password(password, member.password):
            raise serializers.ValidationError("Invalid credentials.")

        attrs['member'] = member
        return attrs
