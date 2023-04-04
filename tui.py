#!/usr/bin/python

import click
import tracker


@click.command()
@click.option('--url', default="https://er.ncsbe.gov/enr/20221108/data/results_0.txt?v=3-11-31", help='URL to track')
@click.option('--gid', default="1378", help='Group ID to track')
@click.option('--names', default=["Cheri Beasley", "Ted Budd"], help='List of names to track')
@click.option('--hw/--no-hw', default=True, help='Boolean to indicate if HAT present')
@click.option('--sim/--no-sim', default=True, help='Boolean to indicate if results should be simulated')
def track(url, gid, names, hw, sim):
    """Simple program that tracks results at a given url"""
    t1 = tracker.Tracker(
        url,
        gid,
        names,
        hw,
        sim,
    )
    # t1.update_once()
    t1.track()


if __name__ == "__main__":
    track()
