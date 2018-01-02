#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import csv
import os

positions = {
    'QB': 1,
    'RB': 2,
    'WR': 3,
    'TE': 4,
    'K': 7,
    'DEF': 8
}
weeks = range(1, 22)

def cbs(pos, week):
    url = 'http://fantasy.nfl.com/research/projections?position={pos}&sort=projectedPts&statCategory=projectedStats&statSeason=2017&statType=weekProjectedStats&statWeek={week}'.format(pos=positions[pos], week=week)
    try:
        contents = requests.get(url).content
        soup = BeautifulSoup(contents, "html.parser")
        table = soup.find('table')
        header = [td.text.rstrip().replace(u'\xa0', u'') for td in table.find('thead').find_all('tr')[1].find_all('th')]
        data = [[td.text.rstrip().replace(u'\xa0', u'') for td in row.find_all('td')] for row in table.find('tbody').find_all('tr')]
    except IndexError:
        print("Failed: " + pos + " " + str(week))
        return
    filename = 'nfl_{pos}_week{week}.csv'.format(pos=pos, week=week)
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


os.chdir('nfl')
[cbs(pos, week) for pos in positions for week in weeks]
os.chdir('..')
