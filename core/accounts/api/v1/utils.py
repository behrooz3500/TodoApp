# dj
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from threading import Thread
from django.core.mail import send_mail

# rest
from rest_framework_simplejwt.tokens import RefreshToken


class EmailSenderThread(Thread):
    """ Class for sending email in a thread """
    def __init__(self, subject, plain_message, from_email, to_email, html_message):
        Thread.__init__(self)
        self.subject = subject
        self.html_message = html_message
        self.plain_message = plain_message
        self.from_email = from_email
        self.to = to_email

    def run(self):
        send_mail(
            self.subject,
            self.plain_message,
            self.from_email,
            self.to,
            html_message=self.html_message
        )


def send_activation_email(user_object, email, action):
    """ Send activation links to users """
    if action == 'activation':
        template = 'email/test_email.html'
    elif action == 'reset_password':
        template = 'email/reset_password.html'
    token = get_tokens_for_user(user_object)
    subject = 'Activation Data'
    context = {'user': user_object.email, 'token': token}
    html_message = render_to_string(template, context)
    plain_message = strip_tags(html_message)
    from_email = 'From <behrooz3500@gmail.com>'
    to = email
    email_sender_thread = EmailSenderThread(
        subject, plain_message, from_email, [to], html_message)
    email_sender_thread.start()


def get_tokens_for_user(user):
    """ Create token for users """
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)

