import base64
import io
import urllib.parse

import fastf1
import fastf1.plotting
import fastf1.plotting
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from fastf1.core import Laps
from matplotlib.collections import LineCollection
from timple.timedelta import strftimedelta

mpl.use('Agg')


class ChartFactory:

    @staticmethod
    def generate_table():
        fastf1.Cache.enable_cache('./f1cache')  # replace with your cache directory
        request = requests.get('http://ergast.com/api/f1/current/last.json')
        data = request.json()
        ergast_race = data['MRData']['RaceTable']['Races'][0]
        session = fastf1.get_session(int(ergast_race['season']), ergast_race['raceName'], 'R')
        session.load()
        return [
            {
                'position': int(row['Position']),
                'name': row['FullName'],
                'team': row['TeamName'],
                'status': row['Status'],
                'points': row['Points'],
                'color': row['TeamColor'],
                'code': row['Abbreviation']
            }
            for index, row in session.results.iterrows()
        ]

    @staticmethod
    def generate_times(session_type):
        plt.rcParams["figure.figsize"] = (7, 5)
        fastf1.Cache.enable_cache('./f1cache')  # replace with your cache directory
        fastf1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme=None, misc_mpl_mods=False)

        request = requests.get('http://ergast.com/api/f1/current/last.json')
        data = request.json()
        ergast_race = data['MRData']['RaceTable']['Races'][0]

        session = fastf1.get_session(int(ergast_race['season']), ergast_race['raceName'], session_type)
        session.load()

        drivers = pd.unique(session.laps['Driver'])

        list_fastest_laps = []
        for driver in drivers:
            driver_fastest_lap = session.laps.pick_driver(driver).pick_fastest()
            list_fastest_laps.append(driver_fastest_lap)

        fastest_laps = Laps(list_fastest_laps).sort_values(by='LapTime').reset_index(drop=True)
        fastest_laps = fastest_laps.dropna(axis=0, how='all')

        pole_lap = fastest_laps.pick_fastest()
        fastest_laps['LapTimeDelta'] = fastest_laps['LapTime'] - pole_lap['LapTime']

        team_colors = []
        for index, lap in fastest_laps.iterlaps():
            color = fastf1.plotting.team_color(str(lap['Team']))
            team_colors.append(color)

        fig, ax = plt.subplots()
        ax.barh(fastest_laps.index, fastest_laps['LapTimeDelta'], color=team_colors, edgecolor='grey')
        ax.set_yticks(fastest_laps.index)
        ax.set_yticklabels(fastest_laps['Driver'])
        ax.invert_yaxis()
        ax.set_axisbelow(True)
        ax.xaxis.grid(True, which='major', linestyle='--', color='black', zorder=-1000)

        pole_lap_time_string = strftimedelta(pole_lap['LapTime'], '%m:%s.%ms')

        plt.suptitle(f"{session.event['EventName']} {session.event.year}\n"
                     f"Fastest Lap: {pole_lap_time_string} ({pole_lap['Driver']})")

        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())
        uri = urllib.parse.quote(string)
        plt.close("all")

        return uri

    @staticmethod
    def generate_f1(year, driver, circuit_name):
        fastf1.Cache.enable_cache('./f1cache')

        request = requests.get('http://ergast.com/api/f1/{}/results.json?limit=1000'.format(year))
        data = request.json()
        wknd = int([race['round'] for race in data['MRData']['RaceTable']['Races'] if
                    race['Circuit']['circuitName'] == circuit_name][0])
        session_type = 'R'
        driver_name = driver
        colormap = mpl.cm.plasma

        session = fastf1.get_session(year, wknd, session_type)
        weekend = session.event
        session.load()
        lap = session.laps.pick_driver(driver_name).pick_fastest()

        x = lap.telemetry['X']
        y = lap.telemetry['Y']
        color = lap.telemetry['Speed']
        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)

        fig, ax = plt.subplots(sharex=True, sharey=True, figsize=(12, 6.75))
        fig.suptitle(f'{weekend.name} {year} - {driver_name} - Speed', size=24, y=0.97)

        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.12)
        ax.axis('off')

        ax.plot(lap.telemetry['X'], lap.telemetry['Y'], color='black', linestyle='-', linewidth=16, zorder=0)

        norm = plt.Normalize(color.min(), color.max())
        lc = mpl.collections.LineCollection(segments, cmap=colormap, norm=norm, linestyle='-', linewidth=5)

        lc.set_array(color)

        line = ax.add_collection(lc)

        cbaxes = fig.add_axes([0.25, 0.05, 0.5, 0.05])
        normlegend = mpl.colors.Normalize(vmin=color.min(), vmax=color.max())
        legend = mpl.colorbar.ColorbarBase(cbaxes, norm=normlegend, cmap=colormap, orientation="horizontal")

        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())
        uri = urllib.parse.quote(string)
        plt.close("all")

        return uri

    @staticmethod
    def generate_VS(year, driver1, driver2, circuit_name):
        fastf1.Cache.enable_cache('./f1cache')

        plt.rcParams["figure.figsize"] = (20, 20)

        request = requests.get('http://ergast.com/api/f1/{}/results.json?limit=1000'.format(year))
        data = request.json()
        wknd = int([race['round'] for race in data['MRData']['RaceTable']['Races'] if
                    race['Circuit']['circuitName'] == circuit_name][0])
        session_type = 'R'

        session = fastf1.get_session(year, wknd, session_type)
        session.load()

        driver1_lap = session.laps.pick_driver(driver1).pick_fastest()
        driver2_lap = session.laps.pick_driver(driver2).pick_fastest()

        driver1_tel = driver1_lap.get_car_data().add_distance()
        driver2_tel = driver2_lap.get_car_data().add_distance()

        driver1_color = fastf1.plotting.driver_color(driver1)
        driver2_color = fastf1.plotting.driver_color(driver2)

        fig, (ax0, ax1, ax2, ax3, ax4, ax5) = plt.subplots(nrows=6, sharex=True, layout='constrained')
        """
        ax0 = Speed
        ax1 = Throttle
        ax2 = Brake
        ax3 = Gear
        ax4 = RPM
        ax5 = DRS
        """
        ax0.plot(driver1_tel['Distance'], driver1_tel['Speed'], color=driver1_color, label=driver1)
        ax0.plot(driver2_tel['Distance'], driver2_tel['Speed'], color=driver2_color, label=driver2)
        ax0.set_ylabel('Speed in km/h', fontsize=18)
        ax0.legend()

        ax1.plot(driver1_tel['Distance'], driver1_tel['Throttle'], color=driver1_color, label=driver1)
        ax1.plot(driver2_tel['Distance'], driver2_tel['Throttle'], color=driver2_color, label=driver2)
        ax1.set_ylabel('Throttle %', fontsize=18)

        ax2.plot(driver1_tel['Distance'], driver1_tel['Brake'], color=driver1_color, label=driver1)
        ax2.plot(driver2_tel['Distance'], driver2_tel['Brake'], color=driver2_color, label=driver2)
        ax2.set_ylabel('Brake', fontsize=18)

        ax3.plot(driver1_tel['Distance'], driver1_tel['nGear'], color=driver1_color, label=driver1)
        ax3.plot(driver2_tel['Distance'], driver2_tel['nGear'], color=driver2_color, label=driver2)
        ax3.set_ylabel('Gear', fontsize=18)

        ax4.plot(driver1_tel['Distance'], driver1_tel['RPM'], color=driver1_color, label=driver1)
        ax4.plot(driver2_tel['Distance'], driver2_tel['RPM'], color=driver2_color, label=driver2)
        ax4.set_ylabel('RPM', fontsize=18)

        ax5.plot(driver1_tel['Distance'], driver1_tel['DRS'], color=driver1_color, label=driver1)
        ax5.plot(driver2_tel['Distance'], driver2_tel['DRS'], color=driver2_color, label=driver2)
        ax5.set_xlabel('Distance in m', fontsize=20)
        ax5.set_ylabel('DRS', fontsize=18)

        session_dict = {'FP1': 'Practice 1',
                        'FP2': 'Practice 2',
                        'FP3': 'Practice 3',
                        'Q': 'Qualifying',
                        'S': 'Sprint',
                        'SQ': 'Sprint Qualifying',
                        'R': 'Race'}
        plt.suptitle(f"Fastest Lap Comparison \n "
                     f"{session.event['EventName']} {session.event.year} {session_dict[session_type]}\n"
                     f"{driver1} vs {driver2}",
                     size='xx-large')


        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())
        uri = urllib.parse.quote(string)
        plt.close("all")

        return uri
