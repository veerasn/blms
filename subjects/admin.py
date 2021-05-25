from django.contrib import admin
from .models import Person, Identification

# Register your models here.
admin.site.register([Person, Identification])
