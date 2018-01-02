#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import csv
import os

positions = {
    'QB': 10,
    'RB': 20,
    'WR': 30,
    'TE': 40,
    'K': 80
}
weeks = range(1, 22)

def cbs(pos, week):
    url = 'https://www.fftoday.com/rankings/playerwkproj.php?Season=2017&GameWeek={week}&PosID={pos}&LeagueID=1'.format(pos=positions[pos], week=week)
    try:
        contents = requests.get(url).content
        soup = BeautifulSoup(contents, "html.parser")
        rows = soup.find_all('table')[9].find_all('tr')
        header = [td.text.rstrip().replace(u'\xa0', u'') for td in rows[2].find_all('td')]
        data = [[td.text.rstrip().replace(u'\xa0', u'') for td in row.find_all('td')] for row in rows[3:]]
    except IndexError:
        print("Failed: " + pos + " " + str(week))
        return
    filename = 'fftoday_{pos}_week{week}.csv'.format(pos=pos, week=week)
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


os.chdir('fftoday')
[cbs(pos, week) for pos in positions for week in weeks]
os.chdir('..')
