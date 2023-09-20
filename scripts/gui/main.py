#!user/bin/python

'''
TODO
- add login window                   : Pending
- Fixed irregular spaces in document : Pending
'''

import sys
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

class Main_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.window_height      = 750
        self.window_width       = 800
        self.init_UI()

        self.meta_data          = {}

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
            self.checklist_checkboxes.append(
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



        # text = "No name found"
        # self.approved_by_name           = self.make_label(text)
        # text = "No date found"
        # self.approved_by_date           = self.make_label(text)
        # text = "No signature found"
        # self.approved_by_signature      = self.make_label(text)






        text = "Assembled by: "
        self.assembled_by_name_label          = self.make_label(text,40,500,10)
        text = "Date: "
        self.assembled_by_date_label          = self.make_label(text,300,500,10)
        text = "Signature: "
        self.assembled_by_signature_label     = self.make_label(text,500,500,10)
        text = "No name found"
        self.assembled_by_name                = self.make_label(text,140,500,10)
        text = "No date found"
        self.assembled_by_date                = self.make_label(text,350,500,10)
        text = "No signature found"
        self.assembled_by_signature           = self.make_label(text,580,500,10)

        text = "Tested by: "
        self.tested_by_name_label             = self.make_label(text,40,530,10)
        text = "Date: "
        self.tested_by_date_label             = self.make_label(text,300,530,10)
        text = "Signature: "
        self.tested_by_signature_label        = self.make_label(text,500,530,10)
        text = "No name found"
        self.tested_by_name                   = self.make_label(text,140,530,10)
        text = "No date found"
        self.tested_by_date                   = self.make_label(text,350,530,10)
        text = "No signature found"
        self.tested_by_signature              = self.make_label(text,580,530,10)

        text = "Approved by"
        self.approved_by_name_label           = self.make_label(text,40,560,10)
        text = "Date: "
        self.approved_by_date_label           = self.make_label(text,300,560,10)
        text = "Signature: "
        self.approved_by_signature_label      = self.make_label(text,500,560,10)
        text = "No name found"
        self.approved_by_name                 = self.make_label(text,140,560,10)
        text = "No date found"
        self.approved_by_date                 = self.make_label(text,350,560,10)
        text = "No signature found"
        self.approved_by_signature            = self.make_label(text,580,560,10)


        self.save_data_button                 = self.make_button("Save data",40,700)
        self.make_document_button             = self.make_button("Make document",300,700)
        self.request_approval_button          = self.make_button("Request approval",600,700)

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


def main():
    app     = QApplication(sys.argv)
    window  = Main_window()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()