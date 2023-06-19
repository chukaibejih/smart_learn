from django.core.mail import send_mail
from celery.utils.log import get_task_logger
from celery import shared_task


logger = get_task_logger(__name__)


@shared_task()
def send_email_confirmation_task(subject, message, from_email, to_email):
    logger.info('send email confirmation')
    try:
        print('Task received')
        result = send_mail(subject, message, from_email, [to_email], fail_silently=False)
        print(f'Email sent: {result}')  # Debug print
        return result
    except Exception as e:
        print(f'Error sending email: {e}')  # Debug print

