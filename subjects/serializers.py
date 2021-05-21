from djongo import models
from rest_meets_djongo import serializers
#from rest_framework import serializers
from .models import Person, HumanName, Address, Communication, ContactPoint, Identification, Metadata


class IdentificationSerializer(serializers.DjongoModelSerializer):
    class Meta:
        model = Identification
        fields = ['idValue', 'idType']


class HumanNameSerializer(serializers.DjongoModelSerializer):
    class Meta:
        model = HumanName
        fields = ['text', 'family', 'given', 'middle', 'prefix', 'suffix', 'use']


class AddressSerializer(serializers.DjongoModelSerializer):
    class Meta:
        model = Address
        fields = ['use', 'type', 'text', 'city', 'district', 'state', 'postalCode', 'country']


class CommunicationSerializer(serializers.DjongoModelSerializer):
    class Meta:
        model = Communication
        fields = ['language', 'preferred']


class ContactPointSerializer(serializers.DjongoModelSerializer):
    class Meta:
        model = ContactPoint
        fields = ['system', 'value', 'use', 'type', 'rank']


class MetaDataSerializer(serializers.DjongoModelSerializer):
    class Meta:
        model = Metadata
        fields = ['author', 'pub_date', 'mod_date']


class PersonSerializer(serializers.DjongoModelSerializer):

    class Meta:
        model = Person
        fields = [
            'active', 'sex', 'gender', 'birthDate', 'deceasedDate', 'maritalStatus', 'ethnicity', 'religion',
            'identification', 'humanname', 'address', 'communication', 'contactpoint', 'metadata',
        ]

