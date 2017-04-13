
"""
Backup Manager GUI

TODO: 
    - add restore page (use PyQT Layout class)
    - add background service functionality
    - add ability to specify multiple folders to be backed up

"""

import sys
from PyQt5.QtCore import QCoreApplication # pylint: disable=E0611
# from PyQt5.QtGui import *
from PyQt5.QtGui import QIcon # pylint: disable=E0611
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QMainWindow, QPushButton, QAction, QLabel, QLineEdit, QFileDialog, QSpinBox, QHBoxLayout, QVBoxLayout# pylint: disable=E0611
from PyQt5.uic.properties import QtGui

import BackupManager


class window(QMainWindow):

    def __init__(self):
        super(window, self).__init__()
        self.setGeometry(200, 200, 600, 300)
        self.center()
        self.setWindowTitle('Backup Manager')
        # self.setWindowIcon(QIcon('pic.png'))
        #self.dialog = FileBrowser(self) """not needed anymore, deleted when removing FileBrowser class"""
        self.test = 0


        """Qt Actions"""
        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('leave the app')
        exit_action.triggered.connect(self.close_application)

        action2 = QAction('Save(not)', self)
        action2.setShortcut('Ctrl+S')
        action2.triggered.connect(self.close_application)

        restore_backup = QAction('Restore Backup', self)
        restore_backup.setShortcut('Ctrl+R')
        restore_backup.triggered.connect(self.show_restore_page)

        set_folder_to_backup = QAction('Backup Folder Location', self)
        set_folder_to_backup.setStatusTip('Designate the location of the folder that you wish to backup')
        set_folder_to_backup.triggered.connect(self.browse_backup_folder)

        set_backup_destination = QAction('Backup Destination Location', self)
        set_backup_destination.setStatusTip('Designate where you want your backups to be saved')
        set_backup_destination.triggered.connect(self.browse_backup_destination)

        self.statusBar()

        """Main menu bar at top"""
        main_menu = self.menuBar()
        file_menu = main_menu.addMenu('&File')
        file_menu.addAction(action2)
        file_menu.addAction(restore_backup)
        file_menu.addAction(exit_action)
        edit_menu = main_menu.addMenu('&Edit')
        edit_menu.addAction(set_folder_to_backup)
        edit_menu.addAction(set_backup_destination)
        view_menu = main_menu.addMenu('&View')
        help_menu = main_menu.addMenu('&Help')

        exit_action = QAction(QIcon('pic.png'), 'flee the scene', self)
        exit_action.triggered.connect(self.close_application)

        # self.toolBar = self.addToolBar('Extraction')
        # self.toolBar.addAction(exit_action)

        self.home()

    def home(self):
        """Home page for setting up the backup settings.

        Some variables were made into class variables so that their contents could be edited via other methods (with the 'self.' prefix)  
        I've not done this with all of them to avoid cluttering the class namespace""" 
        self.folder_to_backup_qle_label = QLabel('Folder Location:', self)
        self.folder_to_backup_qle_label.move(50, 50)

        self.folder_to_backup_qle = QLineEdit(bm.folder_to_backup, self)
        self.folder_to_backup_qle.setGeometry(50, 75, 400, 20)
        self.folder_to_backup_qle.setStatusTip("The location of the folder you wish to back up")

        self.browse_folder_to_backup_btn = QPushButton('Browse', self)
        self.browse_folder_to_backup_btn.clicked.connect(self.browse_backup_folder)
        self.browse_folder_to_backup_btn.setGeometry(460, 74, 75, 22)

        self.backup_destination_qle_label = QLabel('Backup Destination:', self)
        self.backup_destination_qle_label.move(50, 100)

        self.backup_destination_qle = QLineEdit(bm.backup_destination, self)
        self.backup_destination_qle.setGeometry(50, 125, 400, 20)
        self.backup_destination_qle.setStatusTip("The location where you wish to store backups")

        self.browse_backup_destination_btn = QPushButton('Browse', self)
        self.browse_backup_destination_btn.clicked.connect(self.browse_backup_destination)
        self.browse_backup_destination_btn.setGeometry(460, 124, 75, 22)

        self.backup_interval_label = QLabel('Backup interval: every     7        days', self)
        self.backup_interval_label.setGeometry(305, 245, 300, 30)

        self.backup_interval_spnbx = QSpinBox(self)
        self.backup_interval_spnbx.valueChanged.connect(self.interval_change)
        self.backup_interval_spnbx.setGeometry(420, 251, 33, 20)
        self.backup_interval_spnbx.setValue(7)
        self.backup_interval_spnbx.setRange( 0, 60)
        self.backup_interval_spnbx.setStatusTip("The frequency (in days) that you want to back everything up")

        self.complete_btn = QPushButton('Complete', self)
        self.complete_btn.clicked.connect(bm.backup_folder)
        self.complete_btn.resize(self.complete_btn.sizeHint())
        self.complete_btn.move(500, 250)

        self.show()

    def restore_page(self):
        self.clear_class_widgets()
        okButton = QPushButton("OK")
        cancelButton = QPushButton("Cancel")

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        
        self.setLayout(vbox)    
        
        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Buttons')    
        self.show()
        print(self.__dict__)
        #testing

    def show_restore_page(self):
        """The page that lets the user restore a saved backup"""
        self.rp = RestorePage()
        
    def browse_backup_folder(self):
        """opens file browser for user to choose the location of folder_to_backup('backup_folder' possibly a better variable name?)"""
        folder_name = self.openFolderNameDialog()
        bm.folder_to_backup = folder_name
        self.folder_to_backup_qle.setText(folder_name)
        print(folder_name)

    def browse_backup_destination(self):
        """Opens file browser for user to choose the location of backup_destination"""
        folder_name = self.openFolderNameDialog()
        bm.backup_destination = folder_name
        self.backup_destination_qle.setText(folder_name)
        print(folder_name)
    
    def interval_change(self):
        """Changes BackupManager's backup_interval variable to the spinbox input"""
        bm.backup_interval = self.backup_interval_spnbx.value()

    def clear_class_widgets(self):
        """hides all PyQT widgets in the class namespace"""
        for key in self.__dict__:
            try:
                self.__dict__[key].hide()
            except:
                continue

    def close_application(self):
        print('Close_application()')
        sys.exit()

    def center(self):
        """centers a window on the screen"""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def openFolderNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        options |= QFileDialog.Directory
        #options |= QFileDialog.ShowDirsOnly
        folderName = QFileDialog.getExistingDirectory(self,"QFileDialog.getExistingDirectory()")
        if folderName:
            return(folderName)

class RestorePage(QWidget):
    """The backup restore page - Work In Progress..."""
    def __init__(self):
        super().__init__()
        self.title = 'File Browser'
        self.left = 300
        self.top = 300
        self.width = 300
        self.height = 150
        self.initUI()

    def initUI(self):
        okButton = QPushButton("OK")
        cancelButton = QPushButton("Cancel")

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        
        self.setLayout(vbox)    
        
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle('Buttons')
        self.show()


if __name__ == "__main__":
    bm = BackupManager.Main()
    def run():
        app = QApplication(sys.argv)
        Gui = window()
        rp = RestorePage()
        sys.exit(app.exec_())


run()