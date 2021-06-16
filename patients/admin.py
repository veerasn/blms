from django.contrib import admin
from .models import Patient, Name, Identification, Address, Communication, ContactPoint, Contact

# Register your models here.
admin.site.register([Patient, Name, Identification, Address, Communication, ContactPoint, Contact])

