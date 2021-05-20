from rest_framework import serializers
from .models import Person, HumanName, Address, Communication, ContactPoint, Identification, Metadata


class IdentificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Identification
        fields = ['idValue', 'idType']


class HumanNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = HumanName
        fields = ['text', 'family', 'given', 'middle', 'prefix', 'suffix', 'use']


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


class MetaDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metadata
        fields = ['author', 'pub_date', 'mod_date']


class PersonSerializer(serializers.ModelSerializer):
    identifications = IdentificationSerializer(many=True, read_only=True)
    humannames = HumanNameSerializer(many=True,  read_only=True)
    addresses = AddressSerializer(many=True,  read_only=True)
    communications = CommunicationSerializer(many=True,  read_only=True)
    contactpoints = ContactPointSerializer(many=True,  read_only=True)
    metadatas = MetaDataSerializer(many=True,  read_only=True)

    class Meta:
        model = Person
        fields = ['identifications', 'humannames', 'addresses', 'communications', 'contactpoints', 'metadatas',
                  'active', 'sex', 'gender', 'birthDate',
                  'deceasedDate', 'maritalStatus', 'ethnicity', 'religion'
        ]

