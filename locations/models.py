from django.db import models
from django.contrib.postgres.fields import JSONField
from subjects.models import Organization


# Create your models here.

class Location(models.Model):
    STATUS = (
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('inactive', 'Inactive'),
    )

    status = models.CharField(max_length=12, choices=STATUS, default='active')
    name = models.CharField(max_length=12, unique=True)
    alias = JSONField(null=True)
    description = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length=8)  # code for location type, link to location-type
    # position = (include GIS capability later)
    managingOrganization = models.ForeignKey(Organization, related_name='location_organizations', on_delete=models.CASCADE)
    partOf = models.ForeignKey('self', related_name='partsOf', on_delete=models.PROTECT, null=True)
    hoursOfOperation = JSONField(null=True)


class ContactPoint(models.Model):
    CONTACT_POINT_SYS = (
        ('phone', 'phone'),
        ('fax', 'fax'),
        ('email', 'E-mail'),
        ('url', 'url'),
        ('sms', 'sms')
    )

    SYS_USE = (
        ('H', 'home'),
        ('W', 'work'),
        ('T', 'temporary'),
        ('O', 'old'),
        ('B', 'billing')
    )

    system = models.CharField(max_length=12, choices=CONTACT_POINT_SYS)
    value = models.CharField(max_length=255)
    use = models.CharField(max_length=1, choices=SYS_USE)
    rank = models.PositiveSmallIntegerField()
    patient = models.ForeignKey(Location, related_name='contactpoints', on_delete=models.CASCADE)


class Address(models.Model):
    ADDRESS_USE = (
        ('H', 'home'),
        ('W', 'work'),
        ('T', 'temporary'),
        ('O', 'old'),
        ('B', 'billing')
    )

    ADDRESS_TYPE = (
        ('PO', 'postal'),
        ('PH', 'physical'),
        ('BO', 'both')
    )

    use = models.CharField(max_length=1, choices=ADDRESS_USE)
    type = models.CharField(max_length=2, choices=ADDRESS_TYPE)
    text = models.CharField('address', max_length=255)
    city = models.CharField(max_length=25)
    district = models.CharField(max_length=25)
    state = models.CharField(max_length=25)
    postalCode = models.CharField('post code', max_length=12)
    country = models.CharField(max_length=2, default='MY')
    patient = models.ForeignKey(Location, related_name='addresses', on_delete=models.CASCADE)