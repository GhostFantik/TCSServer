from django.shortcuts import get_object_or_404
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from Core.serializers import CompanySerializer, RouteSerializer
from Core.models import Company, Route


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = []
    name_parameter = openapi.Parameter('name', openapi.IN_QUERY, type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[name_parameter])
    @action(detail=False, methods=['GET'])
    def current(self, request):
        name = self.request.query_params.get('name')
        company: Company = get_object_or_404(Company, name=name)
        return Response(CompanySerializer(company).data, status=HTTP_200_OK)


class RouteViewSet(ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = []
    name_parameter = openapi.Parameter('name', openapi.IN_QUERY, type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[name_parameter])
    @action(detail=False, methods=['GET'])
    def current(self, request):
        name = self.request.query_params.get('name')
        route:  Route = get_object_or_404(Route, name=name)
        return Response(RouteSerializer(route).data, status=HTTP_200_OK)
