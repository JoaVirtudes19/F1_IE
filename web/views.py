from django.shortcuts import render, HttpResponseRedirect

from web.forms import DriverCircuitYear, CompareSpeed, Prediction
from web.populateDB import populate_drivers, populate_circuits,populate_constructors
from web.charts import ChartFactory
from web.predict import predict


def latest_results(request):
    chart_q = ChartFactory.generate_times('Q')
    chart_r = ChartFactory.generate_times('R')
    table_data = ChartFactory.generate_table()
    return render(request, 'latest_results.html', {'chart_q': chart_q, 'chart_r': chart_r, 'table': table_data})


def predict_results(request):
    if request.method == "POST":
        form = Prediction(request.POST)
        if form.is_valid():
            driver = form.cleaned_data['driver']
            circuit = form.cleaned_data['circuit']
            year = int(form.cleaned_data['year'])
            constructor = form.cleaned_data['constructor']
            grid = int(form.cleaned_data['grid'])
            year_round = int(form.cleaned_data['year_round'])
            weather={'weather_warm':int(form.cleaned_data['warm']),
                    'weather_cold':int(form.cleaned_data['cold']),
                    'weather_dry':int(form.cleaned_data['dry']),
                    'weather_wet':int(form.cleaned_data['wet']),
                    'weather_cloudy':int(form.cleaned_data['cloudy'])}

            results = predict(driver.driver_id,
                    grid_pos,
                    year,
                    constructor.constructor_id,
                    circuit.circuit_id,
                    year_round,
                    weather)



        return render(request, 'predict_results.html', {'form': form})
    form = Prediction()
    return render(request, 'predict_results.html',{'form': form})


def points_stats(request):
    return render(request, 'points_charts.html')


def populate_db(request):
    if request.method == "POST":
        populate_drivers()
        populate_circuits()
        populate_constructors()
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
