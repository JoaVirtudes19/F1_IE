# -*- coding: utf-8 -*-
"""
Carga de datos de F1
"""

import numpy as np
import pandas as pd


parent_dir = 'C:/Users/ManuelV/Desktop/Universidad/IE/Trabajo/'

circuits = pd.read_csv(parent_dir+'f1db_csv/circuits.csv', na_values=["\\N"])
constructor_results = pd.read_csv(parent_dir+'f1db_csv/constructor_results.csv', na_values=["\\N"])

constructor_standings = pd.read_csv(parent_dir+'f1db_csv/constructor_standings.csv', na_values=["\\N"])
constructor_standings = constructor_standings.drop(['positionText'], axis=1)

constructors = pd.read_csv(parent_dir+'f1db_csv/constructors.csv', na_values=["\\N"])

driver_standings = pd.read_csv(parent_dir+'f1db_csv/driver_standings.csv', na_values=["\\N"])
driver_standings = driver_standings.drop(['positionText'], axis=1)

drivers = pd.read_csv(parent_dir+'f1db_csv/drivers.csv', na_values=["\\N"], parse_dates=['dob'])
drivers['number'] = drivers['number'].astype('Int64')

lap_times = pd.read_csv(parent_dir+'f1db_csv/lap_times.csv', na_values=["\\N"])
lap_times = lap_times.drop(lap_times.loc[lap_times['time'].str.len()>8].index, axis=0)
lap_times['time'] = pd.to_datetime(lap_times['time'], format='%M:%S.%f').dt.time

pit_stops = pd.read_csv(parent_dir+'f1db_csv/pit_stops.csv', na_values=["\\N"])
pit_stops = pit_stops.drop(pit_stops[pit_stops.duration.str.contains(':')].index, axis=0)
pit_stops['duration'] = pd.to_datetime(pit_stops['duration'], format='%S.%f').dt.time
pit_stops['time'] = pd.to_datetime(pit_stops['time'], format='%H:%M:%S').dt.time

qualifying = pd.read_csv(parent_dir+'f1db_csv/qualifying.csv', na_values=["\\N"])
qualifying['q1'] = pd.to_datetime(qualifying['q1'], format='%M:%S.%f').dt.time
qualifying['q2'] = pd.to_datetime(qualifying['q2'], format='%M:%S.%f').dt.time
qualifying['q3'] = pd.to_datetime(qualifying['q3'], format='%M:%S.%f').dt.time

date_parse_list = ['date', 'fp1_date', 'fp2_date', 'fp3_date', 'quali_date', 'sprint_date']
races = pd.read_csv(parent_dir+'f1db_csv/races.csv', na_values=["\\N"], parse_dates=date_parse_list)
races['time'] = pd.to_datetime(races['time'], format='%H:%M:%S').dt.time
races['fp1_time'] = pd.to_datetime(races['fp1_time'], format='%H:%M:%S').dt.time
races['fp2_time'] = pd.to_datetime(races['fp2_time'], format='%H:%M:%S').dt.time
races['fp3_time'] = pd.to_datetime(races['fp3_time'], format='%H:%M:%S').dt.time
races['quali_time'] = pd.to_datetime(races['quali_time'], format='%H:%M:%S').dt.time
races['sprint_time'] = pd.to_datetime(races['sprint_time'], format='%H:%M:%S').dt.time

results = pd.read_csv(parent_dir+'f1db_csv/results.csv', na_values=["\\N"])
results['number'] = results['number'].astype('Int64')
results['fastestLapTime'] = pd.to_datetime(results['fastestLapTime'], format='%M:%S.%f').dt.time

seasons = pd.read_csv(parent_dir+'f1db_csv/seasons.csv', na_values=["\\N"])

sprint_results = pd.read_csv(parent_dir+'f1db_csv/sprint_results.csv', na_values=["\\N"])
sprint_results['number'] = sprint_results['number'].astype('Int64')
sprint_results['fastestLapTime'] = pd.to_datetime(sprint_results['fastestLapTime'], format='%M:%S.%f').dt.time

status = pd.read_csv(parent_dir+'f1db_csv/status.csv', na_values=["\\N"])

weather_info = pd.read_csv(parent_dir+'f1db_csv/weather.csv')
