# The parent folder you want to upload to
# Copy this from the URL when looking at the folder in the Web
GDRIVE_PARENTS = ["15DgirpJA-Z2O-DNz_iHd3DjoYwLyP3Gu"]
# Db params
DB_USER = "root"
DB_PASSWORD = "admin"
DBS_TO_BACKUP = ['farmit', 'blog_db']
# This should be a path to the client secrets file assumed to be in the current folder
SERVICE_ACCOUNT_FILE = 'client_secrets.json'
# The target directory to store your database backups
TARGET_DIRECTORY = '/tmp/'
TIME_TO_BACKUP = "03:00"
# The number of backup files to keep for a database
LATEST_BACKUPS_TO_KEEP = 5
# The gmail email that created the app password
GMAIL_USER = ""
# The app password
GMAIL_PASSWORD = ""
# The from email to be used for the email notification
FROM_EMAIL = GMAIL_USER
# The email notification subject
BACKUP_EMAIL_SUBJECT = "MariaDB Backup Service Notification"
# The addresses to receive the notifications, can also be a single str
NOTIFICATION_EMAIL_DESTINATION = ['xxx@gmail.com']
