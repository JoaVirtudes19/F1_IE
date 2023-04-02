from django.shortcuts import render, HttpResponseRedirect
import matplotlib.pyplot as plt
import matplotlib as mpl
import io
import urllib, base64
mpl.use('Agg')
import fastf1 as ff1
import numpy as np
from matplotlib.collections import LineCollection
from web.populateDB import populate_drivers, populate_circuits
from web.forms import DriverCircuitYear
import requests
# Create your views here.


def generarF1(year,driver,circuit_name):
    ff1.Cache.enable_cache('./f1cache')  # replace with your cache directory
    request = requests.get('http://ergast.com/api/f1/{}/results.json?limit=1000'.format(year))
    data = request.json()
    wknd = int([ race['round'] for race in data['MRData']['RaceTable']['Races'] if race['Circuit']['circuitName'] == circuit_name][0])
    ses = 'R'
    driver = driver
    colormap = mpl.cm.plasma
    session = ff1.get_session(year, wknd, ses)
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
    graficas = []
    return render(request,'inicio.html',{'charts':graficas})




def predecir(request):
    return render(request,'predecir.html')


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