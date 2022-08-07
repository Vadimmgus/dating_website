from clients.send_mail import send_new_letter
from meeting_website.celery import app


@app.task
def send_new_email(email: str, theme: str, message: str):
    send_new_letter(email, theme, message)
