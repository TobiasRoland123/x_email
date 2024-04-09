from bottle import get, template, run, post, request, static_file
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import x
import uuid
from bottle import get, run

 
##############################
@get("/")
def _():
    return template("index", name="x")

##############################

@get("/mixhtml.js")
def _():
    return static_file("mixhtml.js", ".")

 
##############################
@get("/email_signup")
def _():
    try:
        return template("views/email_signup")
    
    except Exception as ex:
      print(ex)
    return "error"


##############################
@get("/email_verify")
def _():
    try:
        return template("views/email_verify")
    
    except Exception as ex:
      print(ex)
    return "error"

##############################
@get("/email")
def _():
    try:
        message = MIMEMultipart()
        message["To"] = 'samueltobiasrolanduyet@gmail.com'
        message["From"] = 'samueltobiasrolanduyet@gmail.com'
        message["Subject"] = 'Testing my email'


        email_body= template("email_welcome")
 
        messageText = MIMEText(email_body, 'html')
        message.attach(messageText)
 
        email = 'samueltobiasrolanduyet@gmail.com'
        password = 'sxakvggwacukkdmk'
 
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo('Gmail')
        server.starttls()
        server.login(email,password)
        from_email = 'samueltobiasrolanduyet@gmail.com'
        to_email  = 'samueltobiasrolanduyet@gmail.com'
        server.sendmail(from_email,to_email,message.as_string())
 
        server.quit()
    except Exception as ex:
        print(ex)
        return "error"


##############################
@post("/signup_user")
def _():
    try:
        user_email = request.forms.get("user_email", "")
        user_password = request.forms.get("user_password", "")
        user_pk = uuid.uuid4().hex
        user_verified = 0
        user_verification_id = uuid.uuid4().hex


        print(f"user_email: {user_email}, user_password: {user_password}, user_pk: {user_pk}, user_verified: {user_verified}, user_verification_id: {user_verification_id}")

        db = x.sqldb()
        q = db.execute("INSERT INTO users VALUES(?, ?, ?,?,?)",(user_pk, user_email, user_password, user_verified, user_verification_id))
        db.commit()



        x.send_email('samueltobiasrolanduyet@gmail.com', user_email, user_verification_id)
        print(f"###################   {user_email}  #################")
    
    except Exception as ex:
        print(f'***************   {ex} ******************')
        return "error"


##############################
@get("/verify")
def _():
    try:
        print("####################### RUNNING VERIFY EMAIL POST ROUTE ##############")
        message = MIMEMultipart()
        message["To"] = 'samueltobiasrolanduyet@gmail.com'
        message["From"] = 'samueltobiasrolanduyet@gmail.com'
        message["Subject"] = 'Testing my email to verify'


        email_body= template("views/emailTemplates/email_verify_link")
 
        messageText = MIMEText(email_body, 'html')
        message.attach(messageText)
 
        email = 'samueltobiasrolanduyet@gmail.com'
        password = 'sxakvggwacukkdmk'
 
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo('Gmail')
        server.starttls()
        server.login(email,password)
        from_email = 'samueltobiasrolanduyet@gmail.com'
        to_email  = 'samueltobiasrolanduyet@gmail.com'
        server.sendmail(from_email,to_email,message.as_string())
 
        server.quit()
        
    
    except Exception as ex:
        print(ex)
        return "error"



###############################################
@get("/activate_user/<key>")
def _(key):
    try:

        db = x.sqldb()
        user = db.execute("SELECT * FROM users WHERE user_verification_id = ?", (key,))
        q = db.execute("UPDATE users SET user_verified = 1 WHERE user_verification_id = ?", (key,))
        db.commit()
      
        db.commit()

        
        return template("activate_user.html", user=user)
    except Exception as ex:
        print(ex)


###############################################
run(host="127.0.0.1", port=8080,debug=True, reloader=True, interal=0)