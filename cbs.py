#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import csv
import os

positions = ['QB', 'RB', 'WR', 'TE', 'K', 'DST']
weeks = range(1, 21)
writers = ['jamey_eisenberg', 'dave_richard']
source = ['cbs1', 'cbs2']
leaguetype = 'standard'


def cbs(pos, week, leaguetype, writer):
    url = 'https://fantasynews.cbssports.com/fantasyfootball/stats/weeklyprojections/{pos}/{week}/{writer}/{leaguetype}?&print_rows=9999'.format(pos=pos, week=week, leaguetype=leaguetype, writer=writer)
    contents = requests.get(url).content
    soup = BeautifulSoup(contents, "html.parser")
    rows = soup.find('table').find_all('tr')
    header = [td.text.split(',')[0] for td in rows[2]]
    data = [[td.text.split(',')[0] for td in row] for row in rows[3:-1]]
    filename = 'week{week}_{pos}_cbs_{writer}.csv'.format(pos=pos, week=week, writer=writer)
    with open(filename, 'w') as f:
        print('writing: ', filename)
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)


os.chdir('cbs')
[cbs(pos, week, leaguetype, writer) for pos in positions for week in weeks for writer in writers]
os.chdir('..')
