

import time

from django.utils import timezone as dj_datetime

SUCCESS_DICT = {'success':True}
ERROR_DICT = {'success':False,'message':"Somme error occured on server"}

def file_upload_to(instance, filename):
    try:
        filename = filename.encode("utf-8")
    except Exception as e:
        filename =unicode( int(time.time()))
    return '/'.join([instance.__class__.__name__, unicode(dj_datetime.now().strftime('%Y/%m/%d')),
                     unicode( int(time.time()))+filename])

