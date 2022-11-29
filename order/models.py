from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
import re
from main.models import Products, ProductVariants
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
    uuid = models.UUIDField()

    def __str__(self):
        return self.name



class Order(models.Model):
    PAYMENT = [('Cash', 'Cash'), ('Online', 'Online')]
    STATES = [
        ("Андижанская область", "Андижанская область"),
        ("Бухарская область   ", "Бухарская область   "),
        ("Джизакская область ", "Джизакская область "),
        ("Кашкадарьинская область  ", "Кашкадарьинская область  "),
        ("Навоийская область", "Навоийская область"),
        ("Наманганская область", "Наманганская область"),
        ("Самаркандская область   ", "Самаркандская область"),
        ("Сурхандарьинская область   ", "Сурхандарьинская область"),
        ("Сырдарьинская область", "Сырдарьинская область"),
        ("Ташкентская область", "Ташкентская область"),
        ("Ферганская область", "Ферганская область"),
        ("Хорезмская область", "Хорезмская область"),
        ("Республика Каракалпакстан", "Республика Каракалпакстан"),
        ("Город Ташкент", "Город Ташкент")
    ]
    STATUS = [('Accepted', 'Accepted'), ('Performed', 'Performed'), ('Canseled', 'Canseled'), ('Paid', 'Paid')]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.CharField('Session Key', max_length=255)
    price = models.FloatField('Price', validators=[MinValueValidator(1.00)])
    payment = models.CharField('Payment type', max_length=255, choices=PAYMENT)
    first_name = models.CharField('First Name', max_length=255)
    last_name = models.CharField('Last Name', max_length=255)
    patronymic = models.CharField('Patronymic', max_length=255)
    adres = models.CharField('Adres', max_length=255)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='orders')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField('Status', max_length=255, choices=STATUS)
    tel = models.CharField('Tel. number', max_length=13, validators=[telephone_validator])
    date = models.DateTimeField('Date')
    

    def __str__(self):
        return 'Order №' + str(self.id)


class OrderProducts(models.Model):
    product = models.ForeignKey(ProductVariants, on_delete=models.CASCADE)
    order= models.ForeignKey(Order, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField('Qty')
    price = models.FloatField('Price', validators=[MinValueValidator(1.00)])

    def set_qty(self):
        self.product.qty -= 1
        self.product.qty.save()

    def save(self, *args, **kwargs):
        self.set_qty()
        super(OrderProducts, self).save(*args, **kwargs)


    def __str__(self):
        return f'Order №{self.order.id} product: "{self.product.product.name}"'


class OrderHistory(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='history')
    status = models.CharField('Status', max_length=255)
    comment = models.CharField('Comment', max_length=255)
    date = models.DateTimeField('Date')

    def __str__(self):
        return f'Order №{self.order.id} status => {self.status}'



class OrderData(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    ip = models.GenericIPAddressField('Ip')
    forw_ip = models.GenericIPAddressField('Forwarded Ip')
    user_agent = models.CharField('User Agent', max_length=255)
    lng = models.CharField('Accept Language', max_length=255)

    def __str__(self):
        return f'Order №{self.order.id} data'
