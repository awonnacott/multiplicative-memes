#!/usr/bin/env python3

import os
import csv
import pdb

def clean(pos, week, source):
    # Player, passing YDS, passing TD, INT, rushing YDS, rushing TD, receiving YDS, receiving TD
    stats = {}
    filename = source + "/" + source + "_" + pos + "_week" + week + ".csv"
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        if source == "espn" :
            if pos == "QB" or pos == "RB" or pos == "WR" or pos == "TE":
                first_row = True
                for row in reader:
                    if first_row:
                        first_row = False
                    elif len(row) == 14:
                        player = row[0]
                        if(player[len(player) - 1] == '*'):
                            player = player[:(len(player) - 1)]
                        stats[player] = [float(row[4]), float(row[5]), float(row[6]), float(row[8]),
                                         float(row[9]), float(row[11]), float(row[12])]
            else:
                print "Unrecognized position."
        elif source == "cbs":
            print ""
        elif source == "fftoday":
            if pos == "QB":
                first_row = True
                for row in reader:
                    if first_row:
                        first_row = False
                    else:
                        stats[row[1]] = [float(row[6]), float(row[7]), float(row[8]), float(row[10]),
                                         float(row[11]), 0, 0]
            elif pos == "RB":
                first_row = True
                for row in reader:
                    if first_row:
                        first_row = False
                    else:
                        stats[row[1]] = [0, 0, 0, float(row[5]), float(row[6]), float(row[8]), float(row[9])]
            elif pos == "WR":
                first_row = True
                for row in reader:
                    if first_row:
                        first_row = False
                    else:
                        stats[row[1]] = [0, 0, 0, 0, 0, float(row[5]), float(row[6])]
            elif pos == "TE":
                first_row = True
                for row in reader:
                    if first_row:
                        first_row = False
                    else:
                        stats[row[1]] = [0, 0, 0, 0, 0, float(row[5]), float(row[6])]
            else:
                print "Unrecognized position."
        elif source == "nfl":
            if pos == "QB" or pos == "RB" or pos == "WR" or pos == "TE":
                first_row = True
                for row in reader:
                    if first_row:
                        first_row = False
                    else:
                        for i in range(len(row)):
                            if row[i] == "-":
                                row[i] = 0
                        player = row[0][:(row[0].find(pos) - 1)]
                        stats[player] = [float(row[2]), float(row[3]), float(row[4]), float(row[5]),
                                         float(row[6]), float(row[7]), float(row[8])]
            else:
                print "Unrecognized position."
        else:
            print "Unrecognized source."
        return stats

def get_true_values(pos, week):
    # Player, passing YDS, passing TD, INT, rushing YDS, rushing TD, receiving YDS, receiving TD
    stats = {}
    filename = "cbs/week" + week + "_" + pos + "_cbs_dave_richard.csv"
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        if pos == "QB":
            first_row = True
            for row in reader:
                if first_row:
                    first_row = False
                else:
                    stats[row[0]] = [float(row[3]), float(row[4]), float(row[5]), float(row[9]),
                                     float(row[11]), 0, 0]
        elif pos == "RB":
            first_row = True
            for row in reader:
                if first_row:
                    first_row = False
                else:
                    stats[row[0]] = [0, 0, 0, float(row[2]), float(row[4]), float(row[6]), float(row[8])]
        elif pos == "WR":
            first_row = True
            for row in reader:
                if first_row:
                    first_row = False
                else:
                    stats[row[0]] = [0, 0, 0, 0, 0, float(row[2]), float(row[4])]
        elif pos == "TE":
            first_row = True
            for row in reader:
                if first_row:
                    first_row = False
                else:
                    stats[row[0]] = [0, 0, 0, 0, 0, float(row[2]), float(row[4])]
        else:
            print "Unrecognized position."
    return stats

#print clean("WR", "10", "fftoday")
#print get_true_values("TE", "10")