import logging

from backup_lib.gdrive import GDrive
from backup_lib.backup import MariaDBBackup
from config import (DB_USER, DB_PASSWORD, GDRIVE_PARENTS, DBS_TO_BACKUP,
                    SERVICE_ACCOUNT_FILE, TARGET_DIRECTORY)

logger = logging.getLogger("MariaDB backup process")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

if __name__ == "__main__":
    gdrive = GDrive(logger, SERVICE_ACCOUNT_FILE)
    mbackup = MariaDBBackup(logger, DB_USER, DB_PASSWORD, TARGET_DIRECTORY)
    back_ups_to_upload = set()
    try:
        logger.info("Now backing up the db files")
        for db in DBS_TO_BACKUP:
            backed_up_file = mbackup.backup_database(db)
            if backed_up_file:
                back_ups_to_upload.add(backed_up_file)

        logger.info("Now uploading the backed up files")
        for back_up_file in back_ups_to_upload:
            gdrive.upload_file(back_up_file, GDRIVE_PARENTS)

        logger.info("Done backing up and uplaoding")
    except Exception as e:
        logger.exception(f"Could not complete successfully :> {e}")
        exit(1)
