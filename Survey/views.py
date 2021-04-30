from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from Survey.serializers import SurveySerializer
from Survey.models import Survey
from Auth.permissions import (IsCarPermission, IsAdminPermission, IsDriverPermission)


# GET - ADMIN, POST - Car, Driver, Admin. Remove PATCH, DELETE query
class SurveyViewSet(ModelViewSet):
    queryset = Survey.objects.order_by('date', '-end_time')
    serializer_class = SurveySerializer
    permission_classes = [IsCarPermission|IsDriverPermission|IsAdminPermission|IsAdminUser]
    http_method_names = ['get', 'post', 'head', 'options']
