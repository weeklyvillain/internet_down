#!/usr/bin/python3

import time, smtplib, urllib.request

gmail_user = "your_email"
gmail_password = "your_password"
mail_from = "your_email"

mail_to = "ISP_mail"
subject = "some subject"
text = "Internet was down for "

timeout_interval = 5
host = "http://www.google.com/"
connection_active = True
down_time = 0


def check_connectivity(reference):
    try:
        urllib.request.urlopen(reference, timeout=1)
        return True
    except urllib.request.URLError:
        return False

def wait_for_internet():
    global down_time
    while(True):
        print("Internet is down now waiting for reconnect")
        if(check_connectivity(host)):
            break
        time.sleep(timeout_interval)
        down_time += timeout_interval
    return

def main():
    while(True):
        global connection_active
        print("Connected to internet? " + str(connection_active))
        connection_active = check_connectivity(host)
        if(not connection_active):
            wait_for_internet()
            try:
                global text
                global down_time
                text += str(down_time)
                text += " seconds."
                message = 'Subject: {}\n\n{}'.format(subject, text)
                mail = smtplib.SMTP('smtp.gmail.com', 587)
                mail.ehlo()
                mail.starttls()
                mail.login(gmail_user, gmail_password)
                mail.sendmail(mail_from, [mail_to], message)
                print("Successfully sent email")
            except SMTPException:
                print("Error: unable to send email")
            down_time = 0
        time.sleep(timeout_interval)


if __name__ == "__main__":
    main()
