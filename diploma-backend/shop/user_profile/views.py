from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from rest_framework.parsers import MultiPartParser

from .models import Profile, ProfileAvatar
from .serializers import ProfileSerializer, UpdateProfileSerializer, UpdatePasswordSerializer


class ProfileView(APIView):
    """Получение и обновление профиля пользователя"""

    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['profile'],
        description="Получение профиля",
        responses={
            200: {"description": "Successful operation"},
        }
    )
    def get(self, request: Request) -> Response:
        """Обновление профиля пользователя"""

        data = Profile.objects.filter(user=self.request.user).select_related('user', 'avatar').first()

        serializer = ProfileSerializer(data)

        return Response(serializer.data)


    @extend_schema(
        tags=['profile'],
        description="Обновление профиля",
        responses={
            200: {"description": "Successful operation"},
            400: {'description': 'Bad request'},
        },
        request=UpdateProfileSerializer
    )
    def post(self, request: Request) -> Response:
        """Обновление профиля"""

        request_serializer = UpdateProfileSerializer(data=request.data)

        if not request_serializer.is_valid():
            return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        profile = Profile.objects.filter(user=self.request.user).select_related('user').first()

        profile.user.email = request_serializer.validated_data['email']
        profile.fullName = request_serializer.validated_data['fullName']
        profile.phone = request_serializer.validated_data['phone']

        profile.save()
        profile.user.save()

        response_serializer = ProfileSerializer(profile)

        return Response(response_serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    tags=['profile'],
    description="Обновление пароля",
    responses={
        200: {"description": "Successful operation"},
        400: {'description': 'Bad request'},
    },
    request=UpdatePasswordSerializer
)
class UpdatePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        """Обновление пароля"""

        serializer = UpdatePasswordSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        current_password = serializer.validated_data['currentPassword']
        new_password = serializer.validated_data['newPassword']

        if not check_password(current_password, user.password):
            return Response({
                "message": "Invalid password"
            }, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        update_session_auth_hash(request, user)

        return Response({
            "description": "Successful operation"
        })


@extend_schema(
    tags=['profile'],
    description="Обновление аватара пользователя",
    request={
        'multipart/form-data': {
            'type': 'object',
            'properties': {
                'avatar': {
                    'type': 'string',
                    'format': 'binary',
                    'description': 'Файл изображения (JPEG, PNG, GIF, WEBP)'
                }
            },
            'required': ['avatar']
        }
    },
    responses={
        200: {'Successful operation'},
        400: {'description': 'Bad request'},
        401: {'description': 'Unauthorized'},
    }
)
class UpdateAvatarView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request: Request) -> Response:
        """Обновление аватара"""

        profile = request.user.profile
        avatar = request.FILES['avatar']

        max_size = 5 * 1024 * 1024

        if avatar.size > max_size:
            return Response({
                "message": "File is too large, max size 5 mb",
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            avatar_obj = profile.avatar

            if avatar_obj.preview:
                avatar_obj.preview.delete()

            avatar_obj.preview = avatar
            avatar_obj.alt = f"Avatar for {request.user.username}"
            avatar_obj.save()
        except ProfileAvatar.DoesNotExist:
            ProfileAvatar.objects.create(
                profile=profile,
                preview=avatar,
                alt=f"Avatar for {request.user.username}"
            )

        return Response({
            "message": "Successful operation",
        }, status=status.HTTP_200_OK)
