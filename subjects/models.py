from django.db import models
from django.utils import timezone
import uuid


# Create your models here.


class Organization(models.Model):
    TYPE = (
        ('prov', 'Healthcare Provider'),
        ('dept', 'Hospital Department'),
        ('team', 'Organizational team'),
        ('govt', 'Government'),
        ('ins', 'Insurance Company'),
        ('pay', 'Payer'),
        ('edu', 'Educational Institute'),
        ('reli', 'Religious Institution'),
        ('crs', 'Clinical Research Sponsor'),
        ('cg', 'Community Group'),
        ('bus', 'Non-Healthcare Business or Corporation'),
        ('other', 'Other'),
    )

    PURPOSE = (
        ('BILL', 'Billing'),
        ('ADMIN', 'Administrative'),
        ('HR', 'Human Resource'),
        ('PAYOR', 'Payor'),
        ('PATINF', 'Patient'),
        ('PRESS', 'Press'),
    )

    ADDRESS_TYPE = (
        ('PO', 'postal'),
        ('PH', 'physical'),
        ('BO', 'both')
    )

    active = models.BooleanField(default=True)
    type = models.CharField(max_length=12, choices=TYPE)
    name = models.CharField(max_length=255)
    purpose = models.CharField(max_length=12, choices=PURPOSE)
    addressType = models.CharField(max_length=2, default='PH', choices=ADDRESS_TYPE)
    text = models.CharField('address', max_length=1000)
    city = models.CharField(max_length=25)
    district = models.CharField(max_length=25, null=True)
    state = models.CharField(max_length=25)
    postalCode = models.CharField('post code', default='00000', max_length=12)
    country = models.CharField(max_length=2, default='MY')
    manager = models.ForeignKey('self', related_name='composition', on_delete=models.PROTECT, null=True)


class PractitionerRole(models.Model):
    ROLE = (
        ('doctor', 'Doctor'),
        ('path', 'Pathologist'),
        ('so', 'Scientific officer'),
        ('mlt', 'Laboratory technologist'),
        ('nurse', 'Nurse'),
        ('pharmacist', 'Pharmacist'),
        ('researcher', 'Researcher'),
        ('teacher', 'Teacher/educator'),
        ('ict', 'ICT professional'),
    )

    SPECIALTY = (
        ('general', 'General'),
        ('cardiology', 'Cardiology'),
        ('primary', 'Primary care'),
    )

    organization = models.ForeignKey(Organization, related_name='organizations', on_delete=models.CASCADE)
    role = models.CharField(max_length=6, choices=ROLE)
    specialty = models.CharField(max_length=12, choices=SPECIALTY)


class Person(models.Model):
    SEX = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('U', 'Unknown'),
    )

    GENDER = (
        ('M', 'Male',),
        ('F', 'Female'),
        ('N', 'Non-binary'),
        ('T', 'Transgendered'),
        ('U', 'Unknown'),
        ('O', 'Others')
    )

    MARITAL_STATUS = (
        ('A', 'Annulled'),
        ('D', 'Divorced'),
        ('I', 'Interlocutary'),
        ('L', 'Legally Separated'),
        ('M', 'Married|'),
        ('P', 'Polygamous'),
        ('N', 'Never Married'),
        ('O', 'Domestic Partner'),
        ('U', 'Unmarried'),
        ('W', 'Widowed'),
        ('U', 'Unknown')
    )

    ETHNICITY = (
        ('ML', 'Malay'),
        ('CH', 'Chinese'),
        ('IN', 'Indian'),
        ('IB', 'Iban'),
        ('KM', 'Kadazan Murut'),
        ('IM', 'West Malaysia indigenous'),
        ('IS', 'Other East Malaysia indigenous'),
        ('EA', 'East Asian'),
        ('HI', 'Hispanic'),
        ('PI', 'Pacific Islander'),
        ('AR', 'Arab'),
        ('PE', 'Persian'),
        ('UN', 'Unspecified')
    )

    RELIGION = (
        ('IS', 'Islam'),
        ('BD', 'Buddhist'),
        ('TA', 'Taoist'),
        ('CH', 'Christian'),
        ('HI', 'Hindu'),
        ('AG', 'Agnostic')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    text = models.CharField('full name', null=True, max_length=120)
    family = models.CharField('family or last name', max_length=60, null=True)
    given = models.CharField('given or first name', max_length=60)
    middle = models.CharField('middle name', max_length=60, null=True, blank=True)
    prefix = models.CharField('salutations or honorifics', max_length=20, null=True, blank=True)
    suffix = models.CharField(max_length=20, null=True, blank=True)
    active = models.BooleanField(default=1)
    sex = models.CharField(max_length=1, choices=SEX)
    gender = models.CharField(max_length=1, choices=GENDER, null=True, blank=True)
    birthDate = models.DateField('date of birth', null=True, blank=True)
    maritalStatus = models.CharField('marital status', max_length=1, choices=MARITAL_STATUS, null=True, blank=True)
    ethnicity = models.CharField(max_length=2, choices=ETHNICITY, null=True, blank=True)
    religion = models.CharField(max_length=2, choices=RELIGION, null=True, blank=True)
    practitioner_role = models.ManyToManyField(PractitionerRole, through='Practitioner', symmetrical=False)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.text


class Practitioner(models.Model):
    person = models.ForeignKey(Person, related_name='practitioners', on_delete=models.CASCADE)
    role = models.ForeignKey(PractitionerRole, related_name='practitioners', on_delete=models.CASCADE)
    startingDate = models.DateField(default=timezone.now)
    terminationDate = models.DateField(null=True, blank=True)


class Qualification(models.Model):
    code = models.CharField(max_length=5)
    issuer = models.CharField(max_length=20)
    startingDate = models.DateField()
    terminationDate = models.DateField(null=True, blank=True)
    qualification = models.ForeignKey(Person, related_name='qualifications', on_delete=models.CASCADE)


class Identification(models.Model):
    ID_TYPE = (
        ('NR', 'National registration id'),
        ('PP', 'Passport id'),
        ('MC', 'Medicaid card'),
        ('HR', 'Hospital registration number'),
        ('SB', 'US Social Security Number'),
        ('PRN', 'US National Provider Identifier')
    )

    idValue = models.CharField(max_length=30)
    idType = models.CharField(max_length=5, choices=ID_TYPE)
    person = models.ForeignKey(Person, related_name='identifications', on_delete=models.CASCADE)

    def __str__(self):
        return self.idValue


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
    text = models.CharField('address', max_length=1000)
    city = models.CharField(max_length=25)
    district = models.CharField(max_length=25, null=True)
    state = models.CharField(max_length=25)
    postalCode = models.CharField('post code', default='00000', max_length=12)
    country = models.CharField(max_length=2, default='MY')
    person = models.ForeignKey(Person, related_name='addresses', on_delete=models.CASCADE)


class Communication(models.Model):
    language = models.CharField(max_length=3)
    preferred = models.BooleanField(default=0)
    person = models.ForeignKey(Person, related_name='communications', on_delete=models.CASCADE)


class ContactPoint(models.Model):
    CONTACT_POINT_SYS = (
        ('phone', 'phone'),
        ('mobile', 'mobile'),
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
        ('P', 'personal')
    )

    system = models.CharField(max_length=12, choices=CONTACT_POINT_SYS)
    value = models.CharField(max_length=255)
    use = models.CharField(max_length=1, choices=SYS_USE)
    rank = models.PositiveSmallIntegerField()
    person = models.ForeignKey(Person, related_name='contactpoints', on_delete=models.CASCADE)


class OrganizationContactPoint(models.Model):
    CONTACT_POINT_SYS = (
        ('phone', 'phone'),
        ('fax', 'fax'),
        ('email', 'E-mail'),
        ('url', 'url'),
        ('sms', 'sms')
    )

    SYS_USE = (
        ('T', 'temporary'),
        ('O', 'old'),
        ('B', 'billing'),
        ('E', 'enquiry'),
    )

    system = models.CharField(max_length=5, choices=CONTACT_POINT_SYS)
    value = models.CharField(max_length=255)
    use = models.CharField(max_length=1, choices=SYS_USE, default='E')
    organization = models.ForeignKey(Organization, related_name='organization_contact_points', on_delete=models.CASCADE)