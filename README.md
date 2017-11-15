# emreminder

Send email reminders to yourself.

Do you have a server that's just sitting around 24x7 doing nothing? Do you want it to be
doing some useful work like taking out the garbage and washing your clothes? Well this
program won't do that. But it will send you reminders for events to your email so you
won't have to deal with fancy apps with fancy features to remind you of things ever again!

This program is as rudimentary as reminder programs come:
1. Only 2 priority levels.
2. Reminders are sent only for events today, tomorrow and next week.
3. Reminders are sent only once a day (or more. You are the one setting the cronjob for it).
4. All events are in a single sqlite database.
5. No fancy GUI's! Only interaction is a csv file and the commandline.

# Instructions

1. Rename the files `exampleevents.csv` and `exampleconfig.py` to `events.csv` and
   `config.py` respectively.
2. In `events.csv` add the events you want in the format `serial no,YYYY-MM-DD,person
   name,event name,priority value (1 or 2)`.
   * Priority 1 are events whose reminders are sent on the day before and on the day of
     the events.
   * Priority 2 are events whose reminders are sent 7 days before, the day before and the
     day of the events.
3. run `python3 addtodb.py`. This creates the sqlite database in the current directory and
   populates it with the events from the csv file.
4. Open `config.py` and replace the values of the variables as appropriate. 
   * __IMPORTANT__: The sender account must be a gmail account where access to insecure apps has been
     turned ON.
5. Run `chmod +x reminder.py` to make the program executable.
6. Add a cronjob pointing to the path of reminder.py.

Aaaaannd you're done. Easy!
