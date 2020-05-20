import gzip
import os
import time

from subprocess import Popen, PIPE


class MariaDBBackup():
    def __init__(self, logger, user, password, target_directory='/tmp/'):
        self.user = user
        self.password = password
        self.target_directory = target_directory
        self.logger = logger

    def backup_database(self, database_name: str):
        """
        Backup given database and return the file backup to
        """
        host_name = os.uname().nodename
        timestamp = time.strftime('%Y_%b_%d_%H_%M')
        target_backup_file = os.path.join(
            self.target_directory,
            f"{database_name}_host_{host_name}_backup_at_{timestamp}.sql.gz")

        try:
            command = Popen(
                f"mysqldump --databases {database_name} --user={self.user} --password='{self.password}' --single-transaction {database_name}",
                shell=True,
                stdout=PIPE)
            output, error = command.communicate()
            if command.returncode == 0:
                # Gzip the output
                with gzip.open(target_backup_file, 'wb') as fh:
                    fh.write(output)
                self.logger.info(
                    f"Backed up up database {database_name} in target file {target_backup_file} in gz format"
                )
                return target_backup_file
            else:
                self.logger.error(
                    f"Could not backup database {database_name} :> {error}")
        except Exception as e:
            self.logger.exception(
                f"Could not backup database {database_name} :> {e}")
            raise
