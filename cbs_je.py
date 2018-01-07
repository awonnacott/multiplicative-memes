#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import csv
import os

positions = ['QB', 'RB', 'WR', 'TE', 'K', 'DST']
weeks = range(1, 18)


def cbs(pos, week, leaguetype, writer):
    url = 'https://fantasynews.cbssports.com/fantasyfootball/stats/weeklyprojections/{pos}/{week}/jamey_eisenberg/standard?&print_rows=9999'.format(pos=pos, week=week, leaguetype=leaguetype, writer=writer)
    contents = requests.get(url).content
    soup = BeautifulSoup(contents, "html.parser")
    rows = soup.find('table').find_all('tr')
    header = [td.text.split(',')[0] for td in rows[2]]
    data = [[td.text.split(',')[0] for td in row] for row in rows[3:-1]]
    filename = 'cbs_je_{pos}_week{week}.csv'.format(pos=pos, week=week)
    with open(filename, 'w') as f:
        print('writing: ', filename)
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)


os.chdir('cbs_je')
[cbs(pos, week, leaguetype) for pos in positions for week in weeks]
os.chdir('..')
