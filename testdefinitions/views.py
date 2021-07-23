from rest_framework import viewsets
from testdefinitions.models import TestComposition, TestDef
from testdefinitions.serializers import TestCompositionSerializer, TestDefSerializer


class TestCompositionViewSet(viewsets.ModelViewSet):
    queryset = TestDef.objects.all()
    serializer_class = TestDefSerializer
