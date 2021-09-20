#!/usr/bin/env python 3.9
from patients.models import Patient
from subjects.models import Person, PractitionerRole
from testdefinitions.models import TestDef
from services.datefunctions import calculate_current_age


class RequestValidator:
    # test_id = '57021-8'

    def __init__(self, user='45879acd-3266-43bb-b47e-0f3e04bc1d82', patient_id='4c386829-425f-4b4e-965c-33e89a93c05e',
                 location='7A', test_id='57021-8'):
        self.patient_id = patient_id
        self.location = location
        self.test_id = test_id
        self.td = TestDef.objects.get(loinc_num=self.test_id)
        self.user = user
        self.practitioner_roles = PractitionerRole.objects.filter(person__id=self.user)

    def check_authorisation(self, permission='allow', position='roles'):
        """Check if user is authorised to order the test, based on their specialty, role or as an individual"""
        permit_position = self.td.orderValidation[permission][position]
        response = []
        authorisation = 'no'
        # allow/ restrictions for specified role or specialty is defined in TestDef (dictionary not empty)
        if permit_position:
            # Iterate through roles and specialties the user has been assigned to check if it corresponds to the
            # test ordered
            for practitioner_role in self.practitioner_roles:

                if position == 'roles':
                    authorisation = permit_position.get(practitioner_role.role)
                elif position == 'specialties':
                    authorisation = permit_position.get(practitioner_role.id)

                if authorisation == 'yes':
                    response.append('user is authorised to order %s' % self.test_id)
                    break
                elif authorisation == 'cond':
                    response.append('user requires approval to order %s' % self.test_id)
                    break
                else:
                    response.append('sorry, user not allowed to order %s' % self.test_id)
        else:
            # no restrictions specified in TestDef - dictionary is empty
            response.append('Test %s has no restrictions for ordering' % self.test_id)

        print(response)
        return response

    def iterate_authorisation(self):
        positions = ['roles', 'specialties']
        for position in positions:
            self.check_authorisation('allow', position)
        return

    def check_age_restriction(self):
        """Function to check if the test can be ordered for the patients specified age"""

        p = Patient.objects.get(id=self.patient_id)
        age = calculate_current_age(p.birthDate) # patient's age

        permit_age = self.td.orderValidation['allow']['age'] # age restriction by test

        # check minimum age limits
        if age[1] == 'years':
            if permit_age['min'][1] == 'years':
                x = permit_age['min'][0]
            else:
                x = 0
        elif age[1] == 'months':
            if permit_age['min'][1] == 'years':
                x = permit_age['min'][0]*12
            elif permit_age['min'][1] == 'months':
                x = permit_age['min'][0]
            else:
                x = 0
        elif age[1] == 'days':
            if permit_age['min'][1] == 'years':
                x = permit_age['min'][0]*365
            elif permit_age['min'][1] == 'months':
                x = permit_age['min'][0]*30
            else:
                x = permit_age['min'][0]

        # check maximum age limits
        if age[1] == 'years':
            if permit_age['max'][1] == 'years':
                y = permit_age['max'][0]
            else:
                y = 0
        elif age[1] == 'months':
            if permit_age['max'][1] == 'years':
                y = permit_age['max'][0]*12
            elif permit_age['max'][1] == 'months':
                y = permit_age['max'][0]
            else:
                y = 0
        elif age[1] == 'days':
            if permit_age['max'][1] == 'years':
                y = permit_age['max'][0]*365
            elif permit_age['max'][1] == 'months':
                y = permit_age['max'][0]*30
            else:
                y = permit_age['max'][0]

        return x, y, age, permit_age
