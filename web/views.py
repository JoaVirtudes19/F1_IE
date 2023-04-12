from django.shortcuts import render, HttpResponseRedirect

from web.forms import DriverCircuitYear, CompareSpeed
from web.populateDB import populate_drivers, populate_circuits
from web.charts import ChartFactory


def latest_results(request):
    chart_q = ChartFactory.generate_times('Q')
    chart_r = ChartFactory.generate_times('R')
    table_data = ChartFactory.generate_table()
    return render(request, 'latest_results.html', {'chart_q': chart_q, 'chart_r': chart_r, 'table': table_data})


def predict_results(request):
    return render(request, 'predict_results.html')


def points_stats(request):
    return render(request, 'points_charts.html')


def populate_db(request):
    if request.method == "POST":
        populate_drivers()
        populate_circuits()
        return HttpResponseRedirect('/')

    return render(request, 'populateDB.html')


def telemetry_speed(request):
    if request.method == "POST":
        form = DriverCircuitYear(request.POST)
        if form.is_valid():
            driver = form.cleaned_data['driver']
            circuit = form.cleaned_data['circuit']
            year = int(form.cleaned_data['year'])
            try:
                chart = ChartFactory.generate_f1(year, driver.code, circuit.name)
            except:
                chart = None
        return render(request, 'telemetry_speed.html', {'form': form, 'chart': chart})
    form = DriverCircuitYear()
    return render(request, 'telemetry_speed.html', {'form': form})


def compare_speed(request):
    if request.method == "POST":
        form = CompareSpeed(request.POST)
        if form.is_valid():
            driver_1 = form.cleaned_data['driver_1']
            driver_2 = form.cleaned_data['driver_2']
            circuit = form.cleaned_data['circuit']
            year = int(form.cleaned_data['year'])
            try:
                chart = ChartFactory.generate_VS(year, driver_1.code, driver_2.code, circuit.name)
            except:
                chart = None
        return render(request, 'compare_speed.html', {'form': form, 'chart': chart})
    form = CompareSpeed()
    return render(request, 'compare_speed.html', {'form': form})
