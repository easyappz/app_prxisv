from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from .serializers import MessageSerializer, MemberSerializer, RegisterSerializer, LoginSerializer
from .models import Member, Token


class HelloView(APIView):
    """
    A simple API endpoint that returns a greeting message.
    """

    @extend_schema(
        responses={200: MessageSerializer}, description="Get a hello world message"
    )
    def get(self, request):
        data = {"message": "Hello!", "timestamp": timezone.now()}
        serializer = MessageSerializer(data)
        return Response(serializer.data)


class TokenAuthentication:
    """
    Custom token authentication helper.
    """
    @staticmethod
    def authenticate(request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        try:
            token_key = auth_header.split(' ')[1] if ' ' in auth_header else auth_header
            token = Token.objects.select_related('member').get(key=token_key)
            return token.member
        except (Token.DoesNotExist, IndexError):
            return None


class RegisterView(APIView):
    """
    API endpoint for user registration.
    POST /api/auth/register/
    """

    @extend_schema(
        request=RegisterSerializer,
        responses={
            201: {
                'type': 'object',
                'properties': {
                    'token': {'type': 'string'},
                    'user': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer'},
                            'username': {'type': 'string'}
                        }
                    }
                }
            },
            400: {'type': 'object', 'properties': {'detail': {'type': 'string'}}}
        },
        description="Register a new user with username and password"
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            error_message = next(iter(serializer.errors.values()))[0] if serializer.errors else "Validation error"
            return Response(
                {"detail": str(error_message)},
                status=status.HTTP_400_BAD_REQUEST
            )

        member = serializer.save()
        token = Token.objects.create(member=member)
        
        return Response(
            {
                "token": token.key,
                "user": MemberSerializer(member).data
            },
            status=status.HTTP_201_CREATED
        )


class LoginView(APIView):
    """
    API endpoint for user login.
    POST /api/auth/login/
    """

    @extend_schema(
        request=LoginSerializer,
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'token': {'type': 'string'},
                    'user': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer'},
                            'username': {'type': 'string'}
                        }
                    }
                }
            },
            400: {'type': 'object', 'properties': {'detail': {'type': 'string'}}}
        },
        description="Authenticate user with username and password"
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            error_message = next(iter(serializer.errors.values()))[0] if serializer.errors else "Invalid credentials"
            return Response(
                {"detail": str(error_message)},
                status=status.HTTP_400_BAD_REQUEST
            )

        member = serializer.validated_data['member']
        token = Token.objects.create(member=member)
        
        return Response(
            {
                "token": token.key,
                "user": MemberSerializer(member).data
            },
            status=status.HTTP_200_OK
        )


class MeView(APIView):
    """
    API endpoint to get current authenticated user.
    GET /api/auth/me/
    """

    @extend_schema(
        responses={
            200: MemberSerializer,
            401: {'type': 'object', 'properties': {'detail': {'type': 'string'}}}
        },
        description="Get information about the currently authenticated user"
    )
    def get(self, request):
        member = TokenAuthentication.authenticate(request)
        if not member:
            return Response(
                {"detail": "Unauthorized - invalid or missing token"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        return Response(
            MemberSerializer(member).data,
            status=status.HTTP_200_OK
        )
