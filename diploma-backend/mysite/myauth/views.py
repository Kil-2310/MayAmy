import json
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import status

from .serializers import UserLoginSerializer, UserRegistrationSerializer
from .models import Profile


@extend_schema(
    tags=['auth'],
    description="Регистрация нового пользователя",
    request=UserRegistrationSerializer,
    responses={
        200: {"description": "Successfully registered"},
        400: {"description": "Validation Error"},
    },
)
class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        """Регистрация нового пользователя"""

        serializer = UserRegistrationSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        name = serializer.validated_data['name']

        user = User.objects.create_user(username=username, password=password)

        Profile.objects.create(user=user, name=name)
        login(request, user)

        return Response({"message": "User created successfully"}, status=status.HTTP_200_OK)


@extend_schema(
    tags=['auth'],
    description="Вход в аккаунт",
    responses={
        200: {"description": "Успешный выход"},
        400: {"description": "Validation Error"},
        404: {"description": "Not found"},
    },
    request=UserLoginSerializer,
)
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        """Вход в аккаунт"""

        # serializer = UserLoginSerializer(data=request.data)
        #
        # if not serializer.is_valid():
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        #
        # username = serializer.validated_data['username']
        # password = serializer.validated_data['password']

        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return Response({"message": "Successfully logged in"}, status=status.HTTP_200_OK)

        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)


@extend_schema(
    tags=['auth'],
    description="Выход из аккаунта",
    responses={200: {"description": "Successfully logout"}},
)
class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        """Выход из аккаунта"""

        logout(request)
        return Response({"message": "Successfully logout"}, status=status.HTTP_200_OK)