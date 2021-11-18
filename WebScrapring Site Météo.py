#WebScraping d'un site météo

import requests
from bs4 import BeautifulSoup

response = requests.get('https://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168').content
parser = BeautifulSoup(response, 'html.parser')
seven_day = parser.find(id="seven-day-forecast").find_all(class_='tombstone-container')

pt = [n.select(".period-name") for n in seven_day]
names = [n[0].get_text()for n in pt]
sd = [n.select(".short-desc") for n in seven_day]
short_descs = [n[0].get_text()for n in sd]

t = [n.select(".temp") for n in seven_day]
temps = [n[0].get_text()for n in t]

descs = [n.find("img")['title'] for n in seven_day]

#Affichage avec pandas
import pandas as pd
weather =pd.DataFrame({
    'Period': names,
    'Short description': short_descs,
    'Temperature': temps,
    'Description': descs
})
print(weather)
