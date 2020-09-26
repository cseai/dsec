# Accounts

## Q [What's the best way to store Phone number in Django models](https://stackoverflow.com/questions/19130942/whats-the-best-way-to-store-phone-number-in-django-models)

```
    1. Phone by PhoneNumberField
    You can use phonenumber_field library. It is port of Google's libphonenumber library, which powers Android's phone number handling https://github.com/stefanfoulis/django-phonenumber-field

    In model:

    from phonenumber_field.modelfields import PhoneNumberField

    class Client(models.Model, Importable):
        phone = PhoneNumberField(null=False, blank=False, unique=True)
    In form:

    from phonenumber_field.formfields import PhoneNumberField
    class ClientForm(forms.Form):
        phone = PhoneNumberField()
    Get phone as string from object field:

        client.phone.as_e164 
    Normolize phone string (for tests and other staff):

        from phonenumber_field.phonenumber import PhoneNumber
        phone = PhoneNumber.from_string(phone_number=raw_phone, region='RU').as_e164
```

Installation
```bash
    pip install django-phonenumber-field[phonenumbers]
```