import win32com.client
import os
ol=win32com.client.Dispatch("Outlook.Application")
olmailitem=0x0 #size of the new email
newmail=ol.CreateItem(olmailitem)
newmail.Subject= 'Testing Mail'
newmail.To='harsh.joon@ssinnovations.org'

#newmail.CC='harsh.joon@ssinnovations.org'
newmail.CC='harsh.joon@ssinnovations.org; 1harsh.joon@ssinnovations.org'

newmail.Body= 'Hello, this is a test email to showcase how to send emails from Python and Outlook.'
#attach='..\\..\\images\\1.png'
attach=os.path.abspath("../../images/1.png")
newmail.Attachments.Add(attach)
# To display the mail before sending it
#newmail.Display() 
newmail.Send()