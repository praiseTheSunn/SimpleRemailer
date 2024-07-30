import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json

# create and get password here https://myaccount.google.com/u/3/apppasswords to send
# you can send to temp email, get at: https://temp-mail.org
class Email:
    def __init__(self):
        self.email = ""
        self.password = ""

    def send_email(self, recipient_email, subject, body):
        message = MIMEMultipart()
        message['From'] = self.email
        message['To'] = recipient_email
        message['Subject'] = subject

        message.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()  # Start TLS encryption
            server.login(self.email, self.password)  # Login with the email object's credentials
            text = message.as_string()
            server.sendmail(self.email, recipient_email, text)
            server.quit()
            print("Email has been sent successfully to ", recipient_email)
        except Exception as e:
            print("Failed to send email. Error:", e)

    def get_email_from_json(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            self.email = data['email']
            self.password = data['password']


# for testing
if __name__ == '__main__':
    from HieuMail import mail, pw
    MyEmail = Email(mail, pw)
    MyEmail.send_email("gehago8572@bsidesmn.com", "Hieu test", "Hi there")
