#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import logging
from datetime import datetime,timedelta
from syslog import syslog,LOG_INFO,LOG_ERR

import time
import tzlocal
import pytz
from nlindb import connectInflux
import traceback

from miio import AirPurifier
from miio.airpurifier import (
    AirPurifierException,
    AirPurifierStatus,
    FilterType,
    LedBrightness,
    OperationMode,
    SleepMode,
)

ut = int(time.time())
tz = tzlocal.get_localzone()
tdt = tz.localize(datetime.fromtimestamp(ut))
tdtz = tdt.astimezone(pytz.utc)

# 264b7833c3eeffecc50e69d717f39d41
# zhimi.airpurifier.v7

g_apuri = AirPurifier('192.168.0.10', '260f033938f0b21c3ebf316a8873a30e')

sts = g_apuri.status()

fdata = {}
fdata["power"] = 1 if sts.power == "on" else 0
fdata["aqi"] = sts.aqi
fdata["average_aqi"] = sts.average_aqi
fdata["temperature"] = float(sts.temperature)
fdata["humidity"] = float(sts.humidity)
fdata["filter_life_ramaining"] = sts.filter_life_remaining
fdata["filter_hours_used"] = sts.filter_hours_used
fdata["motor_speed"]=sts.motor_speed
fdata["motor2_speed"]=sts.motor2_speed
fdata["volume"]=sts.volume

indb = connectInflux('icu')

nameMeasurement = 'xiaomiaq' 


sdtz = tdtz.strftime('%Y-%m-%dT%H:%M:%SZ')
print(sdtz)
json_body = [
    {
	"measurement": nameMeasurement,
	"tags": {
            "room": "kj423"
	},
	"time": sdtz,
	"fields": fdata
    }
]
print("JSON=",json_body)
try:
  res=indb.write_points(json_body)
  print("AIR res=",res)
except:
  traceback.print_exc()

