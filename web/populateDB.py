import fastf1 as ff1
from datetime import datetime
import requests
import pandas as pd
from web.models import Driver,Circuit,Constructor




def populate_drivers():
    Driver.objects.all().delete()
    drivers = pd.read_csv('web/data/drivers.csv', na_values=["\\N"], parse_dates=['dob'])
    drivers['number'] = drivers['number'].astype('Int64')
    objs = [Driver(name=row['forename'] + ' '+ row['surname'], code=row['code'], driver_id=row['driverId']) for index, row in drivers.iterrows()]
    Driver.objects.bulk_create(objs)



def populate_circuits():
    Circuit.objects.all().delete()
    circuits = pd.read_csv('web/data/circuits.csv', na_values=["\\N"])
    objs = [Circuit(name=row['name'], circuit_id=row['circuitId']) for index, row in circuits.iterrows()]
    Circuit.objects.bulk_create(objs)

def populate_constructors():
    Constructor.objects.all().delete()
    constructors = pd.read_csv('web/data/constructors.csv', na_values=["\\N"])
    objs = [Constructor(name=row['name'], constructor_id=row['constructorId']) for index, row in constructors.iterrows()]
    Constructor.objects.bulk_create(objs)
