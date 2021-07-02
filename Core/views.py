from django.shortcuts import get_object_or_404
from django.db.models.functions import Length
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from Core.serializers import CompanySerializer, RouteSerializer
from Core.models import Company, Route
from Auth.permissions import (IsCarReadOnlyPermission, IsAdminReadOnlyPermission,
                              IsReadOnlyAllRolePermission, IsDriverReadOnlyPermission, IsAdminPermission)


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsReadOnlyAllRolePermission|IsAdminUser]
    name_parameter = openapi.Parameter('name', openapi.IN_QUERY, type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[name_parameter])
    @action(detail=False, methods=['GET'])
    def current(self, request):
        name = self.request.query_params.get('name')
        company: Company = get_object_or_404(Company, name=name)
        return Response(CompanySerializer(company).data, status=HTTP_200_OK)


# GET - Admin, Car, Driver, POST - Admin, PATCH- Admin, DELETE - Admin
class RouteViewSet(ModelViewSet):
    queryset = Route.objects.order_by(Length('name').asc(), 'name')
    serializer_class = RouteSerializer
    permission_classes = [IsDriverReadOnlyPermission|IsCarReadOnlyPermission|
                          IsAdminReadOnlyPermission|IsAdminPermission|IsAdminUser]
    http_method_names = ['get', 'post', 'head', 'options', 'delete', 'patch']
    name_parameter = openapi.Parameter('name', openapi.IN_QUERY, type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[name_parameter])
    @action(detail=False, methods=['GET'])
    def current(self, request):
        name = self.request.query_params.get('name')
        route:  Route = get_object_or_404(Route, name=name)
        return Response(RouteSerializer(route).data, status=HTTP_200_OK)
