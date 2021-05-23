from rest_framework import serializers
from .models import Person, Address, Communication, ContactPoint, Identification


class IdentificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Identification
        fields = ['idValue', 'idType']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['use', 'type', 'text', 'city', 'district', 'state', 'postalCode', 'country']


class CommunicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Communication
        fields = ['language', 'preferred']


class ContactPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactPoint
        fields = ['system', 'value', 'use', 'type', 'rank']


class PersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = '__all__'

