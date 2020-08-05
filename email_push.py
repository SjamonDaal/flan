import smtplib
import sys
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date

today = date.today().strftime("%d %B %Y")
filename = sys.argv[1]

try:
    if filename.endswith('.xml'):
        print("Exits for .xml files.")
        exit()

    report_file = open(filename)
    html = report_file.read()

    # me == my email address
    # you == recipient's email address
    me = "{} <{}>".format((os.getenv('smtp_from_name') or "Flan Scan"), os.getenv('smtp_from'))
    you = os.getenv('smtp_to')


    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Flan Scan - {}".format(today)
    msg['From'] = me
    msg['To'] = you

    # Create the body of the message (a plain-text and an HTML version).
    text = "Hi!\n\nAre you back in the 90s?\nOpen this e-mail in HTML to read this report."

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # Send the message via local SMTP server.
    server = smtplib.SMTP(os.getenv('smtp_server'), (os.getenv('smtp_port') or 25))

    server.sendmail(me, you, msg.as_string())
    server.quit()

except Exception as e:
    print('Error sending email')
    print(e)
