# Squash
<b>Suite of scripts for booking squash sessions automatically.</b>
<br/><br/>
Define all the sessions you want to play in a config, and see Firefox book the sessions automatically.
<br/><br/>
When setup as a Scheduled Task, the script will fetch login details and session information from the yaml-config and if the squash sessions are within the booking limit (the day before the session), the program will attempt to book each session.
<br/><br/>
The program has a hardcoded court preference of 1, 6, 2, 5, 4 and 3.

## Prerequisites
<b>Programs:</b>
<ul>
<li>Anaconda Python 3.4</li>
<li>Firefox</li>
</ul>
<b>Modules not included in Anaconda:</b>
<ul>
<li>Selenium</li>
</ul>
Install Selenium via Anaconda Command Prompt:
```
>> conda install selenium
```
## Installation
<nl>
<li>Add all files to the same folder.</li>
<li>Use Windows Task Scheduler (Oppgaveplanlegging) to setup a scheduled task at 00:00 for:</li>
</nl>
```
>> C:\Anaconda\python.exe C:\somepath\bookingMain.py
```



