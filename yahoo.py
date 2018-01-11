#!/usr/bin/env python3

from bs4 import BeautifulSoup
import csv
import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

username = "weinky"
password = ""
pages = {
    'QB': 5,
    'RB': 11,
    'WR': 16,
    'TE': 10,
}
weeks = range(1, 18)


def cbs(pos, week):
    url = 'https://football.fantasysports.yahoo.com/f1/731507/players?&sort=AR&sdir=1&status=ALL&pos={pos}&stat1=S_PW_{week}&jsenabled=1&count={i}'.format(pos=pos, week=week, i="{i}")
    try:
        driver.get(url.format(i=0))
        time.sleep(3)
        elem = driver.find_element_by_class_name("Table")
        soup = BeautifulSoup(elem.get_attribute("innerHTML"), "html.parser")
        pheader = soup.find('thead').find_all('tr')[1].find_all('th')
        header = [th.text.strip(u'\ue002') for th in pheader]
        header = ['FN', 'LN'] + header[3:-1]
        data = []
        for i in range(pages[pos]):
            driver.get(url.format(i=25 * i))
            time.sleep(3)
            elem = driver.find_element_by_class_name("Table")
            soup = BeautifulSoup(elem.get_attribute("innerHTML"), "html.parser")
            pdata = [[td.text for td in row.find_all('td')] for row in soup.find_all('tr') if len(row.find_all('td')) == len(pheader)]
            data += [row[1].split('\n')[2].split(' ')[:2] + row[3:-1] for row in pdata]
    except AttributeError:
        print("Failed: " + pos + " " + str(week))
        return
    filename = 'yahoo_{pos}_week{week}.csv'.format(pos=pos, week=week)
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


url = 'https://football.fantasysports.yahoo.com/f1/731507/players'

driver = webdriver.Firefox()
driver.get(url)

elem = driver.find_element_by_id("login-username")
elem.clear()
elem.send_keys(username)
elem.send_keys(Keys.RETURN)
time.sleep(2)

elem = driver.find_element_by_id("login-passwd")
elem.clear()
elem.send_keys(password)
elem.send_keys(Keys.RETURN)

os.chdir('yahoo')
[cbs(pos, week) for pos in pages for week in weeks]
os.chdir('..')
