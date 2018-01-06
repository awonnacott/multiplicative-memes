#!/usr/bin/env python3

import csv


def clean(pos, week, source):
    # Player, passing YDS, passing TD, INT, rushing YDS, rushing TD, receiving YDS, receiving TD
    stats = {}
    filename = source + "/" + source + "_" + pos + "_week" + week + ".csv"
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        if source == "espn":
            next(reader)  # discard first row
            if pos == "QB" or pos == "RB" or pos == "WR" or pos == "TE":
                for row in reader:
                    player = row[0]
                    if(player[len(player) - 1] == '*'):
                        player = player[:(len(player) - 1)]
                    stats[player] = [float(row[i]) for i in [4, 5, 6, 8, 9, 11, 12]]
            else:
                print("Unrecognized position.")
        elif source == "cbs":
            print("")
        elif source == "fftoday":
            next(reader)
            if pos == "QB":
                for row in reader:
                    stats[row[1]] = [float(row[6]), float(row[7]), float(row[8]), float(row[10]),
                                     float(row[11]), 0, 0]
            elif pos == "RB":
                for row in reader:
                    stats[row[1]] = [0, 0, 0, float(row[5]), float(row[6]), float(row[8]), float(row[9])]
            elif pos == "WR":
                for row in reader:
                    stats[row[1]] = [0, 0, 0, 0, 0, float(row[5]), float(row[6])]
            elif pos == "TE":
                for row in reader:
                    stats[row[1]] = [0, 0, 0, 0, 0, float(row[5]), float(row[6])]
            else:
                print("Unrecognized position.")
        elif source == "nfl":
            next(reader)
            if pos == "QB" or pos == "RB" or pos == "WR" or pos == "TE":
                for row in reader:
                    row = ["0" if s == "-" else s for s in row]
                    player = row[0][:(row[0].find(pos) - 1)]
                    stats[player] = [float(row[i]) for i in range(2, 9)]
            else:
                print("Unrecognized position.")
        else:
            print("Unrecognized source.")
        return stats


def get_true_values(pos, week):
    # Player, passing YDS, passing TD, INT, rushing YDS, rushing TD, receiving YDS, receiving TD
    stats = {}
    filename = "cbs/week" + week + "_" + pos + "_cbs_dave_richard.csv"
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # discard first row
        if pos == "QB":
            for row in reader:
                stats[row[0]] = [float(row[3]), float(row[4]), float(row[5]), float(row[9]),
                                 float(row[11]), 0, 0]
        elif pos == "RB":
            for row in reader:
                stats[row[0]] = [0, 0, 0, float(row[2]), float(row[4]), float(row[6]), float(row[8])]
        elif pos == "WR":
            for row in reader:
                stats[row[0]] = [0, 0, 0, 0, 0, float(row[2]), float(row[4])]
        elif pos == "TE":
            for row in reader:
                stats[row[0]] = [0, 0, 0, 0, 0, float(row[2]), float(row[4])]
        else:
            print("Unrecognized position.")
    return stats


if __name__ == "__main":
    print(clean("WR", "10", "fftoday"))
    print(get_true_values("TE", "10"))
