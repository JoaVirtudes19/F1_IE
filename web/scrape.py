import requests
from bs4 import BeautifulSoup
from web.models import Driver,Constructor




def get_constructor_img(constructor_id):
    try:
        constructor = Constructor.objects.all().get(constructor_id=constructor_id)
        response = requests.get(constructor.url)

        soup = BeautifulSoup(response.text, "html.parser")

        infobox = soup.find("td", class_="infobox-image")

        imagen = infobox.find("img")

        url_imagen = imagen["src"]
        return url_imagen
    except:
        return "https://upload.wikimedia.org/wikipedia/commons/3/33/F1.svg"


def get_driver_img(driver_id):
    try:
        driver = Driver.objects.all().get(driver_id=driver_id)
        response = requests.get(driver.url)

        soup = BeautifulSoup(response.text, "html.parser")

        infobox = soup.find("td", class_="infobox-image")

        imagen = infobox.find("img")

        url_imagen = imagen["src"]
        return url_imagen
    except:
        return "https://cdn-icons-png.flaticon.com/512/1170/1170459.png"