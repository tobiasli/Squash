# Squash
[![Build Status](https://travis-ci.org/tobiasli/Squash.svg?branch=master)](https://travis-ci.org/tobiasli/Squash)<br/>
[![Coverage Status](https://coveralls.io/repos/tobiasli/Squash/badge.svg?branch=master&service=github)](https://coveralls.io/github/tobiasli/Squash?branch=master)

<b>Suite of scripts for booking squash sessions automatically.</b>
<br/><br/>
Define all the sessions you want to play in a config, and see Firefox book the sessions automatically.
<br/><br/>
When setup as a Scheduled Task, the script will fetch login details and session information from the yaml-config and if the squash sessions are within the booking limit (the day before the session), the program will attempt to book each session.
<br/><br/>
The program has a hardcoded court preference of 1, 6, 2, 5, 4 and 3.

## Requires
* Selenium
* Firefox

## Installation
1) Add all files to the same folder.

2) Use Windows Task Scheduler (Oppgaveplanlegging) to setup a scheduled task at 00:00 for:

```
python.exe bookingMain.py
```
3) To book a session, modify booking.yaml, and the program will attempt to book the sessions.

4) Date parsing is very flexible. "monday 17:00" will continuously attempt to book next monday at 17:00 oclock.

