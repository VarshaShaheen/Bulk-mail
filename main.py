import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email credentials
email = 'example@gmail.com'  # Sender's email address
password = 'application specific password'  # Sender's email password

# Email content
with open('email_content.txt', 'r') as f:
    content = f.read()  # Read the email content from the file

# Email subject
subject = 'your subject'

# Email sender name
sender_name = 'IEDC CUSAT'

# Email body
body = MIMEMultipart()  # Create the email body container
body['From'] = sender_name + ' <' + email + '>'  # Set the sender's name and email address
body['Subject'] = subject  # Set the email subject

with open('email_list.csv', 'r') as file:
    reader = csv.reader(file)  # Create a CSV reader object to read recipient details
    next(reader)  # Skip header row

    for row in reader:  # Iterate over each row in the CSV file
        try:
            name, email_id = row[:2]  # Extract the name and email address from the row
        except ValueError:
            print(f"Ignoring row: {row}. Expected two values (name, email) per row.")
            continue

        message = MIMEMultipart('alternative')  # Create the message container
        message['From'] = sender_name + ' <' + email + '>'  # Set the sender's name and email address
        message['To'] = email_id  # Set the recipient's email address

        # Add the message body
        message.attach(MIMEText(f'Hello {name},\n\n{content}', 'plain'))

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:  # Connect to the SMTP server
                smtp.login(email, password)  # Login to the sender's email account
                smtp.sendmail(email, email_id, message.as_string())  # Send the email
            print(f"Email sent successfully to {email_id}")
        except smtplib.SMTPException as e:
            print(f"Error sending email to {email_id}: {str(e)}")

print('Bulk emails sent successfully!')
