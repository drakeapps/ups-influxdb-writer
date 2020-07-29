#!/usr/bin/env python3

import time
import os
import argparse
from nut2 import PyNUTClient
from influxdb import InfluxDBClient


parser = argparse.ArgumentParser(description='UPS Influx DB Writer')
parser.add_argument("--ups_name", help="UPS Name. Name that the NUT driver uses to access the UPS")
parser.add_argument("--influx_host", help="InfluxDB Host")
parser.add_argument("--influx_port", help="InfluxDB Port")
parser.add_argument("--influx_db", help="InfluxDB Database")

args = parser.parse_args()

ups_name = args.ups_name
influx_host = args.influx_host
influx_port = args.influx_port
influx_db = args.influx_db


os.system('mkdir -m 2750 /dev/shm/nut')
os.system('chown $USER.$GROUP /dev/shm/nut')
#[ -e /var/run/nut ] || ln -s /dev/shm/nut /var/run
# Issue #15 - change pid warning message from "No such file" to "Ignoring"
os.system('echo 0 > /var/run/nut/upsd.pid && chown $USER.$GROUP /var/run/nut/upsd.pid')
os.system('echo 0 > /var/run/upsmon.pid')

os.system('upsdrvctl -u root start')
os.system('upsd -u $USER')
os.system('upsmon -D &')

while 1:
    client = PyNUTClient()

    fields = {}
    for var in client.list_vars(ups_name):
        value = client.get_var(ups_name, var)
        try:
            fields[var] = float(value)
        except:
            fields[var] = value


    measurement = [
        {
            'measurement': 'ups',
            'fields': fields
        }
    ]


    influx_client = InfluxDBClient(influx_host, influx_port, database=influx_db)
    influx_client.create_database(influx_db)

    influx_client.write_points(measurement)

    time.sleep(15)
