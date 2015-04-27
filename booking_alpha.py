'''
Script for automatic booking of squash courts for sagene squash.

Use selenium for navigating javascript pages.

'''
import time
import datetime
import dateParse3
import copy
from selenium import webdriver

spillestart = '12.02.2015 17:00'
spillelengde = 60 #minutter
spillere = ['Finn Kristian Rognstad']

ukedager = {
        0:'Mandag',
        1:'Tirsdag',
        2:'Onsdag',
        3:'Torsdag',
        4:'Fredag',
        5:'Lørdag',
        6:'Søndag',
    }

dontBook = False

baneprioritet = [1,6,2,5,4,3]

#Tider:
start=dateParse3.parse(spillestart)
lengde = datetime.timedelta(minutes=spillelengde)
leie = datetime.timedelta(minutes=30)

#Create date string: Søndag - 08.02.2015
dag = '%s - %02d.%02d.%d' % (ukedager[start.weekday()],start.day,start.month,start.year)

#Create time match string: 15:00 - 15:30 Bane 4 Bestille
count = 0
timer = []
while start+lengde>start+leie*count:
    count += 1
    first = start + leie*(count-1)
    last = start+leie*count
    timer += ['%02d:%02d - %02d:%02d Bane %%d Bestille' % (first.hour,first.minute,last.hour,last.minute)]

url = 'http://sagenesquash.bestille.no'

browser = webdriver.Firefox()

browser.get(url)

time.sleep(2)

##Login
browser.find_element_by_partial_link_text('logg inn').click()

time.sleep(2)

#Username
browser.find_element_by_id('mainContent_ctlLogin_txtEmail').send_keys('tobiaslland@gmail.com')
#Password
browser.find_element_by_id('mainContent_ctlLogin_txtPin').send_keys('9215')
#Click
browser.find_element_by_id('mainContent_btnLogin').click()

##Booking
time.sleep(2)

#Få opp ledige baner
browser.find_element_by_link_text('Oppgaver').click()
browser.find_element_by_partial_link_text('Sesongkort').click()
time.sleep(2)
browser.find_element_by_id('view-list').click()
browser.find_element_by_id('searchButton').click()
time.sleep(2)

#Find ledige baner med dag og tid
stillMorePages = True

ledigBooking = []
prioritereSamme = []

print('Sjekker ledige...')
dager = browser.find_elements_by_tag_name('h2')
tider = browser.find_elements_by_tag_name('table')
tider.pop(0)
tider.pop(0)

for d,tid in zip(dager,tider):
    if d.text == dag:
        ledig = [t.text for t in tid.find_elements_by_class_name('search-result')]
        for t in timer:
            for b in prioritereSamme + baneprioritet:
                if t % b in ledig:
                    ledigBooking += [t % b]
                    prioritereSamme += [b]
                    break
                    
print('Funnet ledige:')
print(ledigBooking)
                    



print('Booker timer...')

for ledigB in ledigBooking:
    browser.find_element_by_link_text('Oppgaver').click()
    browser.find_element_by_partial_link_text('Sesongkort').click()
    time.sleep(2)
    browser.find_element_by_id('view-list').click()
    browser.find_element_by_id('searchButton').click()
    time.sleep(2)
    
    found = False
    stillMorePages = True
    dager = browser.find_elements_by_tag_name('h2')
    tider = browser.find_elements_by_tag_name('table')
    tider.pop(0)
    tider.pop(0)
    
    for d,tid in zip(dager,tider):
        if d.text == dag:
            for t in tid.find_elements_by_class_name('search-result'):
                if t.text == ledigB:
                    bookedTime = copy.deepcopy(t.text)
                    t.click()
                    time.sleep(2)
                    browser.find_element_by_id('Note2').send_keys(', '.join(spillere))
                    if not dontBook:
                        browser.find_element_by_id('btnNext').click()
                    time.sleep(2)
                    print('Booked %s' % bookedTime)
                    found = True
                if found: break
        if found: break
            
    if not found:
        print('Ikke funnet %s' % ledigB)
        raise Exception('Booking not found!! Wooot!')


