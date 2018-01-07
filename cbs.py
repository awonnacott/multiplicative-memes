#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import csv
import os

positions = [
    'QB',
    'RB',
    'WR',
    'TE',
    'K',
    'DST',
]
weeks = range(1, 22)


def cbs(pos, week):
    url = 'https://www.cbssports.com/fantasy/football/stats/sortable/points/{pos}/standard/projections/2017/{week}?&print_rows=9999'.format(pos=pos, week=week)
    try:
        contents = requests.get(url).content
        soup = BeautifulSoup(contents, "html.parser")
        rows = soup.find('table').find_all('tr')
        header = [td.text.split(',')[0] for td in rows[2]]
        data = [[td.text.split(',')[0] for td in row] for row in rows[3:-1]]
    except IndexError:
        print("Failed: " + pos + " " + str(week))
        return
    filename = 'cbs_{pos}_week{week}.csv'.format(pos=pos, week=week)
    with open(filename, 'w') as f:
        print('writing: ', filename)
        writer = csv.writer(f)
        try:
            writer.writerow(header)
            writer.writerows(data)
        except UnicodeEncodeError:
            print("Failed: " + pos + " " + str(week))
            print(header)
            print(data)
            return


os.chdir('cbs')
[cbs(pos, week) for pos in positions for week in weeks]
os.chdir('..')
