#################
# Name: Jason Grant
# ID: 12430732
# Description: IOT Assignment 2: Opens the Stats file and 1) emails the results amd 2) updates Blynk
#################
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

import smtplib
import imghdr
import sys
import BlynkLib
import logging
BLYNK_AUTH = '_1YBrbat_TJksBX_p4ni9jz5gr3q62so'
# initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

logging.basicConfig(level=logging.INFO)


def send_mail(eFrom, to, subject, text, attachment):
    # SMTP Server details: update to your credentials or use class server
    smtpServer='smtp.mailgun.org'
    smtpUser='postmaster@sandbox1f89e56107b24fa68ae90b26f15714a2.mailgun.org'
    smtpPassword='2c7e61f706dfbe9ae4846b3cfc36a813-8ed21946-642dfd22'
    port=587

    # open attachment and read in as MIME image
    attachmentTest = imghdr.what(attachment)
    if attachmentTest == 'jpeg':
        fp = open(attachment, 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()
    elif attachmentTest == 'NoneType':
        print('no attachment')
        
    else:
        fp = open(attachment, 'rb')
        msgImage = MIMEText(fp.read())
        fp.close()

    #construct MIME Multipart email message
    msg = MIMEMultipart()
    msg.attach(MIMEText(text))
    if attachmentTest == 'jpeg':
        msgImage['Content-Disposition'] = 'attachment; filename="image.jpg"'
        
    msg.attach(msgImage)
    msg['Subject'] = subject

    # Authenticate with SMTP server and send
    s = smtplib.SMTP(smtpServer, port)
    s.login(smtpUser, smtpPassword)
    s.sendmail(eFrom, to, msg.as_string())
    s.quit()

date_time = sys.argv[1]

with open('ResultsFolder/GPS_Stats_1.txt', 'r') as zz:
    zz.seek(0)
    zz_emailBody = zz.readline()
    print(zz_emailBody)

send_mail('myPi@myhouse.ie', '12430732@mail.wit.ie', f'Last Activity_{date_time}_Summary', f'Just Completed an Activity ! See Summary Below: \n {zz_emailBody}  Picture From it :) See attached', f'/home/pi/Assignment_2/DB_Folder/Photo_frame_1.jpg')
blynk.log_event("finished_activity", f"You've just completed an Activity {date_time}! \n Activity Summary \n {zz_emailBody}")