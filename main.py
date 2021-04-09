import urllib.request
from bs4 import BeautifulSoup


print("Welcomeé to Projèct NoSQL \n   First Part : Scraping  \n ")

url = urllib.request.urlopen('https://fr.wikipedia.org/wiki/D%C3%A9mographie_de_la_France/')
soup = BeautifulSoup(url, 'html.parser')
print(soup)





