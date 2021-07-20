#!/usr/bin/env python 3.9

from testdefs.models import Loinc, TestDef, TestComposition


def create_profile():
    """ This will create a new test profile from a dictionary that should be passed in from an UI. The format of the
    object is as in the profile argument. Based on the profile the local testdef and testcomposition tables will be
    updated with a many to many recursive relationship.The function returns x that lists the tests descriptions
    that have included in the profile"""

    profile = {
        "id": "fbc",
        "panel": [{
            "id": "57021-8",
            "test": ["718-7", "4544-3", "789-8", '787-2', '785-6', '786-4']
        },
        ]
    }

    x = []
    loinc = Loinc.objects.all()
    panels = profile['panel']

    for panel in panels:
        p = loinc.get(loinc_num=panel['id'])
        t1 = TestDef(loinc_num=p.loinc_num, component=p.component, long_common_name=p.long_common_name)
        t1.save()
        x.append(p.DisplayName)

        for test in panel['test']:
            t = loinc.get(loinc_num=test)
            t2 = TestDef(loinc_num=t.loinc_num, component=t.component, long_common_name=t.long_common_name)
            t2.save()

            tc = TestComposition(from_test_def=t1, to_test_def=t2)
            tc.save()

            x.append(t.DisplayName)

    return x
