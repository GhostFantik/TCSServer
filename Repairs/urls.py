from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Repairs.views import RepairRequestViewSet, RepairViewSet,TagViewSet, TypeRepairViewSet


router = DefaultRouter()
router.register(r'request', RepairRequestViewSet)
router.register(r'repair', RepairViewSet)
router.register(r'tag', TagViewSet)
router.register(r'type', TypeRepairViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
