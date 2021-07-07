import time
import mariadb as mdb
from datetime import datetime, timedelta
import smtplib
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

MINIMUM_LIFT_TIME = timedelta(minutes = 1)

con = mdb.connect(host='localhost',
                  user='root',
                  password='password', port=3306);
cursor =con.cursor()
now = datetime.now()
eveningStart = datetime(now.year, now.month, now.day, 19, 0, 0)
startOfDay = datetime(now.year, now.month, now.day)
cursor.execute("SELECT timestamp, value FROM build3.events WHERE build3.events.timestamp > '%s';", startOfDay)
foundLift = False
liftTime = startOfDay
brushed = False
for (timestamp, value) in cursor:
    if timestamp > eveningStart:
        if not foundLift and value == 0:
            foundLift = True
            liftTime = timestamp
        if foundLift and value == 1:
            liftPeriod = timestamp - liftTime
            if liftPeriod > MINIMUM_LIFT_TIME:
                # we're good
                brushed = True
                print("Yooooouuuur did it!")
                break
            else:
                # not a valid brush event, reset foundLift to false
                foundLift = False
            
cursor.close()
if not brushed:
    # send an email
    message = Mail(
        from_email="Smartcoaster",
        to_emails="abhishek.prasanna@outlook.com",
        subject="You forgot to brush today!",
        html_content='<p>Hi Abhishek, </p><p>It is 9 PM and you have not brushed yet. There is still time!</p>')
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print("Sending message failed!")
