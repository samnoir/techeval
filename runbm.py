import urllib.request
import json
import time
import sys

HISTORY_URL="http://173.255.230.48:4000/history"
HISTORY_URL="http://cheesydong.pythonanywhere.com/history"

txn = """
{
    "sym":"USD",
    "action":"card_auth",
    "amt":49.21,
    "cuid0":"dWFH5qXl8vNw3vtt",
    "actor":"dWFH5qXl8vNw3vtt",
    "source":"dWFH5qXl8vNw3vtt",
    "note":"PARTY CITYe PlacOHUS",
    "tuid":"8BLZ-XY3E",
    "external_id":"V.27",
    "timestamp":1498867359524
}
"""
jdata = json.loads(txn)
data = json.dumps(jdata).encode('utf8')
req = urllib.request.Request(HISTORY_URL, data)
req.add_header('Content-Type', 'application/json')
total_time = 0
num_txns = 1000
if len(sys.argv) > 1:
    num_txns = int(sys.argv[1])
for i in range(num_txns):
    t = time.time()
    f = urllib.request.urlopen(req)
    t = time.time() - t
    total_time += t
    #print("ELAPSED =", t)
    #print(f.read().decode('utf-8'))
    f.close()
print('Elapsed time for {} = {}'.format(num_txns, total_time))
