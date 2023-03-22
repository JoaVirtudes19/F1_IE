from django.shortcuts import render
import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64
matplotlib.use('Agg')
# Create your views here.

def generar(n,title):
    plt.plot(range(n))
    plt.title(title)
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf,format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return uri

def inicio(request):
    graficas = [generar(10,"primera"),generar(20,"segunda")]
    return render(request,'inicio.html',{'charts':graficas})




def predecir(request):
    return render(request,'predecir.html')