# About

This application is used to bypass the Dexcom Share server for [Looping](https://github.com/LoopKit/Loop/), there may be other reasons to use it as well.
This is an alternative to dabear's [NightScoutShareServer](https://github.com/dabear/NightscoutShareServer). 

This application will take the values from your NightScout website, and convert the JSON into a Dexcom Share friendly formatting for use with Loop.

# Prerequisites

1. Existing NightScout server running.
2. Python3

# Instructions

1. Fork this repository if you want, and clone it to your local machine.
2. Go into the directory you just cloned and create a virtual environment:
    * `$ python3 -m venv env`
3. Activate virtual environment
    * `$ source env/bin/activate`
4. Install python modules
    * `$ pip install flask arrow`
    * `$ pip install git+https://github.com/ps2/python-nightscout.git`

# Optional API Authorization
If you have your NightScout variable `AUTH_DEFAULT_ROLES = denied` and would still like to use this app, you will need to make some changes.

1. Go to http://www.sha1-online.com and get the SHA1 hash of your `API_SECRET` from your NightScout Variables.
2. Edit line 17 of app.py `url = base_url + '/pebble?secret=[SHA1HASH]&count=' + count + '&units=mgdl’` replacing `[SHA1HASH]` with the value that you copied from step 1.


At this point, you want to setup the application for use, you need to edit app.py and change the values on lines 11,12, and 13

`nightscout_url = `http://yournightscout.website.domain'`

Server host = 0.0.0.0 if you want it to listen to all ip addresses on an interface, or you can set it to a specific IP, whether it be public or private.

`server_host = ‘0.0.0.0’`

You change the port, to whatever you want the application to listen on.

`server_port = ‘5000’`

Next, you need to modify your Loop code:

`Loop/Models/ServiceAuthentication/ShareService.swift`

Uncomment lines 55 and 62

Next edit line 56 and change the host and port to match what you put in your DexcomShareServer

`let customServer = "http://server_host_ip_or_domain:5000"`

Go ahead and start the Dexcom_Bridge

`$ python3 app.py`

I prefer to run it in a screen session, and disconnect from the screen, you could probably output everything to /dev/null if you wanted and throw it in the background.

Now, after you recompile Loop and push it to your phone. In the Dexcom Share Server, scroll down and select “custom” and you can choose any user/pass you want to use. (I put in a random user/pass).

Watch your Loop, make sure it’s pulling numbers, but at this point, it should be polling every 5 minutes, and pull the numbers from this bridge instead of using Dexcom’s systems.

# Thanks:
[dabear](https://github.com/dabear/) - He made the initial code, this was just a port.
