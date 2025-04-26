import os

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from loguru import logger

from news_report.news_report_models import NewsReportOutput

class EmailSender:
    def __init__(self):
        self.sender_email=os.getenv('SENDER_EMAIL', None)
        self.sender_password=os.getenv('SENDER_PASSWORD', None)
        
        if not (self.sender_email and self.sender_password):
            raise Exception('You must add environment variables for sender email and password')
        
    def pretty_print_news_report(self, news_report: NewsReportOutput) -> str:
        html = "<!DOCTYPE html>"
        html += "<html lang='de'>"
        html += "<head>"
        html += "  <meta charset='UTF-8'>"
        html += "  <meta name='viewport' content='width=device-width, initial-scale=1.0'>"
        html += "  <title>Dein täglicher Newsletter</title>"
        html += "  <style>"
        html += "    body { font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }"
        html += "    h1 { color: #B7C5AC; }"
        html += "    h2 { border-bottom: 1px solid #ddd; padding-bottom: 5px; }"
        html += "    h3 { margin-top: 20px; }"
        html += "    p { margin: 10px 0; }"
        html += "    ul { list-style: none; padding: 0; }"
        html += "    li { margin: 5px 0; }"
        html += "  </style>"
        html += "</head>"
        html += "<body>"

        # Header
        html += "<h1>Dein täglicher Newsletter</h1>"
        html += "<hr>"

        # Preamble / Summary
        html += "<h2>Zusammenfassung</h2>"
        html += f"<p>{news_report.preamble}</p>"

        # Articles Section
        html += "<h2>Artikel des Tages</h2>"
        for article in news_report.articles:
            html += f"<h3>{article.title}</h3>"
            html += f"<p>{article.text}</p>"

        # Daily Words Section
        html += "<h2>Wörter des Tages</h2>"
        html += "<ul>"
        for word in news_report.daily_words:
            html += f"<li><strong>{word.word}</strong>: {word.translation}</li>"
        html += "</ul>"

        html += "</body>"
        html += "</html>"

        return html

    def send_email(self, recipient_email: str, subject: str, body: str):
        try:
            # Set up the MIME
            message = MIMEMultipart()
            message['From'] = self.sender_email
            message['To'] = recipient_email
            message['Subject'] = subject

            # Attach the email body to the message
            message.attach(MIMEText(body, 'html'))

            # Connect to the SMTP server
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                # Start TLS (Transport Layer Security) for encryption
                server.starttls()

                # Log in to the email account
                server.login(self.sender_email, self.sender_password)

                # Send the email
                server.send_message(message)

            logger.info(f"Email sent successfully to {recipient_email}!")

        except Exception as e:
            logger.error(f"An error occurred: {e}")