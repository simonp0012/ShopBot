import smtplib  # Importing smtplib to send emails
from twilio.rest import Client  # Importing Twilio Client to send SMS
from email.message import EmailMessage  # Importing EmailMessage to create email content
from config import EMAIL_ADDRESS, EMAIL_PASSWORD, TWILIO_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE  # Importing configuration variables

def send_email_alert(email, product_url):
    # Creating an email message object
    msg = EmailMessage()
    # Setting the email subject
    msg["Subject"] = "Purchase Confirmation"
    # Setting the sender's email address
    msg["From"] = EMAIL_ADDRESS
    # Setting the recipient's email address
    msg["To"] = email
    # Setting the email content
    msg.set_content(f"Success! Your bot purchased: {product_url}")

    # Connecting to the Gmail SMTP server using SSL
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        # Logging into the email account
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        # Sending the email message
        smtp.send_message(msg)

def send_sms_alert(phone, product_url):
    # Creating a Twilio client object
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    # Sending an SMS message
    client.messages.create(
        body=f"Success! Your bot purchased: {product_url}",  # Message content
        from_=TWILIO_PHONE,  # Twilio phone number
        to=phone  # Recipient's phone number
    )