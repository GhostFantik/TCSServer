from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Survey.views import SurveyViewSet


router = DefaultRouter()
router.register(r'survey', SurveyViewSet)

urlpatterns = [
    path('', include(router.urls))
]
