from django.db import models
from django.contrib.postgres.fields import JSONField
from patients.models import Patient
from subjects.models import Practitioner
from testdefinitions.models import TestDef, Device
from locations.models import Location


# Create your models here.


class ServiceRequest(models.Model):
    STATUS = (
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('on-hold', 'On Hold'),
        ('revoked', 'Revoked'),
        ('completed', 'Completed'),
        ('entered-in-error', 'Entered in Error'),
        ('unknown', 'Unknown'),
    )

    INTENT = (
        ('original', 'Original order'),
        ('reflex', 'Reflex order'),
    )

    PRIORITY = (
        ('routine', 'Routine'),
        ('urgent', 'Urgent'),
        ('asap', 'ASAP'),
        ('stat', 'STAT'),
    )

    basedOn = models.ForeignKey('self', null=True, related_name='request_based_on', on_delete=models.CASCADE)
    replaces = models.ForeignKey('self', null=True, related_name='request_replaces', on_delete=models.CASCADE)
    requisition = models.CharField(max_length=12)
    status = models.CharField(max_length=25, choices=STATUS)
    intent = models.CharField(max_length=25, choices=INTENT)
    category = models.CharField(max_length=25, default='Laboratory procedure')
    priority = models.CharField(max_length=10, default='routine')
    doNotPerform = models.BooleanField(default=False)
    subject = models.ForeignKey(Patient, on_delete=models.PROTECT)
    authoredOn = models.DateTimeField(auto_now_add=True, blank=True)
    requester = models.ForeignKey(Practitioner, on_delete=models.PROTECT)
    locationReference = models.ForeignKey(Location, on_delete=models.CASCADE)
    reasonReference = models.IntegerField(null=True)  # link to SNOMED diagnosis
    encounter = models.IntegerField(null=True)  # link to Encounter for billing purposes
    note = models.TextField(null=True)
    relevantHistory = models.TextField(null=True)


class Procedure(models.Model):
    STATUS = (
        ('preparation', 'Preparation'),
        ('in-progress', 'In Progress'),
        ('not-done', 'Not Done'),
        ('on-hold', 'On Hold'),
        ('stopped', 'Stopped'),
        ('completed', 'Completed'),
        ('entered-in-error', 'Entered in Error'),
    )

    OUTCOME = (
        ('successful', 'Procedure successful'),
        ('unsuccessful', 'Procedure unsuccessful'),
        ('refuse', 'Patient refused'),
    )

    PRIORITY = (
        ('routine', 'Routine'),
        ('urgent', 'Urgent'),
        ('asap', 'ASAP'),
        ('stat', 'STAT'),
    )

    basedOn = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE)
    partOf = models.ForeignKey('self', null=True, related_name='procedure_part_of', on_delete=models.CASCADE)
    status = models.CharField(max_length=25, choices=STATUS, default='preparation')
    code = models.CharField(max_length=16, default='28520004')  # venupuncture
    # link to SNOMED procedure, update from collection procedure of type_tested of specified test on ordering
    priority = models.CharField(max_length=10, default='routine')
    performedDateTime = models.DateTimeField(null=True)
    location = models.ForeignKey(Location, null=True, on_delete=models.CASCADE)
    outcome = models.CharField(max_length=25, choices=OUTCOME, null=True)
    doNotPerform = models.BooleanField(default=False)


class ProcedurePerformer(models.Model):
    procedure = models.ForeignKey(Procedure, related_name='procedure_performers', on_delete=models.CASCADE)
    actor = models.ForeignKey(Practitioner, on_delete=models.CASCADE)


class Observation(models.Model):
    STATUS = (
        ('registered', 'Registered'),
        ('preliminary', 'Preliminary'),
        ('final', 'Final'),
        ('amended', 'Amended'),
        ('corrected', 'Corrected'),
        ('cancelled', 'Cancelled'),
        ('entered-in-error', 'Entered in Error'),
        ('unknown', 'Unknown'),
    )

    basedOn = models.ForeignKey(ServiceRequest, related_name='observations', on_delete=models.CASCADE)
    partOf = models.ForeignKey(Procedure, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='registered')
    category = models.CharField(max_length=20, default='laboratory')
    code = models.ForeignKey(TestDef, related_name='testdefs', on_delete=models.CASCADE)
    effectiveDateTime = models.DateTimeField(null=True)
    value = JSONField()
    dataAbsentReason = models.CharField(max_length=20, null=True)  # link to codes table
    interpretation = models.CharField(max_length=20, null=True)
    note = models.CharField(max_length=255, null=True)
    method = models.ForeignKey(Device, on_delete=models.CASCADE)
    referenceRange = JSONField()
    component = models.ForeignKey('self', related_name='derived_from', on_delete=models.PROTECT, null=True)


class ObservationPerformer(models.Model):
    observation = models.ForeignKey(Observation, related_name='observer_performers', on_delete=models.CASCADE)
    actor = models.ForeignKey(Practitioner, on_delete=models.CASCADE)
    function = models.CharField(max_length=20)
