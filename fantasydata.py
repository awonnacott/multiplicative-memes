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
    'K': 5,
    'DST': 6,
}
weeks = range(0, 16)


def cbs(pos, week):
    url = 'https://fantasydata.com/nfl-stats/fantasy-football-weekly-projections.aspx?stype=0&w={week}&ew={week}&p={pos}'.format(pos=positions[pos], week=week - 1)
    try:
        contents = requests.get(url).content
        soup = BeautifulSoup(contents, "html.parser")
        header = [th.text for th in soup.find_all('th')]
        data = [[td.text for td in row.find_all('td')] for row in soup.find_all('tr')[1:]]
    except AttributeError:
        print("Failed: " + pos + " " + str(week))
        return
    except IndexError:
        print("Failed: " + pos + " " + str(week))
        return
    filename = 'fantasydata_{pos}_week{week + 1}.csv'.format(pos=pos, week=week)
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


os.chdir('fantasydata')
[cbs(pos, week) for pos in positions for week in weeks]
os.chdir('..')
