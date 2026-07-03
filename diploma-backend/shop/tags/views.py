from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import AllowAny

from .models import Tag
from .serializers import TagSerializer


@extend_schema(
    tags=['tags'],
    description="Получение всех тэгов",
    responses={
        200: {"description": "Successful operation"},
    }
)
class TagsView(APIView):
    """Получение всех тэгов"""

    permission_classes = [AllowAny]

    def get(self, request: Request) -> Response:
        data = Tag.objects.all()

        serializer = TagSerializer(data, many=True)

        return Response(serializer.data)