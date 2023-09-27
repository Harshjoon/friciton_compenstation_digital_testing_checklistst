import sys

from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtWidgets import (
    QCheckBox,
    QPushButton,
    QLineEdit,
    QGridLayout,
    QMessageBox,
    QSizePolicy
)

import sqlite3
#from sqlite3 import Error

"""
TODO
- Replace all path to absolute path     : Pending
"""

class NewUserPage(QWidget):
    def __init__(self):
        super().__init__()

        print("new user page initialized")

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

        self.labels['New Username'] = QLabel('New Username')
        self.labels['Password'] = QLabel('Password')
        self.labels['Confirm Password'] = QLabel('Confirm Password')
        self.labels['New Username'].setSizePolicy(QSizePolicy.Policy.Fixed,QSizePolicy.Policy.Fixed)
        self.labels['Password'].setSizePolicy(QSizePolicy.Policy.Fixed,QSizePolicy.Policy.Fixed)
        self.labels['Confirm Password'].setSizePolicy(QSizePolicy.Policy.Fixed,QSizePolicy.Policy.Fixed)

        self.lineEdits['New Username']     = QLineEdit()
        self.lineEdits['Password']     = QLineEdit()
        self.lineEdits['Password'].setEchoMode(QLineEdit.EchoMode.Password)
        self.lineEdits['Confirm Password']     = QLineEdit()
        self.lineEdits['Confirm Password'].setEchoMode(QLineEdit.EchoMode.Password)

        layout.addWidget(self.labels['New Username'],                    0,0,1,1)
        layout.addWidget(self.lineEdits['New Username'],            0,1,1,3)
        layout.addWidget(self.labels['Password'],                    1,0,1,1)
        layout.addWidget(self.lineEdits['Password'],            1,1,1,3)
        layout.addWidget(self.labels['Confirm Password'],            2,0,1,1)
        layout.addWidget(self.lineEdits['Confirm Password'],    2,1,1,3)


        self.approver_user_checkbox            = QCheckBox("Approver User", self)
        self.approver_user_checkbox.move(30,90)

        # login_button = QPushButton('&Remove User')#, clicked=self.checkCredential)
        # layout.addWidget(login_button,                          3,3,1,1)

        add_users_button = QPushButton('&Add Users', clicked=self.add_user)
        layout.addWidget(add_users_button,                      3,3,1,1)

        self.status = QLabel('')
        self.status.setStyleSheet('font-size: 25px; color: red;')
        layout.addWidget(self.status,                           4,0,1,3)

    def initUI(self):
        return None
    
    def add_user(self):

        new_username        = self.lineEdits['New Username'].text()
        password            = self.lineEdits['Password'].text()
        confirm_password    = self.lineEdits['Confirm Password'].text()

        if new_username == "":
            # show warning message
            choice = QMessageBox.critical(
                None,
                "Warning",
                "New username cannot be empty",
                QMessageBox.StandardButton.Ok
            )
            if choice == QMessageBox.StandardButton.Ok:
                return None
            
        if password == "":
            # show warning message
            choice = QMessageBox.critical(
                None,
                "Warning",
                "Password cannot be empty",
                QMessageBox.StandardButton.Ok
            )
            if choice == QMessageBox.StandardButton.Ok:
                return None


        if password != confirm_password:
            # show warning message
            choice = QMessageBox.critical(
                None,
                "Warning",
                "Confirm password does not match.",
                QMessageBox.StandardButton.Ok
            )
            if choice == QMessageBox.StandardButton.Ok:
                return None

        # serch user in database
        db      = sqlite3.connect(self.database_filepath)
        cursor  = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?",[new_username])
        cursor_output = cursor.fetchall()
        if len(cursor_output) != 0:
            choice = QMessageBox.critical(
                None,
                "Warning",
                "Username already exists",
                QMessageBox.StandardButton.Ok
            )
            if choice == QMessageBox.StandardButton.Ok:
                return None
        
        cursor.execute("SELECT * FROM admins WHERE adminname=?",[new_username])
        cursor_output = cursor.fetchall()
        if len(cursor_output) != 0:
            choice = QMessageBox.critical(
                None,
                "Warning",
                "Username already exists",
                QMessageBox.StandardButton.Ok
            )
            if choice == QMessageBox.StandardButton.Ok:
                return None
            
        cursor.execute("SELECT * FROM approvers WHERE username=?",[new_username])
        cursor_output = cursor.fetchall()
        if len(cursor_output) != 0:
            choice = QMessageBox.critical(
                None,
                "Warning",
                "Username already exists",
                QMessageBox.StandardButton.Ok
            )
            if choice == QMessageBox.StandardButton.Ok:
                return None
        
        choice = QMessageBox.information(
            None,
            "Message",
            "User added successfully",
            QMessageBox.StandardButton.Ok
        )

        try:
            # add user to database
            if self.approver_user_checkbox.isChecked():
                cursor.execute( 'INSERT INTO "approvers" VALUES(\'{0}\',\'{1}\')'.format(new_username, password))
            else: 
                cursor.execute( 'INSERT INTO "users" VALUES(\'{0}\',\'{1}\')'.format(new_username, password))

            db.commit()
            db.close()
        except sqlite3.Error as er:
            choice = QMessageBox.critical(
                None,
                "Warning",
                "User cannot be added, please contact developers.",
                QMessageBox.StandardButton.Ok
            )
            if choice == QMessageBox.StandardButton.Ok:
                return None

        db.close()
        
        self.close()

        return None
    
    def remove_user(self):
        return None

def main():
    print("This is the main function.")
    app = QApplication(sys.argv)
    # set app stylesheet
    # app.setStyleSheet()
    loginWindow = NewUserPage()
    loginWindow.show()

    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Closing Window ...')

if __name__ == '__main__':
    main()
        