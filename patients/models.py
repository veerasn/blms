from django.db import models
import uuid
from subjects.models import Person, Organization

# Create your models here.


class Patient(models.Model):
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
    sex = models.CharField(max_length=1, choices=SEX)
    gender = models.CharField(max_length=1, choices=GENDER, null=True, blank=True)
    birthDate = models.DateField('date of birth')
    deceasedDate = models.DateField('deceased date', null=True, blank=True)
    maritalStatus = models.CharField('marital status', max_length=1, choices=MARITAL_STATUS, null=True, blank=True)
    ethnicity = models.CharField(max_length=2, choices=ETHNICITY, null=True, blank=True)
    religion = models.CharField(max_length=2, choices=RELIGION, null=True, blank=True)

    class Meta:
        ordering = ['created']


class Name(models.Model):
    NAME_USE = (
        ('US', 'usual'),
        ('OF', 'official'),
        ('TM', 'temporary'),
        ('NN', 'nickname'),
        ('AN', 'anonymous'),
        ('OL', 'old'),
        ('MA', 'maiden')
    )

    created = models.DateTimeField(auto_now_add=True)
    text = models.CharField('full name', max_length=100, db_index=True)
    family = models.CharField('family or last name', max_length=60, null=True, blank=True)
    given = models.CharField('given or first name', max_length=60, null=True, blank=True)
    middle = models.CharField('middle name', max_length=60, null=True, blank=True)
    prefix = models.CharField('salutations or honorifics', max_length=20, null=True, blank=True)
    suffix = models.CharField(max_length=20, null=True, blank=True)
    use = models.CharField(max_length=2, default='US', choices=NAME_USE)
    active = models.BooleanField(default=1)
    patient = models.ForeignKey(Patient, related_name='names', on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Identification(models.Model):
    ID_TYPE = (
        ('NR', 'National registration id'),
        ('PP', 'Passport id'),
        ('MC', 'Medicaid card'),
        ('HR', 'Hospital registration number')
    )

    idValue = models.CharField(max_length=30)
    idType = models.CharField(max_length=5, choices=ID_TYPE)
    patient = models.ForeignKey(Patient, related_name='identifications', on_delete=models.CASCADE)

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
    patient = models.ForeignKey(Patient, related_name='addresses', on_delete=models.CASCADE)


class Communication(models.Model):
    language = models.CharField(max_length=3)
    preferred = models.BooleanField(default=0)
    patient = models.ForeignKey(Patient, related_name='communications', on_delete=models.CASCADE)


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
    patient = models.ForeignKey(Patient, related_name='contactpoints', on_delete=models.CASCADE)


class Contact(models.Model):
    patient = models.ManyToManyField(Patient, related_name='patient_contacts')
    person = models.ForeignKey(Person, related_name='persons_contacts', on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, related_name='organization_contacts', on_delete=models.CASCADE, null=True)



