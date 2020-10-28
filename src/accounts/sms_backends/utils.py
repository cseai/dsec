from phone_verify.models import SMSVerification

def check_verified_phone_number(phone_number, security_code, session_token):
    smsv_instance = SMSVerification.objects.filter(
        phone_number=phone_number,
        security_code=security_code,
        session_token=session_token,
        is_verified=True
    ).first()
    if smsv_instance:
        return True
    else:
        False