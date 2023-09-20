#!user/bin/python

'''
TODO
- add login window                   : Pending
- encryption algorithm for users     : Pending
- Fixed irregular spaces in document : Pending

- password protect sqlite database   : Pending

- save data in json and connect it
  to a database                      : Pending 
'''

import sys
import os
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import Qt, QSize, QRegularExpression
from PyQt6.QtWidgets import QApplication, QWidget, QLabel
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
    QDialogButtonBox,
    QMessageBox,
    QComboBox,
    QPlainTextEdit
)

import datetime as dt

from make_document import make_document
from make_meta_data import make_meta_data


class Main_window(QMainWindow):
    def __init__(self,admin_user, login_details, approver_user):
        super().__init__()
        self.admin_user         = admin_user
        self.approver_user      = approver_user
        self.window_height      = 750
        self.window_width       = 800

        #print(login_details['username'])
        self.login_details      = login_details

        self.meta_data          = {}

        self.init_UI()

    def init_UI(self):
        
        self.setFixedSize(QSize(self.window_width, self.window_height))

        #self.heading_label = QLabel("FRICTION COMPENSATION TESTING CHECKLIST",self)
        #x,y = 200,10
        #self.heading_label.move(x,y)
        #self.heading_label.ad

        heading = "FRICTION COMPENSATION TESTING CHECKLIST"
        self.heading_label = self.make_label(heading,190,10,16)

        text    = "Actuator Serial Number"
        self.actuator_sno_label      = self.make_label(text,50,60,10)
        self.actuator_sno_lineedit   = self.make_lineedit("",200,60-5,120,30) 
        self.actuator_find_button = self.make_button("Find",200,100)


        text    = "Document number : 123"
        self.document_no_label       = self.make_label(text,400,60,10)
        text    = "Revision number    : 123"
        self.revision_no_label       = self.make_label(text,400,80,10)

        self.checklist_content = {
            "Check the test setup assembly" : None,
            "Check the connection"          : None,
            "Check the active current value\
 just after enabling the \
drive"                                        : None,
            "Check if actuator is warmed up": None,
            "Test the actuator for velocity\
 control mode."                              : None,
            "Record Actual velocity"        : None,
            "Record Active current"         : None,
            "Recording time"                : None
        }

        self.yes_no_content = {
            "Any abnormal noise"            : None,
            "Abnormal peak current"         : None
        }

        self.remarks_label          = self.make_label("Remarks",500,120,10)

        self.checklist_checkboxes = []
        self.checklist_lineedits  = []

        x_start,y_start = 40,150
        y = y_start
        for key,value in self.checklist_content.items():
            self.checklist_checkboxes.append(
                self.make_check_box(key,x_start,y,10)
            )
            y += 32

        x_start,y_start = 500,150
        y = y_start
        for key,value in self.checklist_content.items():
            self.checklist_lineedits.append(
                self.make_lineedit("",x_start,y-5,250,30)
            )
            y += 32
        
        self.yes_no_labels              = []
        self.yes_no_linedits            = []
        self.yes_no_combobox            = []

        x_start,y_start = 40,420
        y = y_start
        for key,value in self.yes_no_content.items():
            self.yes_no_labels.append(
                self.make_label(key,x_start,y,10)
            )
            y += 32

        x_start,y_start = 500,420
        y = y_start
        for key,value in self.yes_no_content.items():
            self.yes_no_linedits.append(
                self.make_lineedit("Inspector name",x_start,y-10,250,30)
            )
            y += 32

        x_start,y_start = 200,420
        y = y_start
        for key,value in self.yes_no_content.items():
            self.yes_no_combobox.append(
                self.make_combobox(["yes", "no"],x_start,y - 2)
            )
            y += 32

        self.end_remark_label    = self.make_label("Remarks",40,600,10)
        self.end_remark_lineedit = self.make_lineedit("",40,620,700,60)

        a = 20
        text = "Assembled by: "
        self.assembled_by_name_label          = self.make_label(text,40 + a,500,10)
        text = "Date: "
        self.assembled_by_date_label          = self.make_label(text,300 ,500,10)
        text = "Signature: "
        self.assembled_by_signature_label     = self.make_label(text,500 ,500,10)
        text = self.login_details['username']#"No name found"
        self.assembled_by_name                = self.make_label(text,140 + a,500,10)
        text = "No date found"
        self.assembled_by_date                = self.make_label(text,350 ,500,10)
        text = "No signature found"
        self.assembled_by_signature           = self.make_label(text,580 ,500,10)
        self.assembled_checkbox               = self.make_check_box("",30,502)

        text = "Tested by: "
        self.tested_by_name_label             = self.make_label(text,40 + a,530,10)
        text = "Date: "
        self.tested_by_date_label             = self.make_label(text,300,530,10)
        text = "Signature: "
        self.tested_by_signature_label        = self.make_label(text,500,530,10)
        text = "No name found"
        self.tested_by_name                   = self.make_label(text,140 + a,530,10)
        text = "No date found"
        self.tested_by_date                   = self.make_label(text,350,530,10)
        text = "No signature found"
        self.tested_by_signature              = self.make_label(text,580,530,10)
        self.tested_checkbox                  = self.make_check_box("",30,532)

        text = "Approved by"
        self.approved_by_name_label           = self.make_label(text,40 + a,560,10)
        text = "Date: "
        self.approved_by_date_label           = self.make_label(text,300,560,10)
        text = "Signature: "
        self.approved_by_signature_label      = self.make_label(text,500,560,10)
        text = "No name found"
        self.approved_by_name                 = self.make_label(text,140 + a,560,10)
        text = "No date found"
        self.approved_by_date                 = self.make_label(text,350,560,10)
        text = "No signature found"
        self.approved_by_signature            = self.make_label(text,580,560,10)
        self.approved_checkbox                 = self.make_check_box("",30,562)

        self.save_data_button                 = self.make_button("Save data",40,700)
        self.show_document_button             = self.make_button("Show document",200,700)
        self.make_document_button             = self.make_button("Make document",400,700)
        self.request_approval_button          = self.make_button("Request approval",600,700)

        self.connect_signals_and_slots()

        return None
    
    def connect_signals_and_slots(
            self
    ):
        
        #self.actuator_find_button

        #self.save_data_button
        self.make_document_button.clicked.connect(self.on_make_document_clicked)
        #self.request_approval_button 
        self.show_document_button.clicked.connect(lambda:  self.show_document(document_path = "../../documents/checklist_report.docx"))

        self.assembled_checkbox.stateChanged.connect(self.on_assemble_state_change)
        self.tested_checkbox.stateChanged.connect(self.on_tested_state_change)
        self.approved_checkbox.stateChanged.connect(self.on_approved_state_change)

        return None
    
    def on_assemble_state_change(self):
        
        if self.assembled_checkbox.isChecked():

            if self.admin_user or self.approver_user:
                # show message
                choice = QMessageBox.information(
                    None,
                    "Warning",
                    "Are you sure that you want to make this change.",
                    QMessageBox.StandardButton.Yes,
                    QMessageBox.StandardButton.No,
                )
                if choice == QMessageBox.StandardButton.No:
                    self.assembled_checkbox.setChecked(False)
                    return None
                elif choice == QMessageBox.StandardButton.Yes:
                    pass

            date_format = "%d-%m-%Y" 
            self.assembled_by_name.setText(self.login_details['username'])
            self.assembled_by_date.setText(dt.datetime.now().strftime(format=date_format))
            
            #self.assembled_by_signature

        elif not self.assembled_checkbox.isChecked():
            self.assembled_by_name.setText("No name found")
            self.assembled_by_date.setText("No date found")
            self.assembled_by_name.adjustSize()
            self.assembled_by_date.adjustSize()

        return None
    
    def on_tested_state_change(self):
        
        if self.tested_checkbox.isChecked():

            if self.admin_user or self.approver_user:
                # show message
                choice = QMessageBox.information(
                    None,
                    "Warning",
                    "Are you sure that you want to make this change.",
                    QMessageBox.StandardButton.Yes,
                    QMessageBox.StandardButton.No,
                )
                if choice == QMessageBox.StandardButton.No:
                    self.tested_checkbox.setChecked(False)
                    return None
                elif choice == QMessageBox.StandardButton.Yes:
                    pass

            date_format = "%d-%m-%Y"
            self.tested_by_name.setText(self.login_details['username'])
            self.tested_by_date.setText(dt.datetime.now().strftime(format=date_format))
            #self.tested_by_signature

        elif not self.tested_checkbox.isChecked():
            self.tested_by_name.setText("No name found")
            self.tested_by_date.setText("No date found")
            self.tested_by_name.adjustSize()
            self.tested_by_date.adjustSize()

        return None
    
    def on_approved_state_change(self):
        if not (self.admin_user or self.approver_user):
            choice = QMessageBox.critical(
                None,
                "Warning",
                "Only admin user or approver user can approve checlist.",
                QMessageBox.StandardButton.Ok
            )
            self.approved_checkbox.setChecked(False)
            if choice == QMessageBox.StandardButton.Ok:
                self.approved_checkbox.setChecked(False)
                return None

        else:
            if self.approved_checkbox.isChecked():
                date_format = "%d-%m-%Y"
                self.approved_by_name.setText(self.login_details['username'])
                self.approved_by_date.setText(dt.datetime.now().strftime(format=date_format))
                #self.approved_by_signature

        return None

    def make_label(
            self,
            text        = "",
            x           = 0,
            y           = 0,
            font_size   = 12,
            bold        = False
    ):
        label = QLabel(text,self)
        label.setStyleSheet("QLabel{{font-size: {0}pt}}".format(font_size))
        label.move(x,y)
        label.adjustSize()
        return label
    
    def make_lineedit(
            self,
            text        = "",
            x           = 0,
            y           = 0,
            w           = None,
            h           = None,
    ):
        #lineedit = QLineEdit(self)
        lineedit = QPlainTextEdit(self)
        lineedit.setPlaceholderText(text)
        lineedit.move(x,y)
        #lineedit.adjustSize()

        if (w != None) and (h != None):
            lineedit.setFixedSize(QSize(w,h))

        return lineedit

    def make_check_box(
            self,
            text        = "",
            x           = 0,
            y           = 0,
            font_size   = 12,
    ):
        check_box = QCheckBox(text,self)
        check_box.setStyleSheet("QCheckBox{{font-size: {0}pt}}".format(font_size))
        check_box.move(x,y)
        check_box.adjustSize()

        return check_box
    
    def make_combobox(
            self,
            texts   = [],
            x       = 0,
            y       = 0,
    ):
        combobox = QComboBox(self)
        for text in texts:
            combobox.addItem(text)
        combobox.move(x,y)
        combobox.adjustSize()
        return combobox
    
    def make_button(
            self,
            text    ="",
            x       =0,
            y       =0,
    ):
        button = QPushButton(text,self)
        button.move(x,y)
        button.adjustSize()
        return button

    def on_save_clicked(self):
        """
            Description : Save data in a database
        """
        return None
    
    def on_make_document_clicked(self):
        """
            Description : make word document and pdf.
        """

        meta_data = make_meta_data(self,default=False)

        make_document(
            meta_data=meta_data,
            save_pdf=True
        )

        print(meta_data)

        return None

    def show_document(
            self,
            document_path = "../../documents/checklist_report.docx"
            ):
        os.system('start {}'.format(document_path))
        return None

    def make_document_number(
            self
    ):
        
        

        return None

def main():
    app     = QApplication(sys.argv)
    
    window  = Main_window(
        admin_user=False,
        login_details={"username":"admin"},
        approver_user=False
    )
    window.show()
    app.exec()

if __name__ == '__main__':
    main()