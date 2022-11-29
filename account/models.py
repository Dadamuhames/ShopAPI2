from django.db import models
from django.contrib.auth.models import AbstractUser
from order.models import telephone_validator, State, City
from easy_thumbnails.fields import ThumbnailerImageField
from django.core.exceptions import ValidationError
import re
from django.dispatch import receiver
from shop import settings
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save, post_delete
# Create your models here.


def index_validator(value):
    number_temp = r"\+998\d{9}"
    if bool(re.match(number_temp, value)) == False:
        raise ValidationError(
            ("Your telephone number is invalid"),
            params={'value': value}
        )


class User(AbstractUser):
    username = models.CharField('Username', blank=True, null=True, max_length=255, unique=True)
    nbm = models.CharField('Number', max_length=13, null=False, blank=False, validators=[telephone_validator], unique=True)
    avatar = ThumbnailerImageField(upload_to='avatars', default='user.png', blank=True, null=True)
    adres = models.CharField("Adres", max_length=255, blank=True, null=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='users', blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='users', blank=True, null=True)
    post_ind = models.CharField('Post Index', max_length=6, blank=True, null=True)

    USERNAME_FIELD = 'nbm'

    def __str__(self):
        if not self.username:
            return self.nbm
        return self.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


