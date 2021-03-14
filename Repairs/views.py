from rest_framework import viewsets, mixins
from Repairs.serializers import RepairRequestSerializer, TagSerializer
from Repairs.models import RepairRequest, Tag


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = []


class RepairRequestViewSet(mixins.CreateModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    queryset = RepairRequest.objects.all()
    serializer_class = RepairRequestSerializer
    permission_classes = []

