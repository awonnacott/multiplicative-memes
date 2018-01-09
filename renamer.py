import os
for week in range(1, 18):
    for pos in ["QB", "RB", "WR", "TE"]:
        os.rename("fantasyalarm/2017 NFL Week " + str(week) + " Fantasy Football " + pos + " Draft Rankings  FantasyAlarm.com.csv", "fantasyalarm/fantasyalarm_" + pos + "_week" + str(week) + ".csv")
