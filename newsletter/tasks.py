import time
from celery import shared_task
from django.core.mail import send_mail, EmailMessage, get_connection
from smtplib import SMTPException, SMTPConnectError, SMTPDataError
from django.conf import settings
from .helper import process_emails
from . import models



@shared_task
def get_emails(subject, body):
        subscriber_emails = models.Subscriber.objects.filter(is_active=True).values_list('email', flat=True)
        chunk_size = 25

        
        for email_group in process_emails(subscriber_emails, chunk_size):
            print(len(email_group))
            send_emails.delay(subject, body, email_group)
          
        


#Fix: hide subscibers addresses from others
#Mailtrap apply a limitation on the process of sending emails over a period of time.
@shared_task(
    max_retries=3,
  #  rate_limit='1/s',  # Limits task execution to 1 per second per worker instance
    autoretry_for=(SMTPDataError, Exception),
    retry_backoff=True,         # Exponential backoff (1s, 2s, 4s, 8s...)
 #   retry_backoff_max=30,       # Max wait time between retries
 #   retry_jitter=True           # Adds randomness to prevent thundering herd
)
def send_emails(subject, body, email_group):
            #        time.sleep(1.1)
                    from_email = 'motasem@example.com'
                    to_email = [from_email]

                    email_message = EmailMessage(
                        subject=subject,
                        body=body,
                        from_email=from_email,
                        to=to_email,
                        bcc=email_group
        
                    )

                    email_message.send(fail_silently=False)
                    print('Done!')




   

