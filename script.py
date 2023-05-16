import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

with open('settings.json', 'r') as f:
    j = json.load(f)

smtp_server = j["smtp_server"]
smtp_port = int(j["smtp_port"]) 
sender_email = j["e-mail"]
password = j["password"]
subject = j["subject"]

print("Successfully loaded data from /settings.json")
print("Reciepient:")
while True:
    recipient_email = input(">")

    print("Preparing email to " + recipient_email + "...")
    with open('content.txt', 'r', encoding='utf-8') as file:
        body = file.read()

    # Create the email message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain', 'utf-8'))

    current_directory = os.getcwd()
    attachments_folder = os.path.join(current_directory, 'attachments')
    for filename in os.listdir(attachments_folder):
        file_path = os.path.join(attachments_folder, filename)
        with open(file_path, 'rb') as attachment:
            part = MIMEApplication(attachment.read())
            part.add_header('Content-Disposition', 'attachment', filename=filename)
            message.attach(part)

    try:
        # Create a secure connection with the SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, password)

            # Send the email
            server.send_message(message)
        print('Email sent successfully to ' + recipient_email + '!')
    except Exception as e:
        print('Error sending email:', str(e))