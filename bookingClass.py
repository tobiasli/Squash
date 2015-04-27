# -*- coding: utf-8 -*-
from __future__ import unicode_literals
'''-------------------------------------------------------------------------------
 Name:          bookingClass.py
 Purpose:       Class for booking squash sessions. At sagene squash.

 Author:        Tobias Litherland

 Created:       12.02.2015
 Copyright:     (c) Tobias Litherland 2015
-------------------------------------------------------------------------------'''

import datetime
import copy
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

import dateParse #Homemade module for intelligent parcing of dates.

# Various constants:
defaultCourtRental = datetime.timedelta(minutes=30) #minutes
courtPriority = [1,6,2,5,4,3]
weekdays = {
        0:'Mandag',
        1:'Tirsdag',
        2:'Onsdag',
        3:'Torsdag',
        4:'Fredag',
        5:'Lørdag',
        6:'Søndag',
    }
validBookingTimeBeforeSession = datetime.timedelta(days = 1)
maximumBookingAttemptsBeforeFail = 2

class main(object):
    #Main class. Can contain several session-objects that in turn contain
    #booking-objects for each individual court booking. main handles browser and
    #login, booking

    def __init__(self,url,login,sessions,browser = 'Firefox'):
        '''
        url         string, url of main booking page.
        login       struct:
                        user        string
                        password    string
        sessions    list of structs:
                        time        string, start of session
                        length      integer, number of minutes of play
                        partners    string, other player(s)

        browser     string, the browser used for booking. Must be installed seperately.
        '''

        self.url = url
        self.loginInfo = login
        self.sessions = [self._session(self,**details) for details in sessions]
        self.browserType = browser
        self.browser = []
        self.loggedIn = False

    def login(self):
        ##Login
        element = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT,'logg inn')))
        self.browser.find_element_by_partial_link_text('logg inn').click()

        element = self.wait.until(EC.element_to_be_clickable((By.ID,'mainContent_ctlLogin_txtEmail')))
        #Username
        self.browser.find_element_by_id('mainContent_ctlLogin_txtEmail').send_keys(self.loginInfo['username'])
        #Password
        self.browser.find_element_by_id('mainContent_ctlLogin_txtPin').send_keys(self.loginInfo['password'])
        #Click
        self.browser.find_element_by_id('mainContent_btnLogin').click()

    def initiateBrowser(self):
        self.browser = eval('webdriver.%s()' % self.browserType)
        self.browser.get(self.url)
        self.wait = WebDriverWait(self.browser, 10) #Default wait in seconds before assumed timeout.

    def cancelAllBookings(self):
        #Cancel all bookings found on the user. Primarily used for debugging purposes.
        self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT,'Min Side'))).click()
        self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT,'Avbestille time'))).click()

        canceledAll = False

        while not canceledAll:
            #Cancel entries, one at a time, until there are non left.
            self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT,'Avbestille')))

            try:
                cancelCourt = self.browser.find_elements_by_link_text('Avbestille')
            except:
                canceledAll = True

            cancelCourt[0].click()
            self.wait.until(EC.element_to_be_clickable((By.ID,'mainContent_btnYes'))).click()

    class _session(object):
    #Class that handles en entire session. Contains several booking-objects.
    #Handles time and court

        def __init__(self,parent,time,length,partners,comment):
            self.main = parent
            self.time = dateParse.parse(time)
            self.length = datetime.timedelta(minutes=length)

            if isinstance(partners,list):
                partners = ', '.join(partners)

            self.partners = partners
            self.comment = comment

            self.day = '%s - %02d.%02d.%d' % (weekdays[self.time.weekday()],self.time.day,self.time.month,self.time.year)

            self.courtPriority = copy.deepcopy(courtPriority)

            self.bookings = self._parseSessionsInBooking()

        def bookToday(self):
            if datetime.datetime.today().date() == self.time.date()-validBookingTimeBeforeSession:
                return True
            else:
                return False

        def _parseSessionsInBooking(self):
            count = 0
            bookings = []
            while self.time+self.length>self.time+defaultCourtRental*count:
                count += 1
                first = self.time + defaultCourtRental*(count-1)
                last = self.time+defaultCourtRental*count

                bookings += [self.booking(self,first,last)]
            return bookings

        class booking(object):
        #Class that handles booking of a single booking.
            def __init__(self,parent,first,last):
                self.session = parent
                self.first = first
                self.last = last

            def book(self):
                tryCount = 0
                courtFound = False
                while tryCount <= maximumBookingAttemptsBeforeFail:

                    self.session.main.wait.until(EC.element_to_be_clickable((By.LINK_TEXT,'Oppgaver'))).click()
                    self.session.main.wait.until(EC.element_to_be_clickable((By.LINK_TEXT,'Sesongkort'))).click()

                    self.session.main.wait.until(EC.text_to_be_present_in_element((By.ID,'service_selectedTxt'),'Sesongkort'))

                    self.session.main.wait.until(EC.element_to_be_clickable((By.ID,'view-list'))).click()
                    self.session.main.wait.until(EC.element_to_be_clickable((By.ID,'searchButton'))).click()

                    element = self.session.main.wait.until(EC.presence_of_element_located((By.TAG_NAME,'h2')))
                    element = self.session.main.wait.until(EC.presence_of_element_located((By.TAG_NAME,'table')))

                    days = self.session.main.browser.find_elements_by_tag_name('h2')
                    sessionsPrDay = self.session.main.browser.find_elements_by_tag_name('table')

                    #The two first tables on the page are empty and need to be removed from the results list:
                    sessionsPrDay.pop(0)
                    sessionsPrDay.pop(0)

                    courtTimes = []
                    for court in self.session.courtPriority:
                        courtTimes += ['%02d:%02d - %02d:%02d Bane %d Bestille' % (self.first.hour,self.first.minute,self.last.hour,self.last.minute,court)]

                    for d,sessionsThisDay in zip(days,sessionsPrDay):
                        if d.text == self.session.day:
                            candidates = []
                            #Get candidates:
                            for t in sessionsThisDay.find_elements_by_class_name('search-result'):
                                if t.text in courtTimes:
                                    candidates += [t]
                                    courtFound = True

                            if not courtFound:
                                print 'Booking for %s %02d:%02d - %02d:%02d not found' % (self.session.day,self.first.hour,self.first.minute,self.last.hour,self.last.minute)
                                return False

                            #Check candidates and book most preferable court:
                            for courtTime,court in zip(courtTimes,self.session.courtPriority):
                                for t in candidates:
                                    if t.text == courtTime:
                                        bookedTime = copy.deepcopy(t.text)
                                        t.click()

                                        self.session.main.wait.until(EC.presence_of_element_located((By.ID,'Note1'))).send_keys(self.session.comment)
                                        self.session.main.wait.until(EC.presence_of_element_located((By.ID,'Note2'))).send_keys(self.session.partners)
                                        self.session.main.wait.until(EC.presence_of_element_located((By.ID,'btnNext'))).click()

                                        #Verify that page reached is actually receipt for booking. If not continue to next court.
                                        #
                                        if self.session.main.wait.until(EC.presence_of_element_located((By.ID,'mainContent_ShowActivityInfo1_lblHeader'))).text == 'Timen er bekreftet!':
                                            print('Booked %s' % bookedTime)
                                            self.session.courtPriority = [court]+self.session.courtPriority
                                            return True
                                        else:
                                            if tryCount < maximumBookingAttemptsBeforeFail:
                                                print 'Try %d for %s Errored out. Retry booking (max %d tries).' % (tryCount,bookedTime,maxTries)
                                            else:
                                                print 'Booking for %s errored for the last time. Aborted.' % bookedTime
                    tryCount += 1
                return False