from rest_framework import viewsets, mixins

from .models import Patient
from .serializers import PatientSerializer, PatientNestedSerializer


# Create your views here.


class PatientViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    queryset = Patient.objects.all()
    serializer_class = PatientNestedSerializer

    def get_queryset(self):
        search = self.kwargs['search']
        return Patient.objects.filter(names__text__icontains=search)[:20]
