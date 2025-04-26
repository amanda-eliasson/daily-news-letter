import os
from news_report.news_report_creator import NewsReportCreator

EMAIL_RECIPIENTS = os.getenv('EMAIL_RECIPIENTS', None)

def get_email_recipients():
    email_recipients = os.getenv('EMAIL_RECIPIENTS', None)
    if email_recipients is None:
        raise Exception('You must add environment variable for email recipients')
    
    return [email.strip() for email in email_recipients.split(',') if email.strip()]
    
def handler(event, _):
    news_report_generator = NewsReportCreator()
    news_report_generator.scrape_news_and_generate_article_and_send_email(event['recipient_emails'])

if __name__ == "__main__":
    email_recipients = get_email_recipients()
    event = {"recipient_emails": email_recipients}
    handler(event, None)