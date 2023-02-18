# dj
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# rest
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# internal
from ..utils import EmailSenderThread


class TestMailSender(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):

        subject = 'Activation Data'
        context = {'user': request.user.email}
        html_message = render_to_string('email/test_email.html', context)
        plain_message = strip_tags(html_message)
        from_email = 'From <from@example.com>'
        to = 'to@example.com'

        email_sender_thread = EmailSenderThread(
            subject, plain_message, from_email, [to], html_message)
        email_sender_thread.start()

        return Response({'details': 'email sent successfully'})
