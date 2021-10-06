#!/usr/bin/env python 3.9

from testdefinitions.models import Loinc, TestDef, TestComposition


def create_profile(profile):
    """ This will create a new test profile from a dictionary that should be passed in from an UI. The format of the
    object is as in the profile argument. Based on the profile the local testdef and testcomposition tables will be
    updated with a many to many recursive relationship.The function returns x that lists the tests descriptions
    that have included in the profile or None if the profile combination already exists"""

    # profile = {
    #     "id": "fbc",
    #     "panel": [{
    #         "id": "57021-8",
    #         "test": ["718-7", "4544-3", "789-8", '787-2', '785-6', '786-4', '21000-5', '788-0']
    #     },
    #     ]
    # }

    profile = profile

    x = []
    loinc = Loinc.objects.all()
    panels = profile['panel']

    for panel in panels:
        p = loinc.get(loinc_num=panel['id'])
        t1, created = TestDef.objects.get_or_create(
            loinc_num=p.loinc_num,
            component=p.component,
            long_common_name=p.long_common_name,
            property=p.property,
            time_aspct=p.time_aspct,
            system=p.system,
            scale_typ=p.scale_typ,
            method_typ=p.method_typ,
            classname=p.classname,
            VersionLastChanged=p.VersionLastChanged,
            status=p.status,
            consumer_name=p.consumer_name,
            class_type=p.class_type,
            formula=p.formula,
            unitsRequired=p.unitsRequired,
            submitted_units=p.submitted_units,
            shortname=p.shortname,
            order_obs=p.order_obs,
            cdisc_common_tests=p.cdisc_common_tests,
            hl7_field_subfield_id=p.hl7_field_subfield_id,
            example_units=p.example_units,
            UnitsAndRange=p.UnitsAndRange,
            example_ucum_units=p.example_ucum_units,
            example_si_ucum_units=p.example_si_ucum_units,
            common_test_rank=p.common_test_rank,
            common_order_rank=p.common_order_rank,
            common_si_test_rank=p.common_si_test_rank,
            hl7_attachment_structure=p.hl7_field_subfield_id,
            PanelType=p.PanelType,
            AskAtOrderEntry=p.AskAtOrderEntry,
            AssociatedObservations=p.AssociatedObservations,
            ValidHL7AttachmentRequest=p.ValidHL7AttachmentRequest,
            DisplayName=p.DisplayName,
        )
        x.append(p.DisplayName)

        for test in panel['test']:
            t = loinc.get(loinc_num=test)
            t2, created = TestDef.objects.get_or_create(
                loinc_num=t.loinc_num,
                component=t.component,
                long_common_name=t.long_common_name,
                property=t.property,
                time_aspct=t.time_aspct,
                system=t.system,
                scale_typ=t.scale_typ,
                method_typ=t.method_typ,
                classname=t.classname,
                VersionLastChanged=t.VersionLastChanged,
                status=t.status,
                consumer_name=t.consumer_name,
                class_type=t.class_type,
                formula=t.formula,
                unitsRequired=t.unitsRequired,
                submitted_units=t.submitted_units,
                shortname=t.shortname,
                order_obs=t.order_obs,
                cdisc_common_tests=t.cdisc_common_tests,
                hl7_field_subfield_id=t.hl7_field_subfield_id,
                example_units=t.example_units,
                UnitsAndRange=t.UnitsAndRange,
                example_ucum_units=t.example_ucum_units,
                example_si_ucum_units=t.example_si_ucum_units,
                common_test_rank=t.common_test_rank,
                common_order_rank=t.common_order_rank,
                common_si_test_rank=t.common_si_test_rank,
                hl7_attachment_structure=t.hl7_field_subfield_id,
                PanelType=t.PanelType,
                AskAtOrderEntry=t.AskAtOrderEntry,
                AssociatedObservations=t.AssociatedObservations,
                ValidHL7AttachmentRequest=t.ValidHL7AttachmentRequest,
                DisplayName=t.DisplayName,
            )

            tc, created = TestComposition.objects.get_or_create(from_test_def=t1, to_test_def=t2)

            if created:
                x.append(t.DisplayName)
            else:
                x.append(None)

    return x


class UpdateJson:
    """This class contains a collection of functions that create, update or delete  json fields in the TestDef table
    based on the loinc code provided."""

    def __init__(self, loinc):
        self.loinc = loinc
        self.td = TestDef.objects.get(loinc_num=self.loinc)

    def add_category(self, key, value='yes', category='roles', permission='allow'):
        """This function takes the argument permission (allow/restrict) for each category (sex, roles, specialties,
        locations) and applies a condition specific (e.g. key = 'doctor'), to that category.
        Default arguments: value='yes' (options: 'yes', 'no', 'cond'), category='roles'(options: 'roles', 'locations',
        'sex', permission='allow' (options: 'allow', 'restrict').
        Function should normally be triggered through the Test Definition UI"""
        self.td.orderValidation[permission][category][key] = value
        self.td.save()

        return self.td.orderValidation[permission][category]

    def add_ageinterval(self, age=999, option='max', text = 'years', permission='allow'):
        """This function takes the argument permission (allow/restrict) for a max/min age interval and applies an age
        criteria specific to it. age should be a positive integer.
        Default arguments: option='max' (options: 'max', 'min'), text='years'(options: 'years', 'months', 'days')
        permission='allow' (options: 'allow', 'restrict').
        Function should normally be triggered through the Test Definition UI"""
        self.td.orderValidation[permission]['age'][option] = [age, text]
        self.td.save()

        return self.td.orderValidation[permission]['age']
