from bs4 import BeautifulSoup
import requests

url = 'https://www.immobilienscout24.de/Suche/de/baden-wuerttemberg/anlageimmobilie'

r = requests.get(url)

soup = BeautifulSoup(r.content, 'lxml')

print(soup.prettify())