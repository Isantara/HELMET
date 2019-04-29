#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Python example script showing proper use of the Cisco Sample Code header.
Copyright (c) {{current_year}} Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""


from __future__ import absolute_import, division, print_function

__author__ = "Iván Santa <isantara@cisco.com>"
__contributors__ = [
    "Daniel Tobar <dtobar@cisco.com>",
    "Alejandro Ortiz <aleortiz@cisco.com>",
]
__copyright__ = "Copyright (c) {{current_year}} Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"


import requests
import json

iox_token = "26a5c87c-c86a-433a-a440-72ba807ff426"
iox_app_id = "helmet"
metadata_payload = {
  "datapoints": {
  	"logs": {
      "units": "",
      "max": "",
      "displayName": "ALERTS",
      "graphType": "table",
      "min": ""
    },
    "pulse": {
      "units": "BPM",
      "max": "180",
      "displayName": "PULSE",
      "graphType": "gauge",
      "min": "60"
    },
    "pulseHist": {
      "units": "BPM",
      "max": "180",
      "displayName": "PULSE",
      "graphType": "line",
      "min": "60"
    },
	"gas": {
      "units": "0=OK, 1=ALERT",
      "max": "1",
      "displayName": "GAS SENSOR",
      "graphType": "gauge",
      "min": "0"
    },
	"panic": {
      "units": "0=OK, 1=ALERT",
      "max": "1",
      "displayName": "PANIC SENSOR",
      "graphType": "gauge",
      "min": "0"
    },
	"temp": {
      "units": "°C",
      "max": "100",
      "displayName": "TEMPERATURE",
      "graphType": "gauge",
      "min": "0"
    },
	"humidity": {
      "units": "%",
      "max": "100",
      "displayName": "HUMIDITY",
      "graphType": "gauge",
      "min": "0"
    },
	"helmetUse": {
      "units": "0=OK, 1=ALERT",
      "max": "1",
      "displayName": "USE OF HELMET",
      "graphType": "gauge",
      "min": "0"
    }
  }
}
headers = {"Content-Type": "application/json", "X-Token-Id": iox_token, "X-App-Id": iox_app_id}
url = "https://10.42.2.2:8443/iox/api/v2/hosting/apps/" + iox_app_id + "/ioxv/metadata"
response = requests.put(url, json=metadata_payload, headers=headers, verify=False)
#print(response)

indent = 4
print(
    __doc__,
    "Author:",
    " " * indent + __author__,
    "Contributors:",
    "\n".join([" " * indent + name for name in __contributors__]),
    "",
    __copyright__,
    "Licensed Under: " + __license__,
    sep="\n"
)