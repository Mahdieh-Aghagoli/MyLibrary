import pyotp
from PIL import Image
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django_extensions.db.fields import AutoSlugField

from common.validators import username_validator, phone_validator
from user.managers import AccountManager


def slugify_function(content):
    return slugify(content, allow_unicode=True)


class Account(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('Username', max_length=30, unique=True, validators=[username_validator])
    email = models.EmailField('Email', unique=True)
    phone = models.CharField('Phone number', max_length=11, blank=True, null=True, unique=True,
                             validators=[phone_validator])
    GENDER_CHOICES = [('N', 'None'),
                      ('F', 'Female'),
                      ('M', 'Male')]
    gender = models.CharField('Gender', max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    birthday = models.DateField('Birthday', blank=True, null=True,
                                help_text='Please use the follow format :<em>YYYY-MM-DD</em>')
    avatar = models.ImageField('Avatar', default='profile_pics/default.png', upload_to='profile_pics')

    slug = AutoSlugField(populate_from=['username'], unique=True, allow_unicode=True,
                         slugify_function=slugify_function)

    otp = models.CharField(max_length=100, blank=True)

    is_active = models.BooleanField('Active', default=True)
    is_superuser = models.BooleanField('Superuser', default=False)
    is_staff = models.BooleanField('Staff', default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True)

    objects = AccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        app_label = 'user'

    def __str__(self):
        return self.username

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save()

        img = Image.open(self.avatar.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.avatar.path)

    def authenticate(self, otp):
        try:
            provided_otp = int(otp)
        except:
            return False
        # Here we are using Time Based OTP. The interval is 120 seconds.
        # otp must be provided within this interval or it's invalid
        t = pyotp.TOTP(self.otp, interval=120)
        return t.verify(provided_otp)
