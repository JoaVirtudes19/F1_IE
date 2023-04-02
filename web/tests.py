#from django.test import TestCase

import pandas as pd




drivers = pd.read_csv('web/data/drivers.csv', na_values=["\\N"], parse_dates=['dob'])
drivers['number'] = drivers['number'].astype('Int64')
print(drivers)