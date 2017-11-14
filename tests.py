'''
We need some goddamn tests
'''

import datetime
import sqlite3
import unittest
import reminder
import random
from email.mime.text import MIMEText


# Some Helper functions

def random_string():
    '''returns a random 8 char string from the seed'''
    seed = "avadrfwqdviyrgc3rqghcjefq34reiughsogh7sddasagkasergwfhcggbaskaeteu"
    return ''.join(random.sample(seed, 8))


def create_random_table(cursor):
    '''creates an events table in test db and populates it with a random event
    for each day. Year 2013 is used.
    '''
    cursor.execute('''CREATE TABLE events (
                      serial int NOT NULL PRIMARY KEY,
                      eventdate date,
                      name varchar,
                      event varchar,
                      priority int)
                   ''')
    adate = datetime.date(2013, 1, 1)
    day_inc = datetime.timedelta(1)
    for serial in range(1, 366):
        # priority 1 entries
        cursor.execute("INSERT INTO events VALUES(?,?,?,?,?)",
                       (serial,
                        adate.strftime("%Y-%m-%d"),
                        random_string(),
                        random_string() + " Day",
                        1,
                        )
                       )

        # priority 2 entries
        cursor.execute("INSERT INTO events VALUES(?,?,?,?,?)",
                       (serial + 366,
                        adate.strftime("%Y-%m-%d"),
                        random_string(),
                        random_string() + " Day",
                        2,
                        )
                       )

        adate += day_inc


def check_for_table(cursor):
    '''Checks if the events table exists in the test db.
    '''

    check = cursor.execute(
        "SELECT name FROM sqlite_master where type='table' and name='events'")
    if check.fetchone():
        return True
    else:
        return False


def check_test_db():
    '''calls check_for_table on given test db. If returned false, calls
    create_random_table.
    '''

    conn = sqlite3.connect('tests.db')
    cursor = conn.cursor()
    if not check_for_table(cursor):
        create_random_table(cursor)
    conn.commit()
    conn.close()

# Test code starts here (Thanks captain obvious!)
class EventClassTests(unittest.TestCase):
    def setUp(self):
        check_test_db()
        self.test_instance = reminder.Event('tests.db')
        self.today = datetime.date.today()

    def test_db_connection(self):
        self.assertIsInstance(self.test_instance.cursor, sqlite3.Cursor)
        
    def test_get_events(self):
        timediff = random.choice([0, 1, 7])
        priority = random.choice([1, 2])
        eventlist = self.test_instance.get_events(priority, timediff)
        print("1: ", eventlist)
        self.assertIsInstance(eventlist, list)

    def general_checks(self, eventlist, days_to_event):
        if eventlist:
            print(eventlist)
            self.assertIsInstance(eventlist[0], tuple)
            test_date = datetime.datetime.strptime(eventlist[0][1], "%Y-%m-%d")
            future_date = self.today + datetime.timedelta(days_to_event)
            self.assertEqual(test_date.day, future_date.day)
            self.assertEqual(test_date.month, future_date.month)

    def test_next_week(self):
        eventlist = self.test_instance.next_week()
        self.general_checks(eventlist, 7)

    def test_tomorrow(self):
        eventlist = self.test_instance.tomorrow()
        self.general_checks(eventlist, 1)

    def test_today(self):
        eventlist = self.test_instance.today()
        self.general_checks(eventlist, 0)

    def TearDown(self):
        del test_instance


class EmailAndMsgModulesTests(unittest.TestCase):
    def setUp(self):
        check_test_db()
        self.test_instance = reminder.Event('tests.db')
        self.today_events = self.test_instance.today()
        self.tomorrow_events = self.test_instance.tomorrow()
        self.next_week_events = self.test_instance.next_week()

    def test_insert_events_into_msg(self):
        test_msg = "The sample events are:"
        timediff = random.choice([0, 1, 7])
        priority = random.choice([1, 2])
        # eventlist obtained will be different each time...
        # ...since we are doing the above random selection.
        eventlist = self.test_instance.get_events(priority, timediff)
        test_msg = reminder.insert_events_into_msg(eventlist, test_msg)
        self.assertIsInstance(test_msg, str)
        print("msg formatting: \n" + test_msg)

    def test_prepare_message(self):
        full_msg = reminder.prepare_message(self.today_events,
                                                 self.tomorrow_events,
                                                 self.next_week_events)
        self.assertIsInstance(full_msg, str)
        print(self.full_msg)

    def test_prepare_email(self):
        full_msg = reminder.prepare_message(self.today_events,
                                                 self.tomorrow_events,
                                                 self.next_week_events)
        msgobj = reminder.prepare_email(full_msg)
        self.assertIsInstance(msgobj, MIMEText)
        self.assertEqual(msgobj['From'], reminder.send_user)
        self.assertEqual(msgobj['To'], reminder.to_address)

    def test_sendemail(self):
        # probably needs a mock. but eh ¯\_(ツ)_/¯
        # The following crap can't be used for testing offline.
        # It was just to verify that it was working.
        # Don't bother unit testing this without a mock for the mail server.
        # full_msg = reminder.prepare_message(self.today_events,
        #                                          self.tomorrow_events,
        #                                          self.next_week_events)
        # msgobj = reminder.prepare_email(full_msg)
        # testoutput = reminder.sendemail(msgobj)
        # print(testoutput)
        pass

if __name__ == "__main__":
    unittest.main()
