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

    def __str__(self):
        return self.loinc_num + ' - ' + self.shortname


class TestComposition(models.Model):
    from_test_def = models.ForeignKey(TestDef, related_name='from_test_defs', on_delete=models.PROTECT)
    to_test_def = models.ForeignKey(TestDef, related_name='to_test_defs', on_delete=models.PROTECT)
    primaryTest = models.BooleanField(default=True)
    orderable = models.BooleanField(default=False)

    class Meta:
        unique_together = ('from_test_def', 'to_test_def')


class Specimen(models.Model):
    TYPE = (
        ('Aspirate', 'Aspirate'),
        ('Blood', 'Blood'),
        ('Body submitted for autopsy', 'Body submitted for autopsy'),
        ('Bone marrow', 'Bone marrow'),
        ('Condition', 'Condition'),
        ('Condition, Fluid/Tissue', 'Condition, Fluid/Tissue'),
        ('Conditions', 'Conditions'),
        ('Device', 'Device'),
        ('Environment', 'Environment'),
        ('Fluid', 'Fluid'),
        ('Fluid/Secretion', 'Fluid/Secretion'),
        ('Fluid/Tissue', 'Fluid/Tissue'),
        ('Food specimen', 'Food specimen'),
        ('Forensic and possibly chemistry testing', 'Forensic and possibly chemistry testing'),
        ('Gas', 'Gas'),
        ('Lavage', 'Lavage'),
        ('Milk specimen','Milk specimen'),
        ('Object', 'Object'),
        ('Others', 'Others'),
        ('Product', 'Product'),
        ('Site', 'Site'),
        ('Sputum', 'Sputum'),
        ('Stool', 'Stool'),
        ('Tissue', 'Tissue'),
        ('Transfusion', 'Transfusion'),
        ('Urine', 'Urine'),
    )

    type = models.CharField(max_length=45, choices=TYPE)  # type of sample e.g. blood, tissue
    code = models.CharField(max_length=8, unique=True)
    display = models.CharField(max_length=45)
    patientPreparation = models.TextField(null=True)  # patient preparation instructions for collection
    collectionProcedure = models.TextField(null=True)  # specimen collection procedure
    requirement = models.TextField(null=True)
    rejectionCriterion = JSONField(default=dict, null=True)
    handling = JSONField(default=dict, null=True)
    typesTested = models.ManyToManyField(TestDef, through='TypeTested', through_fields=('specimen', 'testDef'))
    isDerived = models.ForeignKey('self', null=True, on_delete=models.CASCADE)  # primary or secondary specimen


class TypeTested(models.Model):
    PREFERENCE = (
        ('preferred', 'Preferred'),
        ('alternative', 'Alternative'),
    )

    testDef = models.ForeignKey(TestDef, on_delete=models.CASCADE)
    specimen = models.ForeignKey(Specimen, on_delete=models.CASCADE)
    site = models.CharField(max_length=12, null=True)
    procedure = models.CharField(max_length=12, null=True)
    preference = models.CharField(max_length=15, choices=PREFERENCE, null=True)
    retentionTime = JSONField(default=dict)

    class Meta:
        unique_together = ('testDef', 'specimen')


class SpecimenContainer(models.Model):
    MATERIAL = (
        ('glass', 'Glass'),
        ('metal', 'Metal'),
        ('plastic', 'Plastic'),
        ('na', 'not applicable'),
    )

    TYPE = (
        ('Acid Citrate Dextrose (ACD) ', 'Acid Citrate Dextrose (ACD) '),
        ('BD BBL CultureSwab EZ', 'BD BBL CultureSwab EZ'),
        ('BD CultureSwab Plus system', 'BD CultureSwab Plus system'),
        ('BD CultureSwab system', 'BD CultureSwab system'),
        ('Blood Culture', 'Blood Culture'),
        ('Citrate tubes ', 'Citrate tubes '),
        ('CultureSwab system', 'CultureSwab system'),
        ('EDTA tubes ', 'EDTA tubes '),
        ('Fluoride tubes ', 'Fluoride tubes '),
        ('Fluoride tubes for blood alcohol testing ', 'Fluoride tubes for blood alcohol testing '),
        ('Heparin tubes ', 'Heparin tubes '),
        ('Lead testing tubes ', 'Lead testing tubes '),
        ('Microtainer', 'Microtainer'),
        ('No additive tube for discard', 'No additive tube for discard'),
        ('PST tubes ', 'PST tubes '),
        ('RST tube ', 'RST tube '),
        ('Sedimentation Rate Determination (SRD) ', 'Sedimentation Rate Determination (SRD) '),
        ('Serum tubes ', 'Serum tubes '),
        ('Sodium citrate tubes ', 'Sodium citrate tubes '),
        ('Sodium Polyanetholesulfonate (SPS) ', 'Sodium Polyanetholesulfonate (SPS) '),
        ('SST tubes ', 'SST tubes '),
        ('Sterile exterior pouch', 'Sterile exterior pouch'),
        ('Swab', 'Swab'),
        ('Trace element ', 'Trace element '),
        ('Urine container', 'Urine container'),
        ('Viral Transport', 'Viral Transport'),
    )

    CAP = (
        ('Black/H', 'Black-Hemogard'),
        ('Clear/H', 'Clear-Hemogard'),
        ('Clear/Red/H', 'Clear/Red-Hemogard'),
        ('Gold', 'Gold'),
        ('Gold/H', 'Gold-Hemogard'),
        ('Gray/C', 'Gray-Conventional'),
        ('Gray/H', 'Gray-Hemogard'),
        ('Green', 'Green'),
        ('Green-Gray/C', 'Green-Gray-Conventional'),
        ('Green/C', 'Green-Conventional'),
        ('Green/H', 'Green-Hemogard'),
        ('Grey', 'Grey'),
        ('Lavender', 'Lavender'),
        ('Lavender/C', 'Lavender-Conventional'),
        ('Lavender/H', 'Lavender-Hemogard'),
        ('Light blue/H', 'Light blue-Hemogard'),
        ('Light gray/H', 'Light gray-Hemogard'),
        ('Light green/H', 'Light green-Hemogard'),
        ('Mint green', 'Mint green'),
        ('na', 'not applicable'),
        ('Orange/H', 'Orange-Hemogard'),
        ('Pink/C', 'Pink-Conventional'),
        ('Pink/H', 'Pink-Hemogard'),
        ('Red', 'Red'),
        ('Red-Gray/C', 'Red-Gray-Conventional'),
        ('Red-Light Gray/C', 'Red-Light Gray-Conventional'),
        ('Red-silicon coated/Lavender-K3 EDTA/C', 'Red-silicon coated/Lavender-K3 EDTA-Conventional'),
        ('Red/C', 'Red-Conventional'),
        ('Red/H', 'Red-Hemogard'),
        ('Red/Yellow/C', 'Red/Yellow-Conventional'),
        ('Royal Blue', 'Royal Blue'),
        ('Tan/H', 'Tan-Hemogard'),
        ('Yellow/C', 'Yellow-Conventional'),
        ('Yellow/H', 'Yellow-Hemogard'),
    )

    ADDITIVE = (
        ('acid citrate dextrose', 'acid citrate dextrose'),
        ('Boric acid, sodium formate and sodium borate preservative',
         'Boric acid, sodium formate and sodium borate preservative'),
        ('Ethylparaben, sodium propionate and chlorhexidine preservative',
         'Ethylparaben, sodium propionate and chlorhexidine preservative'),
        ('K2EDTA', 'K2EDTA'),
        ('K3EDTA', 'K3EDTA'),
        ('lithium heparin', 'lithium heparin'),
        ('na', 'na'),
        ('NaFl/Na2EDTA', 'NaFl/Na2EDTA'),
        ('No additive', 'No additive'),
        ('sodium citrate', 'sodium citrate'),
        ('sodium fluoride', 'sodium fluoride'),
        ('sodium fluoride, Na2EDTA', 'sodium fluoride, Na2EDTA'),
        ('sodium fluoride, potassium oxalate', 'sodium fluoride, potassium oxalate'),
        ('sodium heparin', 'sodium heparin'),
        ('sodium polyanetholesulfonate', 'sodium polyanetholesulfonate'),
    )

    code = models.CharField(max_length=25)
    material = models.CharField(max_length=12, choices=MATERIAL, default='na')
    description = models.TextField(max_length=300)
    type = models.TextField(max_length=60, choices=TYPE)
    cap = models.CharField(max_length=60, choices=CAP, default='na')
    dimension = JSONField(default=dict)
    volume = JSONField(default=dict)
    age = JSONField(default=dict)
    additive = models.CharField(max_length=80, default='na')
    note = models.TextField(null=True)
    specimen = models.ManyToManyField(Specimen)

    class Meta:
        indexes = [models.Index(fields=['code'])]


# class DeviceLookup(models.Model):
#     STATUS = (
#         ('active', 'Active'),
#         ('inactive', 'Inactive'),
#         ('entered-in-error', 'Entered in error'),
#         ('unknown', 'Unknown')
#     )
#
#     REASON = (
#         ('online', 'Active'),
#         ('paused', 'Inactive'),
#         ('standby', 'Entered in error'),
#         ('offline', 'Offline'),
#         ('not-ready', 'Not ready'),
#         ('hw-disconnect', 'Hardware disconnected'),
#         ('maintenance', 'Maintenance ongoing'),
#         ('off', 'Off'),
#     )
#
#     udiCarrier = JSONField()
#     status = models.CharField(max_length=25, choices=STATUS, default='active')
#     statusReason = models.CharField(max_length=25, choices=REASON, default='online')
#     distinctIdentifier = models.CharField(max_length=50)
#     manufacturer = models.CharField(max_length=25)
#     manufactureDate = models.DateField()
#     expirationDate = models.DateField()
#     lotNumber = models.CharField(max_length=50)
#     serialNumber = models.CharField(max_length=50)
#     deviceName = models.CharField(max_length=50)
#     modelNumber = models.CharField(max_length=50)
#     partNumber = models.CharField(max_length=50, blank=True, default='')
#     deviceType = models.IntegerField()
#     specialization = JSONField()
#     version = JSONField()
#     property = JSONField()
#     owner = models.ForeignKey(Organization, on_delete=models.PROTECT)
#     contact = models.ForeignKey(ContactPoint, on_delete=models.PROTECT)
#     location = models.CharField(max_length=25)
#     url = models.URLField()
#     note = models.TextField()
#     safety = models.FilePathField()
#     manual = models.FilePathField()
#     tests = models.ManyToManyField(TestDef, through='DeviceTest', through_fields=('device', 'test'))


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
    tests = models.ManyToManyField(TestDef, through='DeviceTest', through_fields=('device', 'test'))


class DeviceTest(models.Model):
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

    device = models.ForeignKey(Device, related_name='devices', on_delete=models.CASCADE)
    test = models.ForeignKey(TestDef, related_name='tests', on_delete=models.CASCADE)
    status = models.CharField(max_length=25, choices=STATUS, default='active')
    statusReason = models.CharField(max_length=25, choices=REASON, default='online')


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
    unitPerTest = models.IntegerField()
    device = models.ManyToManyField(Device)


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
    reagent = models.ForeignKey(Reagent, related_name='reagent_lots', on_delete=models.CASCADE)