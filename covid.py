import sys
import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

import requests

def load_data(filepath):
  data = {}
  with open(filepath) as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for i, row in enumerate(reader):
      if i < 2:
        continue
      region  = row[0]
      country = row[1]
      date    = row[-2]
      cases   = row[-1]

      if cases == '':
        cases = 0
      year, month, day = [int(n) for n in date.split('-')]

      if row[1] == 'US':
        if month >= 3 and day >= 10: # Johns Hopkins started changing the data format on Mar 10 for some reason???
          if ',' in row[0]: # Ignore county-level data, use state data instead
            cases = 0

      if country not in data: # missing country name
        data[country] = {}
      if date not in data[country]: # missing date
        data[country][date] = 0

      data[country][date] += int(cases)

  for key in data.keys():
    if ' ' in key:
      datum   = data[key]
      new_key = ''.join(key.split())
      del data[key]
      data[new_key] = datum
  return data


def graph(data, countries=['US'], dayzerothreshold=100, ylabel='cases'):
  
  fig, ax1 = plt.subplots()
  ax1.set_xlabel('days since threshold surpassed', fontsize=11)
  ax1.set_ylabel(ylabel, fontsize=12)

  for country in countries:
    try:
      country_y = []
      for date, n in data[country].items():
        if n > dayzerothreshold:
          country_y.append(n)
      country_y = np.asarray(country_y[::-1])
      country_x = np.asarray(range(len(country_y)))
      ax1.plot(country_x, country_y, c=np.random.rand(3), alpha=0.8, label=country)

    except KeyError:
      pass
    #print(data[country].items())
  ax1.legend(loc='upper left')
  fig.tight_layout()
  plt.show()


def prettylogo():
  print()
  print(" .d8888b.   .d88888b.  888     888 8888888 8888888b.        d888   .d8888b. ") 
  print("d88P  Y88b d88P\" \"Y88b 888     888   888   888  \"Y88b      d8888  d88P  Y88b") 
  print("888    888 888     888 888     888   888   888    888        888  888    888") 
  print("888        888     888 Y88b   d88P   888   888    888        888  Y88b. d888") 
  print("888        888     888  Y88b d88P    888   888    888        888   \"Y888P888") 
  print("888    888 888     888   Y88o88P     888   888    888 888888 888         888") 
  print("Y88b  d88P Y88b. .d88P    Y888P      888   888  .d88P        888  Y88b  d88P") 
  print(" \"Y8888P\"   \"Y88888P\"      Y8P     8888888 8888888P\"       8888888 \"Y8888P  ") 
  print()


if __name__ == '__main__':
  prettylogo()

  option1 = input("Would you like to graph confirmed cases or deaths (enter 'cases' or 'deaths'): ").lower()
  while not 'cases' in option1 and not 'deaths' in option1:
    option1 = input("Please enter either 'cases' or 'deaths': ").lower()
  if 'cases' in option1:
    print("\nOk, graphing confirmed cases of Covid-19.")
    cases = True
    data_file = 'covid_cases.csv'
    data_url = 'http://data.humdata.org/hxlproxy/data/download/time_series-ncov-Confirmed.csv?dest=data_edit&filter01=explode&explode-header-att01=date&explode-value-att01=value&filter02=rename&rename-oldtag02=%23affected%2Bdate&rename-newtag02=%23date&rename-header02=Date&filter03=rename&rename-oldtag03=%23affected%2Bvalue&rename-newtag03=%23affected%2Binfected%2Bvalue%2Bnum&rename-header03=Value&filter04=clean&clean-date-tags04=%23date&filter05=sort&sort-tags05=%23date&sort-reverse05=on&filter06=sort&sort-tags06=%23country%2Bname%2C%23adm1%2Bname&tagger-match-all=on&tagger-default-tag=%23affected%2Blabel&tagger-01-header=province%2Fstate&tagger-01-tag=%23adm1%2Bname&tagger-02-header=country%2Fregion&tagger-02-tag=%23country%2Bname&tagger-03-header=lat&tagger-03-tag=%23geo%2Blat&tagger-04-header=long&tagger-04-tag=%23geo%2Blon&header-row=1&url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_19-covid-Confirmed.csv'
  else:
    print("\nOk, graphing deaths due to Covid-19.")
    cases = False
    data_file = 'covid_deaths.csv'
    data_url = 'http://data.humdata.org/hxlproxy/data/download/time_series-ncov-Deaths.csv?dest=data_edit&filter01=explode&explode-header-att01=date&explode-value-att01=value&filter02=rename&rename-oldtag02=%23affected%2Bdate&rename-newtag02=%23date&rename-header02=Date&filter03=rename&rename-oldtag03=%23affected%2Bvalue&rename-newtag03=%23affected%2Bkilled%2Bvalue%2Bnum&rename-header03=Value&filter04=clean&clean-date-tags04=%23date&filter05=sort&sort-tags05=%23date&sort-reverse05=on&filter06=sort&sort-tags06=%23country%2Bname%2C%23adm1%2Bname&tagger-match-all=on&tagger-default-tag=%23affected%2Blabel&tagger-01-header=province%2Fstate&tagger-01-tag=%23adm1%2Bname&tagger-02-header=country%2Fregion&tagger-02-tag=%23country%2Bname&tagger-03-header=lat&tagger-03-tag=%23geo%2Blat&tagger-04-header=long&tagger-04-tag=%23geo%2Blon&header-row=1&url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_19-covid-Deaths.csv'
  
  print("Querying internet for data ...")
  response = requests.get(data_url)
  print("Done.\n")
  open(data_file, 'wb').write(response.content)
  data = load_data(data_file)

  while True:
    validint = False
    try:
      threshold = int(input("Enter a minimum incidence threshold for day 0 (some integer greater than zero): "))
      validint = True
    except ValueError:
      while not validint:
        try:
          threshold = int(input("Enter an integer greater than zero (like 150): "))
          validint = True
        except ValueError:
          pass


    print()
    print(list(data.keys()))
    valid = False
    while not valid:
      countries = input("Enter the countries you wish to compare from the list above, separated by spaces: ").split()
      valid = False not in [c in data.keys() for c in countries]
      for c in countries:
        if c not in data.keys():
          print("Invalid country '{}'.".format(c))
      
    print("Comparing: ", countries)

    graph(data, dayzerothreshold=int(threshold), countries=countries, ylabel=option1)
