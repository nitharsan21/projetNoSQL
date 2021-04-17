#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
import requests
from bs4 import BeautifulSoup as bs
from pymongo import MongoClient
import pandas as pd

def getHeaderTable(tab):
    header = tab.find('tr')
    header = header.find_all('th')
    header = [x.text.strip() for x in header]
    header[0] = "Year"
    return header


def getContaintTable(tab):
    containt = []
    for tr in tab.find_all('tr'):
        tds = tr.find_all('td')
        tds = [x.text.strip() for x in tds]
        containt.append(tds)
    return containt


if __name__ == '__main__':

    start_urls = 'https://en.wikipedia.org/wiki/Demographics_of_France'
    response = requests.get(start_urls)
    soup = bs(response.text, 'html.parser')

    div = soup.find('div', {'id': 'mw-content-text'})
    tables = div.find_all('table', {'class': 'wikitable'})

    headerTable = getHeaderTable(tables[19])
    print(headerTable)

    ContaintTable = getContaintTable(tables[19])
    #print(ContaintTable)

    with open('population.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL, delimiter=',')
        writer.writerow(headerTable)
        print("\nLe fichier CSV est bien crée")
        for containt in ContaintTable[1:]:
            writer.writerow(containt)
            print(containt)

    #Connexion Mongo
    client = MongoClient("mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false")
    database = client['dataDimog']
    collection = database['collecDimog']

    #Ouverture du CSV
    df_dimog = pd.read_csv("population.csv")

    #Push des données
    records = df_dimog.to_dict(orient='records')
    collection.insert_many(records)