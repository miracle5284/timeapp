from celery import shared_task
from utils.send_mail import send_mail


@shared_task(name="send_timer_complete_email")
def send_timer_complete_email(user_email: str, timer_id: int) -> None:
    """
    Celery task to send an email to the user when their timer completes.

    Args:
        user_email (str): Recipient email address.
        timer_id (int): ID of the completed timer (used in the message content).
    """
    subject = "⏰ Your timer is complete!"
    message = f"Hello,\n\nYour timer (ID: {timer_id}) has completed successfully.\n\n– Chrona"
    from_email = "no-reply@chrona.app"
    recipient_list = [user_email]

    # TODO: implement after production access is given
    # try:
    #     send_mail(
    #         subject=subject,
    #         message=message,
    #         from_email=from_email,
    #         recipient_list=recipient_list,
    #     )
    # except Exception as e:
    #     # TODO
    #     # Let Celery handle retries if configured
    #     raise e
