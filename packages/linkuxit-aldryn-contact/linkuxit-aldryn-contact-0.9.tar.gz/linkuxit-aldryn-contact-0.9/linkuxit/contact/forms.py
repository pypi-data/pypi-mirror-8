from django import forms
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from .models import Message


class ContactForm(forms.Form):
    email = forms.EmailField()
    subject = forms.CharField()
    content = forms.CharField(widget=forms.Textarea())

    def send(self, site_email):
        message = Message.objects.create(**self.cleaned_data)
        email_message = EmailMessage(
            self.cleaned_data['subject'],
            render_to_string("aldryn_contact/email.txt", {'message': message}),
            site_email,
            [site_email],
            headers={'Reply-To': self.cleaned_data['email']})
        email_message.send(fail_silently=True)
