'''
----------------------------------------------------------------------
Test module for squash booking module booking.py
----------------------------------------------------------------------

'''

import unittest

class TestSquashModule(unittest.TestCase):

    def test_booking(self):
        import bookingClass
        import os
        import yaml
        import bookingClass
        import codecs

        bookingClass.test_mode = True

        debugging = False

        path =  os.path.dirname(__file__)

        with codecs.open(os.path.join(path,'booking.yaml'),'r', encoding = 'utf-8') as config:
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
                        ok = booking.book() # Don't book in debug mode.

            if debugging:
                b.cancelAllBookings()

            if b.browser:
                b.browser.quit()





def run():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSquashModule)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    run()