# from config import EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_PORT, EMAIL_USE_TLS, DEFAULT_FROM_EMAIL
import smtplib, ssl, threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


'''
# Raw Function Implementation
def send_email(from_email=DEFAULT_FROM_EMAIL, to_email='', subject='Test Subject', msg='Test Mail', is_html=False):
    # Message 
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = from_email
    message["To"] = to_email
    
    content = MIMEText(msg, "html") if is_html else MIMEText(msg, "plain")
    message.attach(content)

    context = ssl.create_default_context()
    try:
        if EMAIL_USE_TLS:
            with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
                server.ehlo()  # Can be omitted
                server.starttls(context=context)
                server.ehlo()  # Can be omitted
                server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
                server.sendmail(from_email, to_email, message.as_string())
        else:
            with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT, context=context) as server:
                server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
                server.sendmail(from_email, to_email, message.as_string())
    except Exception as e:
        print('Exception: -> ', e)
'''



# Sending Email using Threads
class EmailThread(threading.Thread):
    def __init__(self, 
                 from_email, 
                 to_email, 
                 message, 
                 EMAIL_HOST, 
                 EMAIL_HOST_USER, 
                 EMAIL_HOST_PASSWORD, 
                 EMAIL_PORT=587, 
                 EMAIL_USE_TLS=True):
        
        # Compose
        self.from_email = from_email
        self.to_email = to_email
        self.message = message
        
        # SMTP Config
        self.EMAIL_HOST = EMAIL_HOST
        self.EMAIL_HOST_USER = EMAIL_HOST_USER
        self.EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD
        self.EMAIL_PORT = EMAIL_PORT
        self.EMAIL_USE_TLS = EMAIL_USE_TLS

        threading.Thread.__init__(self)


    def trigger_send_email(self):
        context = ssl.create_default_context()
        if self.EMAIL_USE_TLS:
            with smtplib.SMTP(self.EMAIL_HOST, self.EMAIL_PORT) as server:
                server.ehlo()  # Can be omitted
                server.starttls(context=context)
                server.ehlo()  # Can be omitted
                self._extracted_from_trigger_send_email_8(server)
        else:
            with smtplib.SMTP_SSL(self.EMAIL_HOST, self.EMAIL_PORT, context=context) as server:
                self._extracted_from_trigger_send_email_8(server)

    # TODO Rename this here and in `trigger_send_email`
    def _extracted_from_trigger_send_email_8(self, server):
        server.login(self.EMAIL_HOST_USER, self.EMAIL_HOST_PASSWORD)
        server.sendmail(self.from_email, self.to_email, self.message.as_string())
        server.close()

    def run(self):
        try:
            self.trigger_send_email()
           
        except Exception as e:
            print('Exception: -> ', e)

# Class Implementation
class Email:   

    def __init__(self, EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_PORT, EMAIL_USE_TLS, DEFAULT_FROM_EMAIL):
        # SMTP Config
        self.EMAIL_HOST = EMAIL_HOST
        self.EMAIL_HOST_USER = EMAIL_HOST_USER
        self.EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD
        self.EMAIL_PORT = EMAIL_PORT
        self.EMAIL_USE_TLS = EMAIL_USE_TLS
        self.DEFAULT_FROM_EMAIL = DEFAULT_FROM_EMAIL

    # @classmethod
    def send(self, from_email=False, to_email='', subject='Test Subject', msg='Test Mail', is_html=False):
        # Message 
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = from_email or self.DEFAULT_FROM_EMAIL
        message["To"] = to_email
        
        content = MIMEText(msg, "html") if is_html else MIMEText(msg, "plain")
        message.attach(content)
        try:
            EmailThread(
                from_email or self.DEFAULT_FROM_EMAIL, 
                to_email, 
                message,
                EMAIL_HOST = self.EMAIL_HOST,
                EMAIL_HOST_USER = self.EMAIL_HOST_USER,
                EMAIL_HOST_PASSWORD = self.EMAIL_HOST_PASSWORD,
                EMAIL_PORT = self.EMAIL_PORT,
                EMAIL_USE_TLS = self.EMAIL_USE_TLS,
                ).start() # Send Mail
                
        except Exception as e:
            print('Exception: -> ', e)

    

     