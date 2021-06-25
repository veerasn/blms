from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from .models import Patient, Name, Address, Communication, ContactPoint, Identification


class NameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Name
        fields = ('text', 'family', 'given', 'middle', 'prefix', 'suffix', 'use', 'active')


class IdentificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Identification
        fields = ('idValue', 'idType')


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['use', 'type', 'text', 'city', 'district', 'state', 'postalCode', 'country']


class CommunicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Communication
        fields = ['id', 'language', 'preferred']


class ContactPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactPoint
        fields = ['id', 'system', 'value', 'use', 'type', 'rank']


class PatientSerializer(serializers.ModelSerializer):

    names = NameSerializer(many=True)
    identifications = IdentificationSerializer(many=True)

    class Meta:
        model = Patient
        fields = ['pk', 'names', 'identifications', 'addresses', 'contactPoints', 'sex', 'gender', 'birthDate',
                  'deceasedDate', 'maritalStatus',
                  'ethnicity', 'religion']


class PatientNestedSerializer(WritableNestedModelSerializer):

    names = NameSerializer(many=True)
    identifications = IdentificationSerializer(many=True)
    addresses = AddressSerializer(many=True)

    class Meta:
        model = Patient
        fields = ['pk', 'names', 'identifications', 'addresses', 'sex', 'gender', 'birthDate',
                  'deceasedDate', 'maritalStatus',
                  'ethnicity', 'religion']

