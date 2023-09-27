import win32com.client
import os

def send_email(
        to = None,
        cc = [None],
        actuator_no = ""
):

    path_of_report = "../../documents/checklist_report.docx"
    path_of_report = os.path.abspath(path_of_report)


    ol=win32com.client.Dispatch("Outlook.Application")
    olmailitem=0x0 #size of the new email
    newmail=ol.CreateItem(olmailitem)
    newmail.Subject= 'Testing checklist of actuator number {0}'.format(actuator_no)
    #newmail.To='anson.paul@ssinnovations.org'
    newmail.To='harsh.joon@ssinnovations.org'
    #newmail.CC = ";".join(cc)


    newmail.Body= 'Hello, This is an auto generated email from FCTC application. Please find the testing report for actutaor no {0}.'.foramt(actuator_no)
    
    newmail.Attachments.Add(path_of_report)
    #attach='C:\\Users\\admin\\Desktop\\Python\\Sample.xlsx'
    #attach
    #newmail.Attachments.Add(attach)
    # To display the mail before sending it
    #newmail.Display() 
    newmail.Send()   
    return None