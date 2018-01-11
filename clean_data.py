#!/usr/bin/env python3

import csv

experts = ["espn", "nfl", "fftoday", "cbs", "fantasydata", "fantasyalarm", "yahoo"]
# experts = ["espn"]
positions = ["QB", "RB", "WR", "TE"]
num_weeks = 17
points_weights = [.04, 4, -2, .1, 6, .1, 6]


def clean_name(player):
    player = ((player.rstrip('*')).replace('.', '')).lower()
    if player.endswith(' iii'):
        player = player[:-4]
    elif player.endswith(' ii'):
        player = player[:-3]
    elif player.endswith(' iv'):
        player = player[:-3]
    elif player.endswith(' v'):
        player = player[:-2]
    elif player.endswith(' jr'):
        player = player[:-3]
    elif player.endswith(' sr'):
        player = player[:-3]
    return player


def clean(pos, week, source):
    # Player, passing YDS, passing TD, INT, rushing YDS, rushing TD, receiving YDS, receiving TD
    stats = {}
    filename = source + "/" + source + "_" + pos + "_week" + week + ".csv"
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        if source == "truevalues":
            next(reader)
            if pos == "QB" or pos == "RB" or pos == "WR" or pos == "TE":
                for row in reader:
                    row = ["0" if s == "--" or s == "" else s for s in row]
                    player = clean_name(row[0])
                    stats[player] = [float(row[i]) for i in [6, 7, 8, 11, 12, 15, 16]]
            else:
                print("Unrecognized position.")
        elif source == "espn":
            next(reader)  # discard first row
            if pos == "QB" or pos == "RB" or pos == "WR" or pos == "TE":
                for row in reader:
                    row = ["0" if s == "--" else s for s in row]
                    player = clean_name(row[0])
                    stats[player] = [float(row[i]) for i in [4, 5, 6, 8, 9, 11, 12]]
            else:
                print("Unrecognized position.")
        elif source == "cbs":
            next(reader)  # discard first row
            if pos == "QB" or pos == "RB" or pos == "WR" or pos == "TE":
                for row in reader:
                    player = clean_name(row[0])
                    stats[player] = [float(row[i]) for i in [3, 4, 5, 8, 10, 13, 15]]
            else:
                print("Unrecognized position.")
        elif source == "fftoday":
            next(reader)
            if pos == "QB":
                for row in reader:
                    player = clean_name(row[1])
                    stats[player] = [float(row[i]) for i in [6, 7, 8, 10, 11]] + [0, 0]
            elif pos == "RB":
                for row in reader:
                    player = clean_name(row[1])
                    stats[player] = [0, 0, 0] + [float(row[i]) for i in [5, 6, 8, 9]]
            elif pos == "WR":
                for row in reader:
                    player = clean_name(row[1])
                    stats[player] = [0, 0, 0, 0, 0, float(row[5]), float(row[6])]
            elif pos == "TE":
                for row in reader:
                    player = clean_name(row[1])
                    stats[player] = [0, 0, 0, 0, 0, float(row[5]), float(row[6])]
            else:
                print("Unrecognized position.")
        elif source == "nfl":
            next(reader)
            if pos == "QB" or pos == "RB" or pos == "WR" or pos == "TE":
                for row in reader:
                    row = ["0" if s == "-" else s for s in row]
                    player = clean_name(row[0][:(row[0].find(pos) - 1)])
                    stats[player] = [float(row[i]) for i in range(2, 9)]
            else:
                print("Unrecognized position.")
        elif source == "fantasydata":
            next(reader)
            if pos == "QB":
                for row in reader:
                    player = clean_name(row[1])
                    stats[player] = [float(row[i]) for i in [9, 11, 12, 15, 17]] + [0, 0]
            elif pos == "RB":
                for row in reader:
                    player = clean_name(row[1])
                    stats[player] = [0, 0, 0] + [float(row[i]) for i in [7, 9, 12, 13]]
            elif pos == "WR" or pos == "TE":
                for row in reader:
                    player = clean_name(row[1])
                    stats[player] = [0, 0, 0] + [float(row[i]) for i in [15, 16, 9, 10]]
            else:
                print("Unrecognized position.")
        elif source == "fantasyalarm":
            next(reader)
            if pos == "QB" or pos == "RB" or pos == "WR" or pos == "TE":
                for row in reader:
                    row = ["0" if s == "-" else s for s in row]
                    player = clean_name(row[1])
                    stats[player] = [float(row[i]) for i in [6, 7, 8, 9, 10, 11, 12]]
            else:
                print("Unrecognized position.")
        elif source == "yahoo":
            next(reader)
            if pos == "QB" or pos == "RB" or pos == "WR" or pos == "TE":
                for row in reader:
                    if len(row) > 0:
                        row = ["0" if s == "-" else s for s in row]
                        player = clean_name(row[0]) + " " + clean_name(row[1])
                        stats[player] = [float(row[i]) for i in [9, 10, 11, 13, 14, 17, 18]]
            else:
                print("Unrecognized position.")
        else:
            print("Unrecognized source.")
        return stats


if __name__ == "__main__":
    print(clean("QB", "1", "yahoo"))
