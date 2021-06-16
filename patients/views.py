from django.shortcuts import render
from rest_framework import  viewsets
from .models import Patient
from .serializers import PatientSerializer, PatientNestedSerializer

# Create your views here.


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientNestedSerializer
