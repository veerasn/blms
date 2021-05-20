from django.db import models
from djongo import models
import uuid
from django.core.exceptions import ValidationError

# Create your models here.
NAME_USE = (
    ('US', 'usual'),
    ('OF', 'official'),
    ('TM', 'temporary'),
    ('NN', 'nickname'),
    ('AN', 'anonymous'),
    ('OL', 'old'),
    ('MA', 'maiden')
)

ID_TYPE = (
    ('NR', 'National registration id'),
    ('PP', 'Passport id'),
    ('MC', 'Medicaid card'),
    ('HR', 'Hospital registration number')
)

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


class HumanName(models.Model):
    text = models.CharField('full name', max_length=100)
    family = models.CharField('family or last name', max_length=60, null=True)
    given = models.CharField('given or first name', max_length=60, null=True)
    middle = models.CharField('middle name', max_length=60, null=True)
    prefix = models.CharField('salutations or honorifics', max_length=20, null=True)
    suffix = models.CharField(max_length=20, null=True)
    use = models.CharField(max_length=2, choices=NAME_USE)

    class Meta:
        abstract = True

    def __str__(self):
        return self.text


class Identification(models.Model):
    idValue = models.CharField(max_length=30)
    idType = models.CharField(max_length=5, choices=ID_TYPE)

    class Meta:
        abstract = True

    def __str__(self):
        return self.idValue


class Address(models.Model):
    use = models.CharField(max_length=1, choices=ADDRESS_USE)
    type = models.CharField(max_length=2, choices=ADDRESS_TYPE)
    text = models.CharField('address', max_length=255)
    city = models.CharField(max_length=5)
    district = models.CharField(max_length=5)
    state = models.CharField(max_length=5)
    postalCode = models.CharField('post code', max_length=5)
    country = models.CharField(max_length=2, default='MY')

    class Meta:
        abstract = True


class Metadata(models.Model):
    author = models.CharField()
    pub_date = models.DateTimeField()
    mod_date = models.DateField()

    class Meta:
        abstract = True


class Person(models.Model):
    _id = models.ObjectIdField()
    humanname = models.EmbeddedField(model_container=HumanName)
    address = models.EmbeddedField(model_container=Address)
    active = models.BooleanField(default=1)
    sex = models.CharField(max_length=1, choices=SEX)
    gender = models.CharField(max_length=1, choices=GENDER)
    birthDate = models.DateField('date of birth')
    deceasedDate = models.DateField('deceased date', null=True)
    maritalStatus = models.CharField('marital status', max_length=1, choices=MARITAL_STATUS)
    ethnicity = models.CharField(max_length=2, choices=ETHNICITY)
    religion = models.CharField(max_length=2, choices=RELIGION)
    metadata = models.EmbeddedField(model_container=Metadata, null=True)
