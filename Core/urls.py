from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Core.views import CompanyViewSet, RouteViewSet


router = DefaultRouter()
router.register(r'company', CompanyViewSet)
router.register(r'route', RouteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]