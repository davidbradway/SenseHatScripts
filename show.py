import time
import math
import json
import random
from urllib.request import Request, urlopen  # Python 3
hw = True
if hw:
    from sense_hat import SenseHat
    s = SenseHat()
    s.low_light = True
# View HTML: https://er.ncsbe.gov/?election_dt=11/08/2022&county_id=0&office=FED&contest=0
url = 'https://er.ncsbe.gov/enr/20221108/data/results_0.txt?v=3-11-31'
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
   'Accept-Encoding': 'none',
   'Accept-Language': 'en-US,en;q=0.8',
   'Connection': 'keep-alive'}
logo = list()
blue = [0, 0, 255]
red = [255, 0, 0]
purple = [255, 0, 255]


def get_data(link):
    req = Request(link, headers=hdr)
    page = urlopen(req, timeout=10)
    body = page.read().decode('utf-8')
    jsonResponse = json.loads(body)
    return jsonResponse
    #pass


def election():
    jsonResponse = get_data(url)
    beasley_list = [x for x in jsonResponse if (x['gid'] == '1378' and x['bnm'] in ['Cheri Beasley'])]
    beasley = float(beasley_list[0]['pct'])
    #beasley = random.random()
    budd_list = [x for x in jsonResponse if (x['gid'] == '1378' and x['bnm'] in ['Ted Budd'])]
    budd = float(budd_list[0]['pct'])
    #budd = 1 - beasley - .05
    dems = math.floor(beasley * 8 * 8)
    reps = math.floor(budd * 8 * 8)
    und = 8 * 8 - (dems + reps)
    print("{:<7} {:>7.2%} | {:>2d}/64".format("Beasley", beasley, dems))
    print("{:<7} {:>7.2%} | {:>2d}/64".format("Budd", budd, reps))
    print("{:<7} {:>7.2%} | {:>2d}/64".format("Und", 1 - (budd + beasley), und))
    logo[:] = []
    logo.extend([blue] * dems)
    logo.extend([purple] * und)
    logo.extend([red] * reps)
    return logo

images = [election]
count = 0

try:
    while True:
        if hw:
            s.set_pixels(images[count % len(images)]())
        time.sleep(10*60)
        count += 1
except KeyboardInterrupt:
    s.clear()
    print('\ninterrupted!')
