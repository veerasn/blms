from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from subjects.models import Organization, ContactPoint


class SourceOrganization(models.Model):
    copyright_id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    copyright = models.TextField
    terms_of_use = models.TextField
    url = models.TextField


class TestDef(models.Model):
    loinc_num = models.CharField(max_length=10, primary_key=True)
    component = models.CharField(max_length=255)
    long_common_name = models.CharField(max_length=255)
    composition = models.ManyToManyField('self', through='TestComposition', symmetrical=False)


class TestComposition(models.Model):
    from_test_def = models.ForeignKey(TestDef, related_name='from_test_defs', on_delete=models.PROTECT)
    to_test_def = models.ForeignKey(TestDef, related_name='to_test_defs', on_delete=models.PROTECT)
    primaryTest = models.BooleanField(default=True)
    orderable = models.BooleanField(default=False)

    class Meta:
        unique_together = ('from_test_def', 'to_test_def')


class Loinc(models.Model):
    loinc_num = models.CharField(max_length=10, primary_key=True)
    component = models.CharField(max_length=255)
    property = models.CharField(max_length=64)
    time_aspct = models.CharField(max_length=32)
    system = models.CharField(max_length=255)
    scale_typ = models.CharField(max_length=8)
    method_typ = models.CharField(max_length=64)
    classname = models.CharField(max_length=32)
    VersionLastChanged = models.CharField(max_length=8)
    chng_type = models.CharField(max_length=8)
    DefinitionDescription = models.CharField(max_length=6000, null=True)
    status = models.CharField(max_length=12)
    consumer_name = models.CharField(max_length=255)
    class_type = models.IntegerField
    formula = models.CharField(max_length=512, null=True)
    exmpl_answers = models.CharField(max_length=6000, null=True)
    survey_quest_text = models.CharField(max_length=512, null=True)
    survey_quest_src = models.CharField(max_length=64)
    unitsRequired = models.CharField(max_length=1)
    submitted_units = models.CharField(max_length=32)
    relatednames2 = models.CharField(max_length=6000, null=True)
    shortname = models.CharField(max_length=128)
    order_obs = models.CharField(max_length=12)
    cdisc_common_tests = models.CharField(max_length=1)
    hl7_field_subfield_id = models.CharField(max_length=16)
    external_copyright_notice = models.CharField(max_length=3000, null=True)
    example_units = models.CharField(max_length=128)
    long_common_name = models.CharField(max_length=255)
    UnitsAndRange = models.CharField(max_length=32, null=True)
    example_ucum_units = models.CharField(max_length=40)
    example_si_ucum_units = models.CharField(max_length=40)
    status_reason = models.CharField(max_length=12)
    status_text = models.CharField(max_length=800, null=True)
    change_reason_public = models.CharField(max_length=1500, null=True)
    common_test_rank = models.IntegerField
    common_order_rank = models.IntegerField
    common_si_test_rank = models.IntegerField
    hl7_attachment_structure = models.CharField(max_length=15)
    ExternalCopyrightLink = models.CharField(max_length=25, null=True)
    PanelType = models.CharField(max_length=25)
    AskAtOrderEntry = models.CharField(max_length=16)
    AssociatedObservations = models.CharField(max_length=64)
    VersionFirstReleased = models.CharField(max_length=8)
    ValidHL7AttachmentRequest = models.CharField(max_length=1)
    DisplayName = models.CharField(max_length=255)

    def __str__(self):
        return self.loinc_num + ' - ' + self.shortname


class Additive(models.Model):
    code = models.CharField(primary_key=True, max_length=6)
    display = models.CharField(max_length=255)
    comment = models.CharField(max_length=255)

    def __str__(self):
        return 'Additive(%s, %s)' % (self.code, self.display)


class SpecimenContainer(models.Model):
    MATERIAL = (
        ('glass', 'Glass'),
        ('metal', 'Metal'),
        ('plastic', 'Plastic'),
    )

    CAP = (
        ('red', 'red cap'),
        ('yellow', 'yellow cap'),
        ('dark-yellow', 'dark yellow cap'),
        ('grey', 'grey cap'),
        ('light-blue', 'light blue cap'),
        ('black', 'black cap'),
        ('green', 'green cap'),
        ('light-green', 'light green cap'),
        ('lavender', 'lavender cap'),
        ('brown', 'brown cap'),
        ('white', 'white cap'),
        ('pink', 'pink cap'),
    )

    code = models.IntegerField(primary_key=True)
    material = models.CharField(max_length=12, choices=MATERIAL)
    description = models.TextField(max_length=255)
    type = models.TextField(max_length=255)
    cap = models.CharField(max_length=25, choices=CAP, default='')
    capacity = models.PositiveIntegerField
    minimumVolume = JSONField()
    age = JSONField()
    additive = models.ForeignKey(Additive, on_delete=models.PROTECT)
    note = models.TextField(blank=True, default='')

    class Meta:
        indexes = [models.Index(fields=['code'])]

    def __str__(self):
        return 'Specimen container (%i, %s)' % (self.code, self.type)


class TypeTested(models.Model):
    PREFERENCE = (
        ('preferred', 'Preferred'),
        ('alternative', 'Alternative'),
    )

    isDerived = models.BooleanField(default=False)  # primary or secondary specimen
    type = models.CharField(max_length=8)
    container = models.ForeignKey(SpecimenContainer, on_delete=models.PROTECT)
    requirement = models.TextField
    retentionTime = JSONField()
    rejectionCriterion = JSONField()
    handling = JSONField()


class SpecimenDefinition(models.Model):
    typeCollected = models.IntegerField  # kind of material to collect
    patientPreparation = models.IntegerField(null=True)  # patient preparation instructions for collection
    collectionProcedure = models.IntegerField(null=True)  # specimen collection procedure
    typeTested = models.ForeignKey(TypeTested, on_delete=models.PROTECT)


class ReferenceRange(models.Model):
    low = models.DecimalField
    high = models.DecimalField
    unit = models.CharField(max_length=20, blank=True, default='')
    type = JSONField()
    appliesTo = JSONField()
    age = JSONField()
    text = models.TextField(max_length=255, blank=True, default='')


class OrderValidation(models.Model):
    orderBy = JSONField()
    orderInterval = JSONField()
    validationRule = JSONField()


class Reagent(models.Model):
    REASON = (
        ('obsolete', 'Obsolete'),
        ('defective', 'Defective'),
        ('out-of-stock', 'Out of stock'),
        ('verify', 'Pending verification'),
    )

    status = models.BooleanField(default=True)
    statusReason = models.CharField(max_length=20, choices=REASON, default='ok')
    distinctIdentifier = models.CharField(max_length=50)
    manufacturer = models.CharField(max_length=25)
    unitType = models.CharField(max_length=12)
    unitPerTest = models.IntegerField


class ReagentLot(models.Model):
    REASON = (
        ('obsolete', 'Obsolete'),
        ('defective', 'Defective'),
        ('verify', 'Pending verification'),
    )

    reagent = models.ForeignKey(Reagent, on_delete=models.PROTECT)
    status = models.BooleanField(default=True)
    statusReason = models.CharField(max_length=20, choices=REASON, default='ok')
    manufactureDate = models.DateField
    expirationDate = models.DateField
    lotNumber = models.CharField(max_length=30)
    totalUnit = models.IntegerField
    location = JSONField()
    note = models.TextField
    safety = models.FilePathField
    manual = models.FilePathField


class Device(models.Model):

    STATUS = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('entered-in-error', 'Entered in error'),
        ('unknown', 'Unknown')
    )

    REASON = (
        ('online', 'Active'),
        ('paused', 'Inactive'),
        ('standby', 'Entered in error'),
        ('offline', 'Offline'),
        ('not-ready', 'Not ready'),
        ('hw-disconnect', 'Hardware disconnected'),
        ('maintenance','Maintenance ongoing'),
        ('off', 'Off'),
    )

    udiCarrier = JSONField()
    status = models.CharField(max_length=25, choices=STATUS, default='active')
    statusReason = models.CharField(max_length=25, choices=REASON, default='online')
    distinctIdentifier = models.CharField(max_length=50)
    manufacturer = models.CharField(max_length=25)
    manufactureDate = models.DateField
    expirationDate = models.DateField
    lotNumber = models.CharField(max_length=50)
    serialNumber = models.CharField(max_length=50)
    deviceName = models.CharField(max_length=50)
    modelNumber = models.CharField(max_length=50)
    partNumber = models.CharField(max_length=50, blank=True, default='')
    deviceType = models.IntegerField
    specialization = JSONField()
    version = JSONField()
    property = JSONField()
    owner = models.ForeignKey(Organization, on_delete=models.PROTECT)
    contact = models.ForeignKey(ContactPoint, on_delete=models.PROTECT)
    location = models.CharField(max_length=25)
    url = models.URLField
    note = models.TextField
    safety = models.FilePathField
    manual = models.FilePathField


class LocalTestCode(models.Model):
    loinc_num = models.ForeignKey(Loinc, on_delete=models.PROTECT)
    code = models.CharField(max_length=6)
    type = models.SmallIntegerField
    codeShortText = models.CharField(max_length=20)
    codeLongText = models.CharField(max_length=255, null=True)
    categoryLvl = models.IntegerField(default=0)
    component = JSONField()
    specimenDefinition = models.ForeignKey(SpecimenDefinition, on_delete=models.PROTECT)
    reagent = models.ForeignKey(Reagent, on_delete=models.PROTECT)
    device = models.ForeignKey(Device, on_delete=models.PROTECT)
    referenceRange = models.ForeignKey(ReferenceRange, on_delete=models.PROTECT)
    orderValidation = models.ForeignKey(OrderValidation, on_delete=models.PROTECT)
    unit = models.CharField(max_length=20, blank=True, default='')
    decimalPlaces = models.IntegerField(blank=True, default=0)
    maxDigits = models.IntegerField(blank=True, default=4)
    specimenQuantity = JSONField()
    note = models.TextField(blank=True, default='')

    class Meta:
        indexes = [models.Index(fields=['code', 'codeShortText'])]
        unique_together = [['loinc_num', 'code']]

    def __str__(self):
        return self.code + ' - ' + self.codeShortText










