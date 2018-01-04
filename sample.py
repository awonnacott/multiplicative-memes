#!/usr/bin/env python3

import os
import csv
import pdb

sources = [f for f in os.listdir() if os.path.isdir(f) and f[0] != '.']
data = {}

for source in sources:
    os.chdir(source)
    results = {}
    files = os.listdir()
    for f in files:
        with open(f, 'r') as raw:
            reader = csv.reader(raw)
            table = {}
            header = next(reader)
            for row in reader:
                table[row[1]] = dict(zip(header, row))
        results[f] = table
    data[source] = results
    os.chdir('..')

# drop to a shell
pdb.set_trace()
