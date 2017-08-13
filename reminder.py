#!/usr/bin/env python3
import datetime
from email.mime.text import MIMEText
import os
import smtplib
import sqlite3

# TODO: add logging
send_user = os.environ.get('SEND_USER')
send_pwd = os.environ.get('SEND_PWD')
to_address = os.environ.get('TO_USER')


class Event:
    def __init__(self, db='events.db'):
        self.today_date = datetime.date.today()
        self.connect = sqlite3.connect(db)
        self.cursor = self.connect.cursor()

    def get_events(self, priority, timediff):
        """Collects events one week from now. Only for level 2 events"""

        if priority == 2:
            events = [x for x in self.cursor.execute(
                "SELECT * FROM events WHERE priority=?", (priority,))]
        else:
            events = [x for x in self.cursor.execute("SELECT * FROM events")]
        time_delta = datetime.timedelta(timediff)
        required_events = []
        for event in events:
            original_date = datetime.datetime.strptime(event[1], '%Y-%m-%d')
            presentday_date = datetime.date(
                self.today_date.year, original_date.month, original_date.day)
            if presentday_date - self.today_date == time_delta:
                required_events.append(event)
        return required_events

    def next_week(self):
        """Collects events one week from now. Only for level 2 events"""
        return self.get_events(2, 7)

    def tomorrow(self):
        return self.get_events(1, 1)

    def today(self):
        return self.get_events(1, 0)

    def __del__(self):
        self.cursor.close()


def insert_events_into_msg(events, msg):
    if events:
        for event in events:
            msg += "\n {} - {}".format(event[2], event[3])
        msg += "\n\n"
        return msg


def prepare_message(today_events, tomorrow_events, next_week_events):
    today_date = datetime.date.today()
    tomorrow_date = today_date + datetime.timedelta(1)
    next_week_date = today_date + datetime.timedelta(7)
    full_msg = ""
    if today_events:
        today_msg = "The following events are occuring today ({}):".format(today_date)
        full_msg += insert_events_into_msg(today_events, today_msg)
    if tomorrow_events:
        tomorrow_msg = "The following events are occuring tomorrow ({}):".format(tomorrow_date)
        full_msg += insert_events_into_msg(tomorrow_events, tomorrow_msg)
    if next_week_events:
        next_week_msg = "The following events are occuring next_week ({}):".format(next_week_date)
        full_msg += insert_events_into_msg(next_week_events, next_week_msg)
    return full_msg


    
    
def prepare_email(eventlist):
    message = "Today {} is the {} of {}. Send 'em a wish".format(
        today, eventlist[2], eventlist[1])
    msgobj = MIMEText(message)
    msgobj['Subject'] = 'Event Reminder for today ({})'.format(today)
    msgobj['From'] = send_user
    msgobj['To'] = to_address
    return msgobj


def sendemail(eventlist):
    '''arg `eventlist` is a list of 3 strings of the form [<date>,<entity>,<event>,<priority>]
    which was sent from the csvcheck fn.'''

    msgobj = prepare_email(eventlist)
    smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
    smtpserver.ehlo()
    smtpserver.starttls()
    print("Logging in now")
    smtpserver.login(send_user, send_pwd)
    print("logged in to SMTP Server")
    smtpserver.send_message(msgobj, send_user, to_address)
    print("reminder sent. Logging out.")
    smtpserver.close()


if __name__ == '__main__':
    csvcheck('events.csv')
