'''
TODO
- add approver user
'''

import sys

from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import Qt, QSize, QRegularExpression
from PyQt6.QtWidgets import (
    QCheckBox,
    QPushButton,
    QFileDialog,
    QLineEdit,
    QTableWidget,
    QFormLayout,
    QTabWidget,
    QVBoxLayout,
    QMainWindow,
    QDialog,
    QGridLayout,
    QDialogButtonBox,
    QMessageBox,
    QSizePolicy
)

import sqlite3
from sqlite3 import Error

from new_user_page import NewUserPage
from main          import Main_window

class LoginPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login')
        # set window icon
        # self.setWindowIcon(QIcon(''))
        self.database_filepath = "../../databases/main.db"

        self.window_width, self.window_height = 600,200
        self.setFixedSize( self.window_width, self.window_height )

        layout = QGridLayout()
        self.setLayout(layout)

        self.labels = {}
        self.lineEdits = {}

        self.labels['Username'] = QLabel('Username')
        self.labels['Password'] = QLabel('Password')
        self.labels['Confirm Password'] = QLabel('Confirm Password')
        self.labels['Username'].setSizePolicy(QSizePolicy.Policy.Fixed,QSizePolicy.Policy.Fixed)
        self.labels['Password'].setSizePolicy(QSizePolicy.Policy.Fixed,QSizePolicy.Policy.Fixed)
        self.labels['Confirm Password'].setSizePolicy(QSizePolicy.Policy.Fixed,QSizePolicy.Policy.Fixed)

        self.lineEdits['Username']     = QLineEdit()
        self.lineEdits['Password']     = QLineEdit()
        self.lineEdits['Password'].setEchoMode(QLineEdit.EchoMode.Password)
        self.lineEdits['Confirm Password']     = QLineEdit()
        self.lineEdits['Confirm Password'].setEchoMode(QLineEdit.EchoMode.Password)

        layout.addWidget(self.labels['Username'],                    0,0,1,1)
        layout.addWidget(self.lineEdits['Username'],            0,1,1,3)
        layout.addWidget(self.labels['Password'],                    1,0,1,1)
        layout.addWidget(self.lineEdits['Password'],            1,1,1,3)
        layout.addWidget(self.labels['Confirm Password'],            2,0,1,1)
        layout.addWidget(self.lineEdits['Confirm Password'],    2,1,1,3)

        login_button = QPushButton('&Log In', clicked= lambda:  self.checkCredential(open_main=True))
        layout.addWidget(login_button,                          3,3,1,1)

        add_users_button = QPushButton('&Add Users', clicked=self.on_add_user_clicked)
        layout.addWidget(add_users_button,                      3,2,1,1)

        self.labels['Confirm Password'].setHidden(True)
        self.lineEdits['Confirm Password'].setHidden(True)

        self.status = QLabel('')
        self.status.setStyleSheet('font-size: 25px; color: red;')
        layout.addWidget(self.status,                           4,0,1,3)

    def initUI(self):
        return None
    
    def checkCredential(self, open_main=True):

        username = self.lineEdits['Username'].text()
        password = self.lineEdits['Password'].text()

        print("Open main: ", open_main)

        login_details = {
            'username' : username,
        }

        normal_user     = False
        admin_user      = False
        approver_user   = False

        username_found = False

        db      = sqlite3.connect(self.database_filepath)
        cursor  = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?",[username])
        cursor_output = cursor.fetchall()
        if len(cursor_output)==0:
            print("Username not present.")
        else:
            target_username, target_password = cursor_output[0]
            if password == target_password:
                username_found = True
                print("password is correct.")
                normal_user = True
                if open_main:
                    self.Main_Window = Main_window(admin_user=False,login_details=login_details,approver_user=False)
                    self.Main_Window.show()
                    self.close()
                
        
        cursor.execute("SELECT * FROM admins WHERE adminname=?",[username])
        cursor_output = cursor.fetchall()
        if len(cursor_output)==0:
            print("adminname not present.")
        else:
            target_username, target_password = cursor_output[0]
            if password == target_password:
                username_found = True
                print("password is correct.")
                admin_user = True
                if open_main:
                    self.Main_Window = Main_window(admin_user=True,login_details=login_details,approver_user=False)
                    self.Main_Window.show()
                    self.close()

        cursor.execute("SELECT * FROM approvers WHERE username=?",[username])
        cursor_output = cursor.fetchall()
        if len(cursor_output)==0:
            print("username not present.")
        else:
            target_username, target_password = cursor_output[0]
            if password == target_password:
                username_found = True
                print("password is correct.")
                approver_user = True
                if open_main:
                    self.Main_Window = Main_window(admin_user=True,login_details=login_details,approver_user=True)
                    self.Main_Window.show()
                    self.close()

        if not (admin_user or normal_user or approver_user):
            print("Incorrect password.")

            choice = QMessageBox.critical(
                None,
                "Warning",
                "Incorrect password.",
                QMessageBox.StandardButton.Ok
            )
            if choice == QMessageBox.StandardButton.Ok:
                return None

        if admin_user:
            print("user has admin privlages")

        if approver_user:
            print("user has approver privlages")

        db.close()

        return admin_user

    def is_admin_user(self, username):
        admin_user = False

        db      = sqlite3.connect(self.database_filepath)
        cursor  = db.cursor()
        cursor.execute("SELECT * FROM admins WHERE adminname=?",[username])
        cursor_output = cursor.fetchall()

        if len(cursor_output > 0):
            admin_user = True

        return admin_user

    def on_add_user_clicked(self):

        admin_user = self.checkCredential(open_main=False)

        if not admin_user:
            choice = QMessageBox.critical(
                None,
                "Warning",
                "Need admin privlages. Please enter correct username and password. ",
                QMessageBox.StandardButton.Ok
            )
            if choice == QMessageBox.StandardButton.Ok:
                return None
            return None
        else:
            pass
            self.new_user_window = NewUserPage()
            self.new_user_window.show()

        return None

def main():
    print("This is the main function.")
    app = QApplication(sys.argv)
    # set app stylesheet
    # app.setStyleSheet()
    loginWindow = LoginPage()
    loginWindow.show()

    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Closing Window ...')

if __name__ == '__main__':
    main()
        