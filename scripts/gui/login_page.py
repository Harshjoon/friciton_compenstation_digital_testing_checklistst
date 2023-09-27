'''
TODO
- add approver user                     : Done
- add change password option            : Done
- Replace all path to absolute path     : Pending
- check for valid actuator number       : Pending
'''

import sys

from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtWidgets import (
    QPushButton,
    QLineEdit,
    QGridLayout,
    QMessageBox,
    QSizePolicy
)

import sqlite3
#from sqlite3 import Error

from new_user_page          import NewUserPage
from main                   import Main_window
from change_password_page   import ChangePasswordPage

class LoginPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login')
        # set window icon
        # self.setWindowIcon(QIcon(''))
        self.database_filepath = "../../databases/main.db"

        self.users          = [
            'users',
            'approvers',
            'admins'
        ]

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

        change_password_button = QPushButton('&Change Password', clicked=self.on_change_password)# add slots
        layout.addWidget(change_password_button,                3,1,1,1)

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

        username_found   = False
        password_correct = False 

        db      = sqlite3.connect(self.database_filepath)
        cursor  = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?",[username])
        cursor_output = cursor.fetchall()
        if len(cursor_output)==0:
            print("Username not present.")
        else:
            username_found = True
            target_username, target_password = cursor_output[0]
            if password == target_password:
                password_correct = True 
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
            username_found = True
            target_username, target_password = cursor_output[0]
            if password == target_password:
                password_correct = True
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
            username_found = True
            target_username, target_password = cursor_output[0]
            if password == target_password:
                password_correct = True
                print("password is correct.")
                approver_user = True
                if open_main:
                    self.Main_Window = Main_window(admin_user=True,login_details=login_details,approver_user=True)
                    self.Main_Window.show()
                    self.close()

        if not (admin_user or normal_user or approver_user):
            print("Incorrect password.")

            if open_main:
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

        return admin_user, username_found
    
    def new_check_credential(
            self
    ):
        """
            REQUIREMENTS
                - Input
                - Outputs : 
                    returns if a valid user,
                    what kind of user it is
        """
        username = self.lineEdits['Username'].text()
        password = self.lineEdits['Password'].text()
        user       = None
        valid_user = False
        db      = sqlite3.connect(self.database_filepath)
        cursor  = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?",[username])
        cursor_output = cursor.fetchall()
        if len(cursor_output) == 0:
            print("not a user.")
        elif len(cursor_output) > 0:
            user = self.users[0]
            u,p = cursor_output[0]
            if password == p:
                valid_user = True
                print("password correct")
                return valid_user, user
            return valid_user, user
        cursor.execute("SELECT * FROM approvers WHERE username=?",[username])
        cursor_output = cursor.fetchall()
        if len(cursor_output) == 0:
            print("not an approver.")
        elif len(cursor_output) > 0:
            user = self.users[1]
            u,p  = cursor_output[0]   
            if password == p:
                valid_user = True
                print("password correct")
                return valid_user, user
            return valid_user, user
        cursor.execute("SELECT * FROM admins WHERE adminname=?",[username])
        cursor_output = cursor.fetchall()
        if len(cursor_output) == 0:
            print("not an admin.")
        elif len(cursor_output) > 0:
            user = self.users[2]
            u,p  = cursor_output[0]
            if password == p:
                valid_user = True
                print("password correct")
                return valid_user, user
            return valid_user, user    
        return valid_user, user
    
    def on_change_password(self):
        print("On change password called.")
        valid_user, user         = self.new_check_credential()
        username = self.lineEdits['Username'].text()
        if valid_user:
            self.change_pass_page   = ChangePasswordPage(
                username=username,
                user_type=user
            )
            self.change_pass_page.show()
            return None
        elif user == None:
            self.show_warning(
                text="User not found."
            )
            return None
        elif not valid_user and user != None:
            self.show_warning(
                text="Incorrect Password"
            )
            return None
        return None

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

        print("on_add_user_clicked called")

        admin_user, user_found = self.checkCredential(open_main=False)

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
    loginWindow = LoginPage()
    loginWindow.show()
    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Closing Window ...')

if __name__ == '__main__':
    main()