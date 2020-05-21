import os
import time

from collections import defaultdict
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

    def get_db_prefix(self, db_name):
        host_name = os.uname().nodename
        return f"{db_name}_host_{host_name}_backup_at_"

    def get_db_backups_versions(self, service_account_files, databases):
        """
        Get the file versions for a db, with db_name key it's versions 
        as a list ordered with latest first
        """
        versions = defaultdict(list)
        for db in databases:
            db_prefix = self.get_db_prefix(db)
        for f in service_account_files:
            if f['mimeType'] != 'application/vnd.google-apps.folder' and f[
                    'name'].startswith(db_prefix):
                versions[db].append(f['id'])
        return versions

    def delete_backup_files(self, databases, remain_with_latest_n=5):
        """
        Delete all files for the service account except the latest, remain_with_latest_n
        files defaults to 5 above
        """
        current_files = self.gdrive_resource.files().list().execute()['files']
        file_versions = self.get_db_backups_versions(current_files, databases)
        self.logger.info(f"Current files and versions {file_versions}")
        for db, versions in file_versions.items():
            # Only delete files we have more than required latest files
            number_of_current_files = len(versions)
            if number_of_current_files > remain_with_latest_n:
                current_ids = []
                for file_id in versions:
                    current_ids.append(file_id)
                # Split list to only remain with the remain_with_latest_n file versions
                to_delete_index = len(current_ids) - remain_with_latest_n
                to_delete = current_ids[-to_delete_index:]
                self.logger.info(
                    f"About to delete the stale files {to_delete}")
                for file_id in to_delete:
                    try:
                        r = self.gdrive_resource.files().delete(
                            fileId=file_id).execute()
                        self.logger.info(
                            f"Succesfully deleted {file_id}, response {r}")
                    except Exception as e:
                        self.logger.info(
                            f"Failed to delete file {file_id}:> {e}")
                # Now clear trash
                self.logger.info(
                    self.gdrive_resource.files().emptyTrash().execute())
            else:
                self.logger.info(
                    f"There are currently the desired backup files :> {number_of_current_files}, for db :> {db.split('_')[0]}"
                )
