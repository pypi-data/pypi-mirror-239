from config import cfg
from helpers.email_helper import EmailHelper

import datetime


def send_results(email_helper: EmailHelper, attachments):
    dt_str = datetime.datetime.now().strftime('%d %b %Y')
    body = '''Dear All,
   <br> 
   <br> 
Please find attached the passive tenor management signals.
   <br> 
   <br> 
Please confirm receipt via return email.
   <br> 
   <br> 
Regards,
   <br> 
QI Team 
'''
    email_helper.send_email(recipients=cfg.EMAIL_RECIPIENTS,
                            subject=f'MGI Tenor Management: {dt_str}',
                            body=body,
                            attachments=attachments)
