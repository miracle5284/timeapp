from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from utils import sub_dict
from django.conf import settings


@api_view(['GET'])
@permission_classes([AllowAny])
def extension_info(request):
    return Response(sub_dict(settings, 'EXTENSION_ID', 'EXTENSION_NAME'))

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    return Response({'status': "ok"})