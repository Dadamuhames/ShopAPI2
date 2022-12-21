#from osm_field.fields import LatitudeField, LongitudeField, OSMField
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
import re
from main.models import Products, ProductVariants
import datetime
# Create your models here.

def telephone_validator(value):
    number_temp = r"\+998\d{9}"
    if bool(re.match(number_temp, value)) == False:
        raise ValidationError(
            ("Your telephone number is invalid"),
            params={'value': value}
        )


class State(models.Model):
    name = models.CharField('State Name', max_length=255)
    price = models.FloatField('Price of shipping', validators=[MinValueValidator(1.00)])
    uuid = models.UUIDField(editable=False, blank=True, null=True)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField('Name', max_length=255)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='city')
    uuid = models.UUIDField(blank=True, null=True)

    def __str__(self):
        return self.name


class Promocode(models.Model):
    code = models.CharField('Promocode', max_length=255, unique=True)
    percent = models.PositiveIntegerField()


    def __str__(self):
        return self.code


class PaymentTyps(models.Model):
    name = models.CharField('Name', max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name


class Order(models.Model):
    PAYMENT = [('Cash', 'Cash'), ('Online', 'Online')]
    STATUS = [('Ожидание', 'Ожидание'), ('Ожидание модерации', 'Ожидание модерации'),
              ('Ожидание сборки', 'Ожидание сборки'), ('На доставке', 'На доставке'), ('Отменено', 'Отменено'), ('Доставлено', 'Доставлено')]
    SHIP_TYPE = [('Самовывоз', "Самовывоз"), ("Курьером до двери", "Курьером до двери")]

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    session = models.CharField('Session Id', max_length=255, blank=True, null=True)
    price = models.FloatField('Price', validators=[MinValueValidator(1.00)])
    payment = models.ForeignKey(PaymentTyps, on_delete=models.CASCADE)
    first_name = models.CharField('First Name', max_length=255)
    last_name = models.CharField('Last Name', max_length=255)
    patronymic = models.CharField('Patronymic', max_length=255)
    adres = models.CharField('Adres', max_length=255, blank=True, null=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='orders', blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='orders', blank=True, null=True)
    status = models.CharField('Status', max_length=255, default='Ожидание', choices=STATUS)
    tel = models.CharField('Tel. number', max_length=13, validators=[telephone_validator])
    promocode = models.ForeignKey(Promocode, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField('Email', blank=True, null=True)
    post_ind = models.CharField('Post Index', max_length=6, blank=True, null=True)
    comment = models.TextField('Comment', blank=True, null=True)
    date = models.DateTimeField('Date', default=datetime.datetime.now())
    update_date = models.DateTimeField("Update Date", default=datetime.datetime.now())
    shipping = models.CharField('Shipping type', max_length=255, choices=SHIP_TYPE)
    '''    location = OSMField()
    location_lat = LatitudeField()
    location_lon = LongitudeField()'''


    def get_full_name(self):
        return self.first_name + '' + self.last_name + '' + self.patronymic 

    def total(self):
        return float(self.price) + int(self.state.price) if self.shipping == 'Курьером до двери' else self.price

    def shipping_price(self):
        return float(self.state.price) if self.shipping == 'Курьером до двери' else 0.00
    

    def __str__(self):
        return 'Order №' + str(self.id)


class OrderProducts(models.Model):
    product = models.ForeignKey(ProductVariants, on_delete=models.CASCADE)
    order= models.ForeignKey(Order, on_delete=models.CASCADE, related_name='products')
    qty = models.PositiveIntegerField('Qty')
    price = models.FloatField('Price', validators=[MinValueValidator(1.00)])

    def set_qty(self):
        self.product.qty -= 1
        self.product.save()

    def save(self, *args, **kwargs):
        self.set_qty()
        super(OrderProducts, self).save(*args, **kwargs)


    def __str__(self):
        return f'Order №{self.order.id} product: "{self.product.product.name}"'


class OrderHistory(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='history')
    status = models.CharField('Status', max_length=255)
    comment = models.CharField('Comment', max_length=255)
    date = models.DateTimeField('Date', default=timezone.now())

    def get_format_date(self):
        return f'{self.date.day}/{self.date.month}/{self.date.year}'

    def __str__(self):
        return f'Order №{self.order.id} status => {self.status}'



class OrderData(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='data')
    ip = models.GenericIPAddressField('Ip')
    user_agent = models.CharField('User Agent', max_length=255)
    lng = models.CharField('Accept Language', max_length=255)

    def __str__(self):
        return f'Order №{self.order.id} data'



# order aplication
class OrderAplication(models.Model):
    product = models.ForeignKey(ProductVariants, on_delete=models.CASCADE)
    count = models.PositiveIntegerField('Product count')
    nbm = models.CharField('Tel. nbm', max_length=13, validators=[telephone_validator])
    name = models.CharField('Name', max_length=255)
    last_name = models.CharField('Last Name', max_length=255)
    patronymic = models.CharField('Patr', max_length=255)
    data = models.DateTimeField(default=timezone.now())

    def get_total_price(self):
        return int(self.count) * float(self.product.price)

    def __str__(self):
        return 'Application №' + ' ' + str(self.id)
