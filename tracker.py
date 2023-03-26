#!/usr/bin/python

import time
import sys
import math
import json
import random
from urllib.request import Request, urlopen  # Python 3


class Tracker:
    def __init__(self, url, gid, names, hw, sim):
        # initialize the object with parameters passed to the constructor
        self.url = url  # URL of the results data page
        self.gid = gid  # ID of the race we are tracking
        self.names = names  # Strings that match the names of the candidates
        self.hw = hw  # boolean: do I have the Sense Hat hardware?
        self.sim = sim  # boolean: should I simulate changing results over time

        if self.hw:
            from sense_hat import SenseHat

            self.s = SenseHat()
            self.s.low_light = True
        # Create header for URL lib request.
        self.hdr = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
            "Accept-Encoding": "none",
            "Accept-Language": "en-US,en;q=0.8",
            "Connection": "keep-alive",
        }
        self.logo = list()  # logo will contain the image date for the LEDs
        # Define some colors
        self.blue = [0, 0, 255]
        self.red = [255, 0, 0]
        self.purple = [255, 0, 255]
        # Percentage shares
        self.cands = [0, 0]
        # Number of blue, purple, and red LEDs to light
        self.lights = [0, 0, 0]

    def get_data(self):
        req = Request(self.url, headers=self.hdr)
        page = urlopen(req, timeout=10)
        body = page.read().decode("utf-8")
        self.jsonResponse = json.loads(body)

    def parse_candidates(self):
        if self.sim:
            self.cands[0] = random.uniform(0.0, 0.95)
            self.cands[1] = 1 - self.cands[0] - 0.03
        else:
            cand_0 = [
                x
                for x in self.jsonResponse
                if (x["gid"] == self.gid and x["bnm"] in self.names[0])
            ]
            self.cands[0] = float(cand_0[0]["pct"])
            cand_1 = [
                x
                for x in self.jsonResponse
                if (x["gid"] == self.gid and x["bnm"] in self.names[1])
            ]
            self.cands[1] = float(cand_1[0]["pct"])

    def calc_lights(self):
        self.lights[0] = math.floor(self.cands[0] * 8 * 8)
        self.lights[1] = math.floor(self.cands[1] * 8 * 8)
        self.lights[2] = 8 * 8 - (self.lights[0] + self.lights[1])

    def print_data(self):
        print(
            "{:<13} {:>7.2%} | {:>2d}/64".format(
                self.names[0], self.cands[0], self.lights[0]
            )
        )
        print(
            "{:<13} {:>7.2%} | {:>2d}/64".format(
                self.names[1], self.cands[1], self.lights[1]
            )
        )
        print(
            "{:<13} {:>7.2%} | {:>2d}/64".format(
                "Und", 1 - (self.cands[0] + self.cands[1]), self.lights[2]
            )
        )
        print("")

    def form_light_list(self):
        self.logo[:] = []
        self.logo.extend([self.blue] * self.lights[0])
        self.logo.extend([self.purple] * self.lights[2])
        self.logo.extend([self.red] * self.lights[1])

    def update_once(self):
        self.get_data()
        self.parse_candidates()
        self.calc_lights()
        self.print_data()
        self.form_light_list()
        if self.hw:
            self.s.set_pixels(self.logo)

    def track(self):
        try:
            while True:
                self.update_once()
                if self.sim:
                    time.sleep(5)
                else:
                    time.sleep(10 * 60)
        except:
            self.s.clear()
            print("\nInterrupted!", sys.exc_info()[0], "occured")


def main():
    # set up a tracker for the NC Senate race in November 2022.
    t1 = Tracker(
        url="https://er.ncsbe.gov/enr/20221108/data/results_0.txt?v=3-11-31",
        gid="1378",
        names=["Cheri Beasley", "Ted Budd"],
        hw=True,
        sim=True,
    )
    # t1.update_once()
    t1.track()


if __name__ == "__main__":
    main()
