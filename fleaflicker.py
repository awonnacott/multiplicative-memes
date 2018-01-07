#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import csv
import os

positions = {
    'QB': 4,
    'RB': 1,
    'WR': 2,
    'TE': 8,
    'DST': 256,
    'K': 16,
    'DB': 32,
    'DL': 64,
    'LB': 128,
}
pages = {
    'QB': 2,
    'RB': 6,
    'WR': 8,
    'TE': 4,
    'DST': 2,
    'K': 2,
    'DB': 12,
    'DL': 10,
    'LB': 9,
}
weeks = range(1, 22)


def cbs(pos, week):
    url = 'https://www.fleaflicker.com/nfl/leaders?week={week}&sortMode=2&statType=2&position={pos}&tableOffset={i}'.format(pos=positions[pos], week=week, i="{i}")
    try:
        contents = requests.get(url.format(i=0)).content
        soup = BeautifulSoup(contents, "html.parser")
        header = [td.text.split(',')[0].replace(u'\xa0', u'') for td in soup.find('thead').find_all('tr')[1]]
        data = []
        for i in range(pages[pos]):
            contents = requests.get(url.format(i=20 * i)).content
            soup = BeautifulSoup(contents, "html.parser")
            rows = soup.find('table').find_all('tr')
            data += [[td.text.split(',')[0].replace(u'\xa0', u'').replace(u'•', u'') for td in row] for row in rows[2:-1]]
    except AttributeError:
        print("Failed: " + pos + " " + str(week))
        return
    except IndexError:
        print("Failed: " + pos + " " + str(week))
        return
    filename = 'fleaflicker_{pos}_week{week}.csv'.format(pos=pos, week=week)
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


os.chdir('fleaflicker')
[cbs(pos, week) for pos in positions for week in weeks]
os.chdir('..')
