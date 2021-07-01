import re

from rest_framework.exceptions import ValidationError

USERNAME_PATTERN = '^(?=.{8,20}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$'


def username_validator(username):
    if not re.search(USERNAME_PATTERN, username):
        raise ValidationError('Invalid username')


def phone_validator(phone):
    if not re.search('^(09[0-9]{9})$', phone):
        raise ValidationError('Invalid phone number')
