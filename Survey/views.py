from rest_framework.viewsets import ModelViewSet
from Survey.serializers import SurveySerializer
from Survey.models import Survey


class SurveyViewSet(ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = []
