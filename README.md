# Squash
Suite of scripts for booking squash sessions.
<br/><br/>
The point of this package is to be set up as an autorun service that reads the *.yaml config containing user logins and the sessions the player wants to play.
<br/><br/>
If the booking time is available for booking, the script will complete the booking by fireing up a Selenium firefox session and open the booking page for Sagene Squash and perform the booking operations. Bookings will be performed on prefered courts.
<br/>
<br/>
Dependencies:
<ul>
<li>Anaconda Python 2.7</li>
<li>Selenium</li>
<li>Firefox</li>
</ul>
