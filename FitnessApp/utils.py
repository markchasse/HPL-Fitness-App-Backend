

import time

from django.utils import timezone as dj_datetime
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

SUCCESS_DICT = {'success': True}
ERROR_DICT = {'success': False, 'message': "Somme error occurred on server"}


def file_upload_to(instance, filename):
    try:
        filename = filename.encode("utf-8")
    except Exception as e:
        filename = unicode(int(time.time()))
    return '/'.join([instance.__class__.__name__, unicode(dj_datetime.now().strftime('%Y/%m/%d')),
                     unicode(int(time.time()))+filename])


def send_custom_email(request, ctx):
    message = render_to_string("accounts/email_custom_template.html", ctx)
    msg = EmailMultiAlternatives(ctx['subject'], message, settings.DEFAULT_FROM_EMAIL, [ctx['to']])
    msg.attach_alternative(message, "text/html")
    msg.encoding = 'utf8'
    msg.send()