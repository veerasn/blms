from django.contrib import admin
from .models import Person, Identification, Address, Communication, ContactPoint, Organization, Qualification, \
    Practitioner, PractitionerRole

# Register your models here.
admin.site.register([Person, Identification, Address, Communication, ContactPoint, Organization, Qualification,
                     Practitioner, PractitionerRole])
