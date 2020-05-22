# mariadb-backup-to-gdrive
a simple python service to back up your mariadb database to google drive

# Components
The library has these components
- google drive class (uses the official google-api-python client to establish connection to google drive
- backup class (uses Popen in the underneath to call `mysqldump` and writes output as gzipped content

# Configuration
You can configure the service to run according to your set up by modifying the `config.py` file
### The options are 
The parent folder you want to upload to, copy this from the URL when looking at the folder in the Web

`GDRIVE_PARENTS = ["Id_of_a_google_drive_folder"]`

The db params

`DB_USER = "root"`

`DB_PASSWORD = "admin"`

`DBS_TO_BACKUP = ['db_one', 'db_tow']`

This should be a path to the client secrets file, the following is the default.
The client_secrets should be created in a google API project with the credentials as a Service Accounts option.

`SERVICE_ACCOUNT_FILE = '/usr/local/lib/maridb-backup-service/client_secrets.json'`

The target directory to store your database backups

`TARGET_DIRECTORY = '/tmp/'`

The time to run the database backup default below

`TIME_TO_BACKUP = "03:00"`

The number of latest n backups for a database to keep

`LATEST_BACKUPS_TO_KEEP = 5`

The gmail email that created the app password

`GMAIL_USER = ""`

The app password

`GMAIL_PASSWORD = ""`

The from email to be used for the email notification

`FROM_EMAIL = GMAIL_USER`

The email notification subject

`BACKUP_EMAIL_SUBJECT = "MariaDB Backup Service Notification"`

The addresses to receive the notifications, can also be a single str

`NOTIFICATION_EMAIL_DESTINATION = ['xxx@gmail.com']`

# Deployment
You can deploy this service to your server using the ansible roles in the repo

- First create your `ansible/deploy/group_vars/server.yml` from the sample `ansible/deploy/group_vars/server_sample.yml`
- Then update the `ansible/deploy/prod_inventory` with the just created server details
- Run the ansible tasks `$ ansible-playbook -i ansible/deploy/prod_inventory ansible/deploy/appserver.yml`

# Supervisor
The service is run by a supervisor job called `mariadb_backup_service` which is installed and set up by the ansible run.
You may need to install `supervisor` and other os packages on the target server as this ansible role does not have tasks to install packages.

# Note
You will need to create a folder or grant permission to the `service user` for the google drive folder you want
your backups to be uploaded to

Using the GMAIL API to send email requires a G-suite account so might not be fit for those using the free gmail account. As a result the notifier in this repo uses the `smtplib` to send the email notifications.

# Blog post for this repo

# TODO
Add more notifications methods and allow notifcations for process output updates
