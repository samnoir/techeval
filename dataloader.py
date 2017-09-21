import csv
import sys
import os
import simplejson as json
import urllib.request
import time
import pprint
import re

HISTORY_URL="http://173.255.230.48:4000/history"
HISTORY_URL="http://cheesydong.pythonanywhere.com/history"

def numerize(d):
    for key, value in list(d.items()):
        if key == 'amt':
            d[key] = float(value)
        elif key == 'timestamp':
            d[key] = int(value)
    return d

class MyFilter:
    def __init__(self, instr):
        self.instr = instr
    def __enter__(self):
        print("ENTERING filter")
        return self
    def __exit__(self, a, b, c):
        print("EXITING filter")
        self.instr.close()
        return False
    def __next__(self):
        #line = next(self.instr).encode('utf-8')
        #try:
            #line = line.decode('utf-8')
            #return line
        #except UnicodeDecodeError:
            ##self.errstr.write(line)
            #line = re.sub(r'[^\x00-\x7F]+',' ', line)
            #return line.decode('utf-8')
        return next(self.instr)
    def __iter__(self):
        return self

    
start_time = time.time()
with open(sys.argv[1], encoding='latin-1') as csvfile:
    reader = csv.DictReader(csvfile)
    count = 0
    for row in reader:
        data = json.dumps(numerize(row)).encode('utf8')
        #pprint.pprint(data)
        req = urllib.request.Request(HISTORY_URL, data)
        req.add_header('Content-Type', 'application/json')
        f = urllib.request.urlopen(req)
        f.close()
        count += 1
        print(count)


#with open(sys.argv[1]) as istream, MyFilter(istream) as csvfile:
    #for line in csvfile:
        #line = line.encode('utf-8')
        #for row in csv.reader(line):
            #print(line)
    ##reader = csv.DictReader(csvfile)
    ##count = 0
    ##for row in reader:
        ##data = json.dumps(numerize(row)).encode('utf8')
        ###pprint.pprint(data)
        ##req = urllib.request.Request(HISTORY_URL, data)
        ##req.add_header('Content-Type', 'application/json')
        ##f = urllib.request.urlopen(req)
        ##f.close()
        ##count += 1
        ##print(count)
print('Elapsed time for {} = {}'.format(count, time.time() - start_time))