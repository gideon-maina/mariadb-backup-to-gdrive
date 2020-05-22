import json
import smtplib

from abc import ABC, abstractmethod
from base64 import urlsafe_b64encode
from email.mime.text import MIMEText

from googleapiclient.discovery import build
from google.oauth2 import service_account


class BaseNotification(ABC):
    @abstractmethod
    def notify(self, message, destination):
        """
        Abstract notify method that needs a message and destination args
        """
        pass


class GMailNotifier(BaseNotification):
    def __init__(
        self,
        logger,
        gmail_user,
        gmail_password,
        from_address,
        backup_email_subject,
    ):
        self.logger = logger
        self.gmail_user = gmail_user
        self.gmail_password = gmail_password
        self.backup_email_subject = backup_email_subject
        self.email_address = from_address

    def notify(self, message, destination):
        rfc_2822_message = MIMEText(message)
        # if we have a list of emails then expand them`
        if isinstance(destination, list):
            rfc_2822_message['to'] = ",".join(destination)
        else:
            rfc_2822_message['to'] = destination
        rfc_2822_message['from'] = self.email_address
        rfc_2822_message['subject'] = self.backup_email_subject
        try:
            server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server_ssl.login(self.gmail_user, self.gmail_password)
            server_ssl.send_message(rfc_2822_message)
            server_ssl.close()
            self.logger.info(f"Sent an email notification to {destination}")
        except Exception as e:
            self.logger.exception(f"Failed to send notification email :> {e}")
            raise


class SlackNotifier(BaseNotification):
    def __init__(self, ):
        pass

    def notify(self, message, destination):
        pass
