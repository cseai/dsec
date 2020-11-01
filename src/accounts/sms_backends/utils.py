import requests
import datetime
from django.utils.timezone import utc
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from phone_verify.models import SMSVerification

# Settings for phone_verify utils
try:
    phone_verification_utils_settings = settings.PHONE_VERIFICATION_UTILS
except AttributeError:
    raise ImproperlyConfigured("Please define PHONE_VERIFICATION_UTILS in settings")

SCHEME = phone_verification_utils_settings.get('SCHEME')
HOST = phone_verification_utils_settings.get('HOST')
PHONE_VERIFY_REGISTER_PATH = phone_verification_utils_settings.get('PHONE_VERIFY_REGISTER_PATH')
PHONE_VERIFY_VERIFY_PATH = phone_verification_utils_settings.get('PHONE_VERIFY_VERIFY_PATH')


def get_time_diff_second(time_since):
    """
        [TIME DIFF]: https://stackoverflow.com/a/16016130/8520849
        Return time difference in seconds
    """
    if time_since:
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        timediff = now - time_since
        return timediff.total_seconds()


def phone_verify_register(data, scheme=None, netloc=None, path=None, 
        params=None, query=None, fragment=None, url=None):
    """
    [URL]: scheme://netloc/path;parameters?query#fragment
        Example: urlparse('http://www.cwi.nl:80/%7Eguido/Python.html')
        ParseResult(scheme='http', netloc='www.cwi.nl:80', path='/%7Eguido/Python.html',
            params='', query='', fragment='')
    This will register a phone by sending sms via phone_verify API.
    [data]: {
                "phone_number": '+8801xxxxxxxxx',
            }
    """
    if not scheme:
        scheme = SCHEME
    if not netloc:
        netloc = HOST
    if not path:
        path = PHONE_VERIFY_REGISTER_PATH

    response = None
    succeed = False

    if url:
        generated_url = url
    else:
        generated_url = f"{scheme}://{netloc}{path}"
    
    # call API
    response = requests.post(url=generated_url, data=data)

    if response and response.status_code == 200:
        succeed = True
    return response, succeed


def phone_verify_verify(data, scheme=None, netloc=None, path=None, 
        params=None, query=None, fragment=None, url=None):
    """
    [URL]: scheme://netloc/path;parameters?query#fragment
        Example: urlparse('http://www.cwi.nl:80/%7Eguido/Python.html')
        ParseResult(scheme='http', netloc='www.cwi.nl:80', path='/%7Eguido/Python.html',
            params='', query='', fragment='')
    This will verify a phone by checking database table via phone_verify API.
    [data]: {
                "phone_number": '+8801xxxxxxxxx',
                "security_code": security_code,
                "session_token": session_token,
            }
    """
    if not scheme:
        scheme = SCHEME
    if not netloc:
        netloc = HOST
    if not path:
        path = PHONE_VERIFY_VERIFY_PATH

    response = None
    succeed = False

    if url:
        generated_url = url
    else:
        generated_url = f"{scheme}://{netloc}{path}"
    
    # call API
    response = requests.post(url=generated_url, data=data)

    if response and response.status_code == 200:
        succeed = True
    return response, succeed

    
def check_verified_phone_number(phone_number, security_code, session_token, expire_time_from_modified_at=5):
    smsv_instance = SMSVerification.objects.filter(
        phone_number=phone_number,
        security_code=security_code,
        session_token=session_token,
        is_verified=True
    ).first()
    if smsv_instance:
        # check expire_time_from_modified_at limit exit or not
        diff_second = get_time_diff_second(smsv_instance.modified_at)
        if (int(diff_second)//60) > expire_time_from_modified_at:
            # that means time limit exit
            # delete this smsv_instance and return False
            smsv_instance.delete()
            return False
        else:
            return True
    else:
        False

def delete_phone_smsverification_objects(phone_number):
    """
    This will delete all objects of a given phone_number if exists.
    [RETURN] 'True': if succeed. 'False': If something wrong happen.
    """
    succeed = True
    try:
        SMSVerification.objects.filter(phone_number=phone_number).delete()
    except:
        succeed = False

    return succeed
