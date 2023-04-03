import matplotlib.pyplot as plt
import pandas as pd
from timple.timedelta import strftimedelta
import fastf1
import fastf1.plotting
from fastf1.core import Laps
from datetime import datetime
import requests


request = requests.get('http://ergast.com/api/f1/current/last.json')
data = request.json()
ergast_race = data['MRData']['RaceTable']['Races'][0]
session = fastf1.get_session(int(ergast_race['season']), ergast_race['raceName'], 'R')
session.load()

    ##############################################################################
    # First, we need to get an array of all drivers.

print(session.results)