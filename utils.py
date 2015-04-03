import time
from django.utils import timezone as dj_datetime


def file_upload_to(instance, filename):
    return '/'.join([instance.__class__.__name__, unicode(dj_datetime.now().strftime('%Y/%m/%d')),
                     unicode(int(time.time())) + filename])


