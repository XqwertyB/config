import jwt

from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.core.exceptions import ValidationError

from django.db import models
from django.core.validators import RegexValidator


class Category(models.Model):
    title = models.CharField('Categoriya nomi', max_length=100)
    icon = models.CharField("Icona", max_length=255)

    def __str__(self):
        return self.title


class UserManager(BaseUserManager):
    def create_user(self, name, phone, password=None):

        if name is None:
            raise TypeError('Users must have a username.')

        if phone is None:
            raise TypeError('Users must have an email address.')

        user = self.model(name=name, phone=self.normalize_phone(phone))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, name, phone, password):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(name, phone, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

    def normalize_phone(self, phone):

        return phone

class Costumer(AbstractBaseUser, PermissionsMixin):
    _validate_phone = RegexValidator(
        regex=r"^998([3578]{2}|(9[013-57-9]))\d{7}$",
        message="Your phone number must start with 9 and not exceed 12 characters. For example: 998901234567",
    )

    name = models.CharField('F.I.O', max_length=20)
    phone = models.CharField('tel raqami', max_length=12, validators=[_validate_phone], unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name']
    objects = UserManager()

    def __str__(self):
        return f"{self.name} {self.last_name}"

    @property
    def token(self):

        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.timestamp())
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')

class Organization(models.Model):
    title = models.CharField("Organizatsiya Nomi", max_length=200)
    discription = models.TextField("Malumot",)
    address = models.CharField("Address", max_length=250)
    individual = models.BooleanField("Jismony shaxs", default=False)
    legal_entity = models.BooleanField("Yuridik shaxs", default=False)
    long = models.CharField('Kordinata x', max_length=9, unique=True)
    lat = models.CharField('Kordinata y', max_length=9, unique=True)
    costumer_id = models.ForeignKey(Costumer, verbose_name="Foydalanuvchi User", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Announcement(models.Model):

    _validate_phone = RegexValidator(
        regex=r"^998([3578]{2}|(9[013-57-9]))\d{7}$",
        message="Raqam tug'ri kiriting For example: 998901234567",
    )
    title = models.CharField('Nomi', max_length=250)
    sub_category_id = models.ForeignKey(Category, verbose_name='Kategory', on_delete=models.CASCADE)
    discription = models.TextField("Ma'lumot")
    phone = models.CharField('Tel raqam', max_length=12, validators=[_validate_phone])
    telegram_status = models.BooleanField('Telegram bormi?', default=False)
    telegram = models.CharField('Telegram Username', max_length=40, null=True, blank=True)
    salary_status = models.BooleanField('Maosh suxbat asosida bulsa', default=False)
    min_salary = models.FloatField('Maosh narxi minimal', null=True, blank=True)
    max_salary = models.FloatField('Maosh narxi maksimal', null=True, blank=True)
    data = models.DateTimeField('Yaratilish vaqti', auto_now_add=True)
    organization_id = models.ForeignKey(Organization, verbose_name='Organizatsiya', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def clean(self):
        if self.telegram_status and not self.telegram:
            raise ValidationError({'telegram': "To'dirilishi shart"})

    def clean(self):
        # Если salary_status равно True, убеждаемся, что min_salary и max_salary не являются обязательными
        if self.salary_status:
            if self.min_salary is not None or self.max_salary is not None:
                raise ValidationError('Min va max salary faqat salary_status False bo`lganida majburiy.')
        # Если salary_status равно False, убеждаемся, что min_salary и max_salary заполнены
        else:
            if self.min_salary is None or self.max_salary is None:
                raise ValidationError('Min va max salary majburiy.')


class CompanyContact(models.Model):
    telegram = models.CharField("Telegram link", max_length=100)
    phone = models.CharField("Tel raqam", max_length=12, help_text="998990001122")

    def __str__(self):
        return self.telegram

class TopWishList(models.Model):
    costumer_id = models.ForeignKey(Costumer, verbose_name="Foydalanuvchi", on_delete=models.CASCADE)
    announcement_id = models.ForeignKey(Announcement, verbose_name="Vakansiya", on_delete=models.CASCADE)