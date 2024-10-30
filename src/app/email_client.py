import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import settings


class EmailClient:

    def send_email(self, recipient_list: list[str], subject: str, text: str, html: str, send_back: bool = True):
        if send_back:
            recipient_list.append(settings.SMTP_USER)

        msg = MIMEMultipart('alternative')
        msg["Subject"] = subject
        msg["From"] = settings.SMTP_USER
        msg["To"] = ', '.join(recipient_list)

        text_part = MIMEText(text, 'plain')
        html_part = MIMEText(html, 'html')

        msg.attach(text_part)
        msg.attach(html_part)

        with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(settings.SMTP_USER, recipient_list, msg.as_string())
