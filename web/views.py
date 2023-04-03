from django.shortcuts import render, HttpResponseRedirect
import matplotlib.pyplot as plt
import matplotlib as mpl
import io
import urllib, base64
mpl.use('Agg')
import fastf1
import fastf1.plotting
import numpy as np
from matplotlib.collections import LineCollection
from web.populateDB import populate_drivers, populate_circuits
from web.forms import DriverCircuitYear
import requests
from datetime import datetime
import pandas as pd
from fastf1.core import Laps
from timple.timedelta import strftimedelta

# Create your views here.


def generarTabla():
    request = requests.get('http://ergast.com/api/f1/current/last.json')
    data = request.json()
    ergast_race = data['MRData']['RaceTable']['Races'][0]
    session = fastf1.get_session(int(ergast_race['season']), ergast_race['raceName'], 'R')
    session.load()
    return [{'position': int(row['Position']),'name':row['FullName'],'team':row['TeamName'],'status':row['Status'],'points':row['Points'],'color':row['TeamColor'],'code':row['Abbreviation']} for index,row in session.results.iterrows()]

def generarTiempos(sesion):
    fastf1.Cache.enable_cache('./f1cache')  # replace with your cache directory
    fastf1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme=None, misc_mpl_mods=False)
    request = requests.get('http://ergast.com/api/f1/current/last.json')
    data = request.json()
    ergast_race = data['MRData']['RaceTable']['Races'][0]
    session = fastf1.get_session(int(ergast_race['season']), ergast_race['raceName'], sesion)
    session.load()

    ##############################################################################
    # First, we need to get an array of all drivers.

    drivers = pd.unique(session.laps['Driver'])


    ##############################################################################
    # After that we'll get each drivers fastest lap, create a new laps object
    # from these laps, sort them by lap time and have pandas reindex them to
    # number them nicely by starting position.

    list_fastest_laps = list()
    for drv in drivers:
        drvs_fastest_lap = session.laps.pick_driver(drv).pick_fastest()
        list_fastest_laps.append(drvs_fastest_lap)
    fastest_laps = Laps(list_fastest_laps).sort_values(by='LapTime').reset_index(drop=True)
    fastest_laps = fastest_laps.dropna(axis=0, how='all')


    ##############################################################################
    # The plot is nicer to look at and more easily understandable if we just plot
    # the time differences. Therefore we subtract the fastest lap time from all
    # other lap times.

    pole_lap = fastest_laps.pick_fastest()
    fastest_laps['LapTimeDelta'] = fastest_laps['LapTime'] - pole_lap['LapTime']


    ##############################################################################
    # We can take a quick look at the laps we have to check if everything
    # looks all right. For this, we'll just check the 'Driver', 'LapTime'
    # and 'LapTimeDelta' columns.

    print(fastest_laps[['Driver', 'LapTime', 'LapTimeDelta']])


    ##############################################################################
    # Finally, we'll create a list of team colors per lap to color our plot.
    team_colors = list()
    for index, lap in fastest_laps.iterlaps():
        color = fastf1.plotting.team_color(str(lap['Team']))
        team_colors.append(color)


    ##############################################################################
    # Now, we can plot all the data
    fig, ax = plt.subplots()
    ax.barh(fastest_laps.index, fastest_laps['LapTimeDelta'],
            color=team_colors,edgecolor='grey')
    ax.set_yticks(fastest_laps.index)
    ax.set_yticklabels(fastest_laps['Driver'])

    # show fastest at the top
    ax.invert_yaxis()

    # draw vertical lines behind the bars
    ax.set_axisbelow(True)
    ax.xaxis.grid(True, which='major', linestyle='--', color='black', zorder=-1000)
    # sphinx_gallery_defer_figures


    ##############################################################################
    # Finally, give the plot a meaningful title

    lap_time_string = strftimedelta(pole_lap['LapTime'], '%m:%s.%ms')

    plt.suptitle(f"{session.event['EventName']} {session.event.year}\n"
                f"Fastest Lap: {lap_time_string} ({pole_lap['Driver']})")
    
        # Show the plot
    buf = io.BytesIO()
    fig.savefig(buf,format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    plt.close("all")

    return uri


def generarF1(year,driver,circuit_name):
    fastf1.Cache.enable_cache('./f1cache')  # replace with your cache directory
    request = requests.get('http://ergast.com/api/f1/{}/results.json?limit=1000'.format(year))
    data = request.json()
    wknd = int([ race['round'] for race in data['MRData']['RaceTable']['Races'] if race['Circuit']['circuitName'] == circuit_name][0])
    ses = 'R'
    driver = driver
    colormap = mpl.cm.plasma
    session = fastf1.get_session(year, wknd, ses)
    weekend = session.event
    session.load()
    lap = session.laps.pick_driver(driver).pick_fastest()

    # Get telemetry data
    x = lap.telemetry['X']              # values for x-axis
    y = lap.telemetry['Y']              # values for y-axis
    color = lap.telemetry['Speed']     
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    # We create a plot with title and adjust some setting to make it look good.
    fig, ax = plt.subplots(sharex=True, sharey=True, figsize=(12, 6.75))
    fig.suptitle(f'{weekend.name} {year} - {driver} - Speed', size=24, y=0.97)

    # Adjust margins and turn of axis
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.12)
    ax.axis('off')


    # After this, we plot the data itself.
    # Create background track line
    ax.plot(lap.telemetry['X'], lap.telemetry['Y'], color='black', linestyle='-', linewidth=16, zorder=0)

    # Create a continuous norm to map from data points to colors
    norm = plt.Normalize(color.min(), color.max())
    lc = LineCollection(segments, cmap=colormap, norm=norm, linestyle='-', linewidth=5)

    # Set the values used for colormapping
    lc.set_array(color)

    # Merge all line segments together
    line = ax.add_collection(lc)


    # Finally, we create a color bar as a legend.
    cbaxes = fig.add_axes([0.25, 0.05, 0.5, 0.05])
    normlegend = mpl.colors.Normalize(vmin=color.min(), vmax=color.max())
    legend = mpl.colorbar.ColorbarBase(cbaxes, norm=normlegend, cmap=colormap, orientation="horizontal")


    # Show the plot
    buf = io.BytesIO()
    fig.savefig(buf,format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    plt.close("all")

    return uri

def generar(n,title):
    plt.plot(range(n))
    plt.title(title)
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf,format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    plt.close('all')

    return uri

def inicio(request):
    chart_q = generarTiempos('Q')
    chart_r = generarTiempos('R')
    table_data = generarTabla()
    return render(request,'inicio.html',{'chart_q':chart_q,'chart_r':chart_r,'table':table_data})




def predecir(request):
    return render(request,'predecir.html')

def points_stats(request):
    return render(request,'acumulados.html')


def cargar(request):
    if request.method == "POST":
        populate_drivers()
        populate_circuits()
        return HttpResponseRedirect('/')

    return render(request,'populateDB.html')


def velocidad(request):
    if request.method == "POST":
        form = DriverCircuitYear(request.POST)
        if form.is_valid():
            driver = form.cleaned_data['driver']
            circuit = form.cleaned_data['circuit']
            year = int(form.cleaned_data['year'])
            try:
                chart = generarF1(year,driver.code,circuit.name)
            except:
                chart = None
        return render(request,'velocidades.html', {'form':form,'chart':chart})
    form = DriverCircuitYear()
    return render(request,'velocidades.html', {'form':form})