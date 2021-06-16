from django.db import models
from patients.models import Patient
from subjects.models import Practitioner
from testdefs.models import LocalTestCode


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
    locationReference = models.IntegerField  # link to Location
    reasonReference = models.IntegerField  # link to SNOMED diagnosis
    encounter = models.IntegerField  # link to Encounter
    note = models.TextField
    relevantHistory = models.TextField


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

    STATUS_REASON = (
        ('fail', 'Procedure failed'),
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
    requisition = models.CharField(max_length=12)
    status = models.CharField(max_length=25, choices=STATUS)
    statusReason = models.CharField(max_length=25, choices=STATUS_REASON, null=True)
    code = models.IntegerField  # link to SNOMED procedure, update from ActivityList of specified test
    priority = models.CharField(max_length=10, default='routine')
    doNotPerform = models.BooleanField(default=False)

