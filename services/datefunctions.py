#!/usr/bin/env python 3.9

import datetime


def calculate_current_age(dob):
    """This function calculates current age based on the current date. Returns age in years if more than 1 year old,
    in months if 1 to 12 months, and in days if less than 30 days. Returns none if invalid date provided. dob must be
    provided as a datetime argument"""
    today = datetime.date.today()
    year = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

    age = (0, 'none')

    if year > 0:
        age = (year, 'years')
    elif year == 0:
        delta = today - dob
        month = int((delta.days/30))
        if month > 0:
            age = (month, 'months')
        else:
            age = (delta.days, 'days')
    else:
        pass

    return age
