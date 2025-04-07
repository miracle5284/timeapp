from rest_framework.decorators import api_view
from rest_framework.response import Response

from utils import sub_dict
from django.conf import settings

@api_view(['GET'])
def extension_info(request):
    return Response(sub_dict(settings, 'EXTENSION_ID', 'EXTENSION_NAME'))