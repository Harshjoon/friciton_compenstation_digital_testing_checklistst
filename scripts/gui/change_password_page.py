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


class ChangePasswordPage(QWidget):
    def __init__(self, username, user_type):
        super().__init__()

        self.users          = [
            'users',
            'approvers',
            'admins'
        ]

        

        self.username       = username
        self.user_type      = user_type

        self.setWindowTitle('Change password page')
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

        layout.addWidget(self.labels['New Username'],                   0,0,1,1)
        layout.addWidget(self.lineEdits['New Username'],                0,1,1,3)
        layout.addWidget(self.labels['Password'],                       1,0,1,1)
        layout.addWidget(self.lineEdits['Password'],                    1,1,1,3)
        layout.addWidget(self.labels['Confirm Password'],               2,0,1,1)
        layout.addWidget(self.lineEdits['Confirm Password'],            2,1,1,3)

        # login_button = QPushButton('&Remove User')#, clicked=self.checkCredential)
        # layout.addWidget(login_button,                          3,3,1,1)

        add_users_button = QPushButton('&Change username and password', clicked=self.change_username_and_password)
        layout.addWidget(add_users_button,                              3,3,1,1)

        self.status = QLabel('')
        self.status.setStyleSheet('font-size: 25px; color: red;')
        layout.addWidget(self.status,                                   4,0,1,3)



    def initUI(self):
        return None
    

    def change_username_and_password(self):
        
        new_username        = self.lineEdits['New Username'].text()
        password            = self.lineEdits['Password'].text()
        confirm_password    = self.lineEdits['Confirm Password'].text()
        if new_username == "":
            self.show_warning("Username cannot be empty")
            return None
        if password != confirm_password:
            self.show_warning("Confirm password does not match.")
            return None
        # connect to database
        db      = sqlite3.connect(self.database_filepath)
        cursor  = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?",[new_username])
        cursor_output = cursor.fetchall()    

        if new_username != self.username:
            # see if new user in database
            if len(cursor_output) > 0:
                print("Username already present user differect username.")
                self.show_warning(text="Username already present user differect username.")
                return None
            elif len(cursor_output) == 0:
                # add username and password and remove old username 
                #'INSERT INTO "users" VALUES(\'admin_1\',\'admin_1\')'
                cursor.execute(
                    'INSERT INTO "{0}" VALUES(\'{1}\',\'{2}\')'.format(self.user_type, new_username, password)
                    )
                # remove old user
                cursor.execute(
                    'DELETE FROM "{0}" WHERE username=?'.format(self.user_type), [self.username]
                )
                db.commit()
                db.close()
                self.close()
                return None
        elif new_username == self.username:
            db_col_name = {
                'users'     : 'username',
                'approvers' : 'username', 
                'admins'    : 'adminname'
                }
            # update password only.
            cursor.execute(
                "UPDATE {0} SET {1} = '{2}', password='{3}' WHERE username=? ".format(
                    self.user_type, db_col_name[self.user_type], new_username, password
                ), [self.username]
            )
            db.commit()
            db.close()
            self.close()
            return None
        db.close()
        return None
    
    def show_message(
            self,
            text = "message"
            ):
        
        choice = QMessageBox.information(
            None,
            "Warning",
            text,
            QMessageBox.StandardButton.Ok,
            #QMessageBox.StandardButton.No,
        )
        if choice == QMessageBox.StandardButton.Ok:
            return None
        return None
    
    def show_warning(
            self,
            text = "warning"
            ):
        
        choice = QMessageBox.critical(
            None,
            "Warning",
            text,
            QMessageBox.StandardButton.Ok
        )
        if choice == QMessageBox.StandardButton.Ok:
            return None
        return None

    
def main():
    print("This is the main function.")
    app = QApplication(sys.argv)
    # set app stylesheet
    # app.setStyleSheet()
    loginWindow = ChangePasswordPage()
    loginWindow.show()

    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Closing Window ...')

if __name__ == '__main__':
    main()