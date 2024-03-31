from django.db import models

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, EmailValidator, MinLengthValidator

class CustomUser(AbstractUser):
    username = models.CharField(max_length=20, unique=True, validators=[
        RegexValidator(
            regex=r'^[a-zA-Z0-9]+$',
            message='Username must contain only alphanumeric characters.',
            code='invalid_username'
        ),
        MinLengthValidator(5, message='Username must be at least 5 characters long.')
    ])
    first_name = models.CharField(max_length=10, validators=[
        RegexValidator(
            regex=r'^[a-zA-Z]+$',
            message='First name must contain only letters.',
            code='invalid_first_name'
        ),
        MinLengthValidator(5, message='first name must be at least 5 characters long.')
    ])
    last_name = models.CharField(max_length=10)
    email = models.EmailField(unique=True, validators=[
        EmailValidator(message='Invalid email format.')
    ])
    password = models.CharField(max_length=50 ,validators=[
        RegexValidator(
            regex='^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()_+])[0-9a-zA-Z!@#$%^&*()_+]{8,}$',
            message='Password must contain at least 8 characters, including one uppercase letter, one lowercase letter, one digit, and one special character.',
            code='invalid_password'
        ),
        ])
    shipping_address = models.CharField(max_length=100, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos', null=True, blank=True)
    def __str__(self):
        return self.username

