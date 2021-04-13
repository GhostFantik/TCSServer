from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Auth.views import CarViewSet, MechanicViewSet, AdminViewSet, DriverViewSet, UserView

router = DefaultRouter()
router.register(r'car', CarViewSet)
router.register(r'mechanic', MechanicViewSet)
router.register(r'admin', AdminViewSet)
router.register(r'driver', DriverViewSet)
urlpatterns = [
    path('', include('djoser.urls.jwt')),
    path('', include(router.urls)),
    path('me', UserView.as_view())
]
