#!/usr/bin/env python 3.9
from patients.models import Patient
from services.datefunctions import calculate_current_age


class RequestValid:

    test_id = '57021-8'
    user = ''
    location = ''
    patient_id = '4c386829-425f-4b4e-965c-33e89a93c05e'

    p = Patient.objects.get(id=patient_id)
    age = calculate_current_age(p.birthDate)

    def check_test_request(self, p, age):
        r = {'age': age, 'names': p.names.all()}

        return r

    def check_authorisation(self):
        """Check if user is authorised to order the test, based on their specialty, role or as an individual"""

        return 'ok'
