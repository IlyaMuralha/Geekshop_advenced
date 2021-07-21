import hashlib
import random
from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.timezone import now

from geekshop.settings import DOMAIN_NAME, EMAIL_HOST_USER, ACTIVATION_KEY_TTL


class ShopUser(AbstractUser):
    age = models.PositiveIntegerField('возраст', null=True)
    avatar = models.ImageField(upload_to='avatars', blank=True)
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    # можно сделать вариант с лямбдой
    # activation_key_expires = models.DateTimeField(default=lambda x: now())

    @cached_property
    def get_items_cached(self):
        return self.basket.select_related()

    def basket_price(self):
        # return sum(el.product_cost for el in self.basket.all())
        _items = self.get_items_cached
        return sum(list(map(lambda x: x.quantity, _items)))

    def basket_quantity(self):
        # return sum(el.quantity for el in self.basket.all())
        _items = self.get_items_cached
        return sum(list(map(lambda x: x.product_cost, _items)))

    @property
    def is_activation_key_expired(self):
        return now() - self.activation_key_created > timedelta(hours=ACTIVATION_KEY_TTL)
        # вместо создания нового поля для юзера, можно было воспользоваться полем date_joined у AbstractUser
        # return now() - self.date_joined > timedelta(hours=ACTIVATION_KEY_TTL)

    def set_activation_key(self):
        salt = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:6]
        self.activation_key = hashlib.sha1((self.email + salt).encode('utf-8')).hexdigest()

    def send_verify_email(self):
        verify_link = reverse('auth:verify',
                              kwargs={'email': self.email,
                                      'activation_key': self.activation_key})

        subject = f'Подтверждение учетной записи {self.username}.'
        message = f'Для подтверждения учетной записи {self.username} на сайте {DOMAIN_NAME} ' \
                  f'перейдите поссылке: \n{DOMAIN_NAME}{verify_link}'

        return send_mail(subject, message, EMAIL_HOST_USER, [self.email], fail_silently=False)


class ShopUserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOICES = (
        (MALE, 'Мужской'),
        (FEMALE, 'Женский'),
    )

    user = models.OneToOneField(ShopUser, primary_key=True, null=False, db_index=True, on_delete=models.CASCADE)
    tagline = models.CharField(verbose_name='тэги', max_length=128, blank=True)
    about_me = models.TextField(verbose_name='о себе', max_length=512, blank=True)
    gender = models.CharField(verbose_name='пол', choices=GENDER_CHOICES, blank=True, max_length=1)
