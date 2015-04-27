# -*- coding: utf-8 -*-
from __future__ import unicode_literals
'''-------------------------------------------------------------------------------
 Name:          booking.py
 Purpose:       Script for booking squash sessions at Sagene Squash and
                and affiliated courts. Uses bookingClass.py to do all the
                dirtywork.

 Author:        Tobias Litherland

 Created:       12.02.2015
 Copyright:     (c) Tobias Litherland 2015
-------------------------------------------------------------------------------'''
import os
import yaml
import bookingClass

debugging = False

path =  os.path.dirname(__file__)

with open(os.path.join(path,'booking.yaml'),'r') as config:
    bookStore = yaml.load(config)

for user in bookStore:
    b = bookingClass.main(**user)
    for session in b.sessions:

        if session.bookToday():

            if not b.browser:
                b.initiateBrowser()
            if not b.loggedIn:
                b.login()

            for booking in session.bookings:
                ok = booking.book()

    if debugging:
        b.cancelAllBookings()






