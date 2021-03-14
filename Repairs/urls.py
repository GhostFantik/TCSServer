from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Repairs.views import RepairRequestViewSet, TagViewSet


router = DefaultRouter()
router.register(r'request', RepairRequestViewSet)
router.register(r'tag', TagViewSet)

urlpatterns = [
    path('', include(router.urls)),
]