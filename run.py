import logging
import time

import schedule

from backup_lib.gdrive import GDrive
from backup_lib.backup import MariaDBBackup
from backup_lib.notifications import GMailNotifier

from config import (DB_USER, DB_PASSWORD, GDRIVE_PARENTS, DBS_TO_BACKUP,
                    TIME_TO_BACKUP, SERVICE_ACCOUNT_FILE, TARGET_DIRECTORY,
                    LATEST_BACKUPS_TO_KEEP, GMAIL_USER, GMAIL_PASSWORD,
                    FROM_EMAIL, BACKUP_EMAIL_SUBJECT,
                    NOTIFICATION_EMAIL_DESTINATION)

logger = logging.getLogger("MariaDB backup process")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.info("Starting...")


def backup_and_upload():
    gdrive = GDrive(logger, SERVICE_ACCOUNT_FILE)
    mbackup = MariaDBBackup(logger, DB_USER, DB_PASSWORD, TARGET_DIRECTORY)
    notifier = GMailNotifier(
        logger,
        GMAIL_USER,
        GMAIL_PASSWORD,
        FROM_EMAIL,
        BACKUP_EMAIL_SUBJECT,
    )
    back_ups_to_upload = set()
    try:
        logger.info("Now backing up the db files")
        summary_message_parts = []

        for db in DBS_TO_BACKUP:
            backed_up_file = mbackup.backup_database(db)
            if backed_up_file:
                back_ups_to_upload.add(backed_up_file)
                msg = f"Backed up db {db} to {backed_up_file}"
                summary_message_parts.append(msg)

        logger.info("Now uploading the backed up files")
        for back_up_file in back_ups_to_upload:
            msg = gdrive.upload_file(back_up_file, GDRIVE_PARENTS)
            summary_message_parts.append(msg)

        logger.info("Now deleting stale backups")
        gdrive.delete_backup_files(DBS_TO_BACKUP, LATEST_BACKUPS_TO_KEEP)

        logger.info("Sending notifications")
        message = '\n'.join(summary_message_parts)
        notifier.notify(message=message,
                        destination=NOTIFICATION_EMAIL_DESTINATION)
    except Exception as e:
        logger.exception(f"Could not complete successfully :> {e}")


# Run the backup only once every day at given time
schedule.every().day.at(TIME_TO_BACKUP).do(backup_and_upload)
while True:
    schedule.run_pending()
    time.sleep(1)
