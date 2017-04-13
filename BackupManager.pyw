
"""
TODO:
    - Test scheduler function on startup after reboot
"""

import sys
import shutil
import os
import time
from distutils.dir_util import copy_tree
from datetime import datetime
from configparser import SafeConfigParser

from apscheduler.schedulers.background import BackgroundScheduler


class Main:
    """Manages folder backups"""
    config = SafeConfigParser()

    def __init__(self):
        self._folder_to_backup = "C:\\Users\\Kyle\\Google Drive\\Programming\\Python3\\Backup Manager\\test_folder_to_backup"
        self._backup_destination = "C:\\Users\\Kyle\\Google Drive\\Programming\\Python3\\Backup Manager\\test_backup_destination"
        self._backup_interval = 7

    @property #getter & setter decorators
    def folder_to_backup(self):
        return self._folder_to_backup
    @folder_to_backup.setter
    def folder_to_backup(self, value):
        self._folder_to_backup = value

    @property
    def backup_destination(self):
        return self._backup_destination
    @backup_destination.setter
    def backup_destination(self, value):
        self._backup_destination = value

    @property
    def backup_interval(self):
        return self._backup_interval
    @backup_interval.setter
    def backup_interval(self, value):
        self._backup_interval = value

    def run(self):
        """Runs the scheduler in background to schedule backup jobs according to the settings"""
        scheduler = BackgroundScheduler()
        #scheduler.add_job(self.backup_folder, 'cron', day=[x for x in range(1, 31, self._backup_interval)])
        scheduler.add_job(self.backup_folder, 'cron', second=[x for x in range(1, 59, self._backup_interval)]) # for testing purposes
        scheduler.start()
        print("press CTRL+C to quit")

        try:
        # This is here to simulate application activity (which keeps the main thread alive).
            while True:
                time.sleep(60)
        except (KeyboardInterrupt, SystemExit):
            # Not strictly necessary if daemonic mode is enabled but should be done if possible
            scheduler.shutdown()

    def backup_folder(self, affix=""):
        """copy the contents of _folder_to_backup to a new folder in the _backup_destination with the current date appended to the end of the folder name"""
        shutil.copytree(self._folder_to_backup, f"{self._backup_destination}\\backup - {datetime.now().strftime('%Y-%m-%d %H %M %S')}{affix}")

        print("Folder backup complete..")
    
    def restore(self, backup_to_restore=None):
        """backs up the current _folder_to_backup with an added affix to let you know its a pre-restore back up and not a scheduled backup 
        before replacing it's contents with a previous backup; the location of the previous backup to replace it with should be specified in args"""
        self.backup_folder(affix="-restore backup")
        shutil.rmtree(self._folder_to_backup)
        os.makedirs(self._folder_to_backup)
        try:
            copy_tree(backup_to_restore, self._folder_to_backup)
        except:
            print("invalid restore folder location, please specify which backup to restore")

    def check_config(self):
        "Checks for the existence of a config.ini file and reads the settings, if none exists it will create one and fill with current/default settings for Main"
        if os.path.isfile('config.ini'):
            self.read_config()
        else:
            Main.config.add_section('main')
            with open('config.ini', 'w') as f:
                Main.config.write(f)
            print("New config file made at: %s" % os.getcwd())
            self.write_config()

    def read_config(self):
        "reads config.ini and gets the settings values then sets the values of its instance to those"
        Main.config.read('config.ini')
        self._folder_to_backup = Main.config.get('main', '_folder_to_backup')
        self._backup_destination = Main.config.get('main', '_backup_destination')
        self._backup_interval = int(Main.config.get('main', '_backup_interval'))

        print("Config file read from: %s" % os.getcwd())
    
    def write_config(self):
        "Writes current settings to a config.ini file"
        Main.config.set('main', '_folder_to_backup', str(self._folder_to_backup))
        Main.config.set('main', '_backup_destination', str(self._backup_destination))
        Main.config.set('main', '_backup_interval', str(self._backup_interval))
        with open('config.ini', 'w') as f:
            Main.config.write(f)

        print("Wrote to config file at: %s" % os.getcwd())

    def install_startup_script(self):
        "saves a .vbs script to the windows startup folder that will run the BackupManager.pyw script on startup"
        startup_folder_location = os.path.expanduser("~\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup")
        backupManager_location = "{}/BackupManager.pyw".format(os.path.dirname(sys.argv[0]))

        with open('{}\\BackupManagerStartup.vbs'.format(startup_folder_location), 'w+') as f:
            f.write("CreateObject(\"Wscript.Shell\").run \"\"\"{}\"\"\"".format(backupManager_location))

        print("scheduler installed")


if __name__ == "__main__":
    os.chdir(os.path.dirname(sys.argv[0])) # change working directory to location of script
    main = Main()

    main.check_config()
    print(main.backup_interval)
    #main.backup_folder()
    #main.install_startup_script()

    main.restore("{}\\backup - test restore".format(main.backup_destination))
    #main.restore()

    """ the following is the code to replace all the debugging code above.
    These commands are meant to be run when this script is run at startup(not when called upon from the GUI), they will check for the existence of config.ini \
    and then run in the background to schedule and execute cron-style jobs based on the settings found in the config file.
    """
    #main = Main()
    #os.chdir(os.path.dirname(sys.argv[0])) # change working directory to location of script
    #if os.path.exists('config.ini')
        #main.read_config()
        #main.run()
    