# H.E.L.M.E.T.

Project for Americas SE Innovation Challenge


## Business/Technical Challenge

"I am tremendously excited about Mining.  I have been to my mandatory set of 8 sessions, and I don’t have to reiterate the investment, opportunity, Investments, Picture of Environment, Opportunities to insert Cisco technology that exec after exec has highlighted in Mining.  Whether it is our solutions that have played no small part at Dundee Precious Metals quadrupling their production, or at Freeport McMoran as they have used Big Data analytics for predictive maintenance and other capabilities, or with BHP Billiton and Rio Tinto in Australia for Autonomous (driverless) Truck Operations and Remote Operations, Cisco has played a large part in helping our customers reach their business outcomes, and we will continue to do so. This is a $4 Bn. TAM for Cisco, growing at 15% CAGR.  This is Big.  And it is Now." Paco Bolaños
The purpose of this project is saving lives, not only in mining, but also in other verticals. 
The helmet is the main element for protection of persons in many verticals. People are exposed to many type of dangers, not only blows to the head; for example dangerous gases, high temperature, low or high humidity, incomunication, and all of these can create heart problems.
But could the helmet do more for save lives?
Could a helmet use the Cisco solutions to save lives?
H.E.L.M.E.T. can.

## Proposed Solution

We desing and implement a helmet that sends data to IOx dashboard, and also send alerts to webex teams spaces.
The name is H.E.L.M.E.T. for Health Enviromental and Location Monitoring Equipment with Telemetry
Health part is done by the Heartbeat sensor, and helmet wearing sensor.
Enviromental part is done by temperature and humidity sensor.
Location part is done with Meraki location analytics (the helmet is connected using wifi, and also has bluetooth)
Telemetry part is done with the IOx dashboard on an IR829 gateway where the data is sent by the helmet.


### Cisco Products Technologies/ Services

Our solution will levegerage the following Cisco technologies:

* [Webex Teams](https://www.cisco.com/c/es_co/solutions/collaboration/webex-teams.html)
* [Cisco IOx with IR829](https://www.cisco.com/c/en/us/products/cloud-systems-management/iox/index.html)
* [Meraki Wireless](http://cisco.com/go/meraki)

Our solutions also uses hardware to collect data and send to APIs:
* Raspberry Pi 3 B+
* Arduino Pro Micro
* Sensor for heartbeat (pulsesensor.com), use of the helmet (LDR), temperature, humidity (DHT11), gases MQ-2 (with buzzer and led alerts), and panic button.
* Battery solution.

## Team Members

* Iván Santa <isantara@cisco.com> - Lab Admin Medellín, acting as SE for Commercial LoB.
* Daniel Tobar <dtobar@cisco.com> - SE for Commercial LoB.
* Alejandro Ortiz <aleortiz@cisco.com> - SE for Enterprise and Public Sector LoB.


## Solution Components

The main components of the software solution are python3 (requests, json, serial, Adafruit_DHT and RPi libraries), IOx Rest APIs and Webex Teams REST APIs.


## Usage

For use this solution you need to connect all sensor to the Raspberry Pi (we are working on the manual), install the dependencies, and clone this project.
Configure the IR829 like the running config here.
Connect an AP to the IR829 on port GE1, and a SIM card to slot 0.
Then deploy the docker container package.tar, and get the token and run metadata.py to create de dashboard.
Then you only need to run HELMET.py.

## Architecture
Download
[HELP - Arch - Innovation Challenge Latam.pdf]()

## VIDEOS
https://www.youtube.com/watch?v=Bxe4f8BBA24
https://www.youtube.com/watch?v=MGL2xpnnAd8
https://www.youtube.com/watch?v=osEagpTWWNk

## Installation

TBA

## Documentation

TBA

## License

Provided under Cisco Sample Code License, for details see [LICENSE](./LICENSE.md)

## Code of Conduct

Our code of conduct is available [here](./CODE_OF_CONDUCT.md)

## Contributing

See our contributing guidelines [here](./CONTRIBUTING.md)




