from django.db import models
from django.contrib.postgres.fields import JSONField
from subjects.models import Organization, ContactPoint


class SourceOrganization(models.Model):
    copyright_id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    copyright = models.TextField()
    terms_of_use = models.TextField()
    url = models.TextField()


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
    class_type = models.IntegerField()
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
    common_test_rank = models.IntegerField()
    common_order_rank = models.IntegerField()
    common_si_test_rank = models.IntegerField()
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


class TestDef(models.Model):
    loinc_num = models.CharField(max_length=10, primary_key=True)
    component = models.CharField(max_length=255)
    property = models.CharField(max_length=64, null=True)
    time_aspct = models.CharField(max_length=32)
    system = models.CharField(max_length=255)
    scale_typ = models.CharField(max_length=8)
    method_typ = models.CharField(max_length=64, null=True)
    classname = models.CharField(max_length=32)
    VersionLastChanged = models.CharField(max_length=8)
    status = models.CharField(max_length=12)
    consumer_name = models.CharField(max_length=255)
    class_type = models.IntegerField()
    formula = models.CharField(max_length=512, null=True)
    unitsRequired = models.CharField(max_length=1)
    submitted_units = models.CharField(max_length=32, null=True)
    shortname = models.CharField(max_length=128)
    order_obs = models.CharField(max_length=12)
    cdisc_common_tests = models.CharField(max_length=1, null=True)
    hl7_field_subfield_id = models.CharField(max_length=16, null=True)
    example_units = models.CharField(max_length=128, null=True)
    long_common_name = models.CharField(max_length=255)
    UnitsAndRange = models.CharField(max_length=32, null=True)
    example_ucum_units = models.CharField(max_length=40, null=True)
    example_si_ucum_units = models.CharField(max_length=40, null=True)
    common_test_rank = models.IntegerField()
    common_order_rank = models.IntegerField()
    common_si_test_rank = models.IntegerField()
    hl7_attachment_structure = models.CharField(max_length=15, null=True)
    PanelType = models.CharField(max_length=25, null=True)
    AskAtOrderEntry = models.CharField(max_length=16, null=True)
    AssociatedObservations = models.CharField(max_length=64, null=True)
    ValidHL7AttachmentRequest = models.CharField(max_length=1, null=True)
    DisplayName = models.CharField(max_length=255)
    referenceRange = JSONField(null=True)
    orderValidation = JSONField(null=True)
    decimalPlaces = models.IntegerField(null=True, default=0)
    maxDigits = models.IntegerField(null=True)
    specimenQuantity = JSONField(null=True)
    composition = models.ManyToManyField('self', through='TestComposition', symmetrical=False)


class TestComposition(models.Model):
    from_test_def = models.ForeignKey(TestDef, related_name='from_test_defs', on_delete=models.PROTECT)
    to_test_def = models.ForeignKey(TestDef, related_name='to_test_defs', on_delete=models.PROTECT)
    primaryTest = models.BooleanField(default=True)
    orderable = models.BooleanField(default=False)

    class Meta:
        unique_together = ('from_test_def', 'to_test_def')


class TypeTested(models.Model):
    PREFERENCE = (
        ('preferred', 'Preferred'),
        ('alternative', 'Alternative'),
    )

    isDerived = models.BooleanField(default=False)  # primary or secondary specimen
    type = models.CharField(max_length=8)  # type of sample e.g. serum, whole blood
    preference = models.CharField(max_length=15, choices=PREFERENCE)
    patientPreparation = models.TextField(null=True)  # patient preparation instructions for collection
    collectionProcedure = models.TextField(null=True)  # specimen collection procedure
    requirement = models.TextField()
    retentionTime = JSONField()
    rejectionCriterion = JSONField()
    handling = JSONField()
    test = models.ForeignKey(TestDef, related_name='types_tested', on_delete=models.CASCADE)


class SpecimenContainerLookup(models.Model):
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

    code = models.CharField(max_length=12)
    material = models.CharField(max_length=12, choices=MATERIAL)
    description = models.TextField(max_length=255)
    type = models.TextField(max_length=255)
    cap = models.CharField(max_length=25, choices=CAP, default='')
    capacity = models.PositiveIntegerField
    minimumVolume = JSONField()
    age = JSONField()
    note = models.TextField(blank=True, default='')

    class Meta:
        indexes = [models.Index(fields=['code'])]


class Additive(models.Model):
    code = models.CharField(primary_key=True, max_length=6)
    display = models.CharField(max_length=255)
    comment = models.CharField(max_length=255)
    specimen_container = models.ForeignKey(SpecimenContainerLookup, related_name='additives', on_delete=models.CASCADE)

    def __str__(self):
        return 'Additive(%s, %s)' % (self.code, self.display)


class SpecimenContainer(models.Model):
    specimenContainer = models.ForeignKey(SpecimenContainerLookup, on_delete=models.PROTECT)
    typeTested = models.ForeignKey(TypeTested, related_name='specimen_containers', on_delete=models.CASCADE)


class DeviceLookup(models.Model):
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
        ('maintenance', 'Maintenance ongoing'),
        ('off', 'Off'),
    )

    udiCarrier = JSONField()
    status = models.CharField(max_length=25, choices=STATUS, default='active')
    statusReason = models.CharField(max_length=25, choices=REASON, default='online')
    distinctIdentifier = models.CharField(max_length=50)
    manufacturer = models.CharField(max_length=25)
    manufactureDate = models.DateField()
    expirationDate = models.DateField()
    lotNumber = models.CharField(max_length=50)
    serialNumber = models.CharField(max_length=50)
    deviceName = models.CharField(max_length=50)
    modelNumber = models.CharField(max_length=50)
    partNumber = models.CharField(max_length=50, blank=True, default='')
    deviceType = models.IntegerField()
    specialization = JSONField()
    version = JSONField()
    property = JSONField()
    owner = models.ForeignKey(Organization, on_delete=models.PROTECT)
    contact = models.ForeignKey(ContactPoint, on_delete=models.PROTECT)
    location = models.CharField(max_length=25)
    url = models.URLField()
    note = models.TextField()
    safety = models.FilePathField()
    manual = models.FilePathField()


class ReagentLookup(models.Model):
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
    unitPerTest = models.IntegerField()
    device = models.ForeignKey(DeviceLookup, related_name='reagents', on_delete=models.CASCADE)


class ReagentLot(models.Model):
    REASON = (
        ('obsolete', 'Obsolete'),
        ('defective', 'Defective'),
        ('verify', 'Pending verification'),
        ('in-use', 'In use'),
    )

    status = models.BooleanField(default=True)
    statusReason = models.CharField(max_length=20, choices=REASON, default='in-use')
    manufactureDate = models.DateField
    expirationDate = models.DateField
    lotNumber = models.CharField(max_length=30)
    totalUnit = models.IntegerField()
    location = JSONField()
    note = models.TextField()
    safety = models.FilePathField()
    manual = models.FilePathField()
    reagent = models.ForeignKey(ReagentLookup, related_name='reagent_lots', on_delete=models.CASCADE)


class Device(models.Model):
    device = models.ForeignKey(DeviceLookup, on_delete=models.PROTECT)
    test = models.ForeignKey(TestDef, related_name='devices', on_delete=models.CASCADE)
