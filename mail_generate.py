import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_mail(subject):
    for i in range(1, 73):
        sender_email = "naviprasaad50@gmail.com"
        receiver_email = f"23am0{i}@kpriet.ac.in"
        password = "bswc ccki wzsu vrnp"

        subject = f"Here new Notes for {subject}..."
        body = "Hello,\n\nThis is a test email sent using Python.\n\nBest Regards,\nPython Script"

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, msg.as_string())
                time.sleep(10)
            print("Email sent successfully!")
        except Exception as e:
            print(f"Error: {e}")
