import time

from pathlib import Path

import googleapiclient.discovery
from google.oauth2 import service_account


class GDrive():
    # These scopes are required to do some actions have a look at the create sample
    # https://developers.google.com/drive/api/v3/reference/files/create
    SCOPES = ['https://www.googleapis.com/auth/drive']

    def __init__(
        self,
        logger,
        service_account_file,
    ):
        self.logger = logger
        self.credentials = service_account.Credentials.from_service_account_file(
            service_account_file, scopes=self.SCOPES)
        self.gdrive_resource = googleapiclient.discovery.build(
            'drive', 'v3', credentials=self.credentials)

    def upload_file(self, file_path, parents: [str], description=""):
        # If we have a full path then get the filename part only
        file_name = Path(file_path).name
        if not description:
            timestamp = time.strftime('%Y_%b_%d_%H_%M')
            description = f"Database back up for {file_name.split('_host')[0]} as at {timestamp}"

        file_to_create_body = {
            "description": description,
            "name": file_name,
            "parents": parents,
        }
        try:
            created_file = self.gdrive_resource.files().create(
                body=file_to_create_body, media_body=file_path).execute()
            self.logger.info(
                f"Created the file {created_file['name']}, with id {created_file['id']} in the parent google drives."
            )

        except Exception as e:
            self.logger.exception(f"Failed to create a file error :> {e}")
            raise
        # TODO: add an empty trash method for the service user
