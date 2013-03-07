#!/usr/bin/env python

import datetime
import dateutil.parser
import csv

with open('2008-pres-polls.csv') as fp:
    reader = csv.reader(fp, delimiter=',')
    writer = csv.writer(open('output.csv', 'wb'))
    first = True
    for row in reader:
        if first:
            writer.writerow(["state","obama","mccain","date","pollster"])
            first = False
            continue
        state, obama, mccain, start, end, pollster = row
        start, end = start + ' 2008', end + ' 2008'
        start, end = [dateutil.parser.parse(x) for x in [start, end]]
        cur = start 
        while cur <= end:
            writer.writerow([state, obama, mccain, cur.strftime("%Y-%m-%d"), pollster])
            cur += datetime.timedelta(1)
        
            
