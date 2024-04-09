from bottle import template
import smtplib
import sqlite3
import pathlib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText





##############################
def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


##############################
def sqldb():
    try:
        sqldb = sqlite3.connect(str(pathlib.Path(__file__).parent.resolve())+"/database/company.db")
        sqldb.execute("PRAGMA foreign_keys = ON")
        sqldb.row_factory = dict_factory # JSON objects
        return sqldb
    except Exception as ex:
        print("db function has an errror")
        print(ex)
    finally:
        pass


def send_email(from_email, to_email, verification_id):
    try:

        message = MIMEMultipart()
        message["To"] = from_email
        message["From"] = to_email
        message["Subject"] = 'Testing my email to verify'


        email_body= template("views/emailTemplates/email_verify_link", key=verification_id)
 
        messageText = MIMEText(email_body, 'html')
        message.attach(messageText)
 
        email = from_email
        password = 'sxakvggwacukkdmk'
 
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo('Gmail')
        server.starttls()
        server.login(email,password)
        from_email = from_email
        to_email  = to_email
        server.sendmail(from_email,to_email,message.as_string())
 
        server.quit()
    except Exception as ex:
        print(ex)
        return "error"