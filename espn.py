#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import csv
import os

positions = {
    'QB': 0,
    'RB': 2,
    'WR': 4,
    'TE': 6,
    'DST': 16,
    'K': 17,
    'FLEX': 23
}
pages = {
    'QB': 4,
    'RB': 8,
    'WR': 10,
    'TE': 6,
    'DST': 1,
    'K': 2,
    'FLEX': 22,
}
weeks = range(1, 22)


def cbs(pos, week):
    url = 'https://games.espn.com/ffl/tools/projections?&scoringPeriodId={week}&seasonId=2017&slotCategoryId={pos}&startIndex={i}'.format(pos=positions[pos], week=week, i="{i}")
    try:
        contents = requests.get(url.format(i=0)).content
        soup = BeautifulSoup(contents, "html.parser")
        rows = soup.find('table').find_all('tr')
        header = [td.text.split(',')[0].replace(u'\xa0', u'') for td in rows[2]]
        data = []
        for i in range(pages[pos]):
            contents = requests.get(url.format(i=40 * i)).content
            soup = BeautifulSoup(contents, "html.parser")
            rows = soup.find('table').find_all('tr')
            data += [[td.text.split(',')[0].split('D/ST')[0] for td in row] for row in rows[3:]]
    except AttributeError:
        print("Failed: " + pos + " " + str(week))
        return
    filename = 'espn_{pos}_week{week}.csv'.format(pos=pos, week=week)
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


os.chdir('espn')
[cbs(pos, week) for pos in positions for week in weeks]
os.chdir('..')
