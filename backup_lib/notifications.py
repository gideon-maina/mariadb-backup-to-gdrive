import json

from abc import ABC, abstractmethod
from base64 import urlsafe_b64encode
from email.mime.text import MIMEText

from googleapiclient.discovery import build
from google.oauth2 import service_account


class BaseNotification(ABC):
    @abstractmethod
    def notify(self, message, to):
        """
        Abstract notify method that needs a message and a to args
        """
        pass


class GMailNotifier(BaseNotification):
    # These scopes are required to do some actions have a look at the create sample
    # https://developers.google.com/gmail/api/v1/reference/users/messages/send#python
    SCOPES = [
        'https://mail.google.com/',
        'https://www.googleapis.com/auth/gmail.send'
    ]

    def __init__(
        self,
        logger,
        service_account_file,
    ):
        self.logger = logger
        self.credentials = service_account.Credentials.from_service_account_file(
            service_account_file, scopes=self.SCOPES)
        self.gmail_service = build('gmail', 'v1', credentials=self.credentials)
        with open(service_account_file) as fh:
            f = json.load(fh)
            self.email_address = f['client_email']

    def notify(self, message, to):
        rfc_2822_message = MIMEText(message)
        rfc_2822_message['to'] = to
        rfc_2822_message['from'] = self.email_address
        rfc_2822_message['subject'] = "MariaDB Backup Notification"
        print(rfc_2822_message)
        b64_message = urlsafe_b64encode(
            rfc_2822_message.as_string().encode('utf8')).decode('utf8')
        body = {
            "raw": b64_message,
        }
        self.gmail_service.users().messages().send(userId=to,
                                                   body=body).execute()


class SlackNotifier(BaseNotification):
    def __init__(self, ):
        pass

    def notify(self, message, channel):
        pass
