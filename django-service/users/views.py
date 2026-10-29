from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Users
from .serializers import UserSerializer

class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all().order_by("id")
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    authentication_classes = []
    http_method_names = ["get", "post", "patch", "head", "options"]


