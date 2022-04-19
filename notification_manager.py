import os
from twilio.rest import Client
import smtplib

my_email = os.environ['email']
passsword = os.environ['email_pass']
my_phone = os.environ['TO_PHONE']
sender_phone = os.environ['SENDING_PHONE']

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']


class NotificationManager:
    def __init__(self):
        self.client = Client(account_sid, auth_token)

    def send_sms(self, message):
        message = self.client.messages.create(
            body=message,
            from_=sender_phone,
            to=my_phone
        )

        print(message.sid)

    def send_emails(self, message, mail):
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=passsword)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=mail,
                msg=f"Subject:Low Price Alert\n\n{message}"
            )
