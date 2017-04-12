# Python-Backup-Manager
A little backup manager app written in Python that will schedule backups of a specified folder at the daily frequency specified.


The GUI uses the PyQT5 framwork and allows the user to specify the folder to be backed up as well as where to save the backups. The user may also specify
how often the script will backup the folder (frequency in days). AP Scheduler module is used to schedule cron-style jobs to run the backup
function.

The script creates a .VBS file in the current users /starup folder that will run the BackupMagaer.pyw script on startup, the script will read the last settings
used from the config.ini file and run in background and execute the backup function accordingly.

