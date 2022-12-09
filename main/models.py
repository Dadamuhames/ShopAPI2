from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from colorfield.fields import ColorField
from ckeditor.fields import RichTextField
from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL
from django.core.validators import MaxValueValidator, MinValueValidator
from easy_thumbnails.fields import ThumbnailerImageField
# Create your models here.
class Atributs(models.Model):
    name = models.CharField('Name', max_length=255)

    def __str__(self):
        return self.name


class AtributOptions(models.Model):
    name = models.CharField('Option Name', max_length=255)
    atribut = models.ForeignKey(Atributs, on_delete=models.CASCADE, related_name='options')

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField('Color name',  max_length=255, unique=True)
    hex = ColorField(default='#FF0000')


    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField('Name', max_length=255)
    image = ThumbnailerImageField(upload_to='category_images')
    inf = models.TextField('Deskription')
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, related_name='children')
    atributs = models.ManyToManyField(Atributs, blank=True, null=True)
    popular = models.BooleanField('Popular', default=False)
    icon = ThumbnailerImageField(upload_to='category_icons')

    def __str__(self):
        return self.name

'''    def save(self, *args, **kwargs):
        ctg = super(Category, self).save(*args, **kwargs)
        print(ctg)
        if ctg.parent is not None:
            for atr in ctg.parent.atributs.all():
                if atr not in ctg.atributs.all():
                    ctg.atributs.add(atr)
                    print(atr)

        return ctg'''


class Brand(models.Model):
    name = models.CharField('Name', max_length=255)

    def __str__(self):
        return self.name




    
@receiver(post_save, sender=Category)
def set_atributs(sender, instance, created, *args, **kwargs):
    if created:
        if instance.parent is not None:
            for atr in instance.parent.atributs.all():
                instance.atributs.add(atr.id)
                instance.save()
                print(instance.atributs.all())






class Products(models.Model):
    STATUS = [('Inactive', 'Inactive'), ('Published', 'Published')]

    name = models.CharField('Name', max_length=255)
    deskription = models.TextField('Product Deskription')
    information = RichTextField()
    category = models.ManyToManyField(Category, related_name='products', blank=True)
    status = models.CharField('Status', max_length=255, choices=STATUS)
    colors = models.ManyToManyField(Color, blank=True, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, blank=True, null=True)
    model = models.CharField('Model', max_length=255)
    prod_of_day = models.BooleanField('Product of day', default=False)
    popular = models.BooleanField('Popular', default=False)
    hit = models.BooleanField("Is Hit Product", default=False)


    def get_default(self):
        return self.variants.filter(default=True).first()

    def __str__(self):
        return self.name + self.model


class ProductVariants(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='variants')
    price = models.FloatField('Price', validators=[MinValueValidator(1.00)])
    default = models.BooleanField("Default", default=False)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='product_variants')
    qty = models.PositiveIntegerField('Qty')
    rating = models.PositiveIntegerField('Rating', validators=[MaxValueValidator(5), MinValueValidator(1)], blank=True, null=True)
    options = models.ManyToManyField(AtributOptions, blank=True)

    def __str__(self):
        return self.product.name + ': variant ' + str(self.id)

    def save(self, *args, **kwargs):
        self.product.colors.add(self.color)

        super(ProductVariants, self).save(*args, **kwargs)




class ProductImages(models.Model):
    variant = models.ForeignKey(ProductVariants, on_delete=models.CASCADE, related_name='images')
    image = ThumbnailerImageField(upload_to='product_images')

    def __str__(self):
        return self.image.url



class Comments(models.Model):
    STATUS = [('Inactive', 'Inactive'), ('Published', 'Published')]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    product = models.ForeignKey(ProductVariants, on_delete=models.CASCADE, related_name='comments')
    rating = models.PositiveIntegerField('Rating', validators=[MaxValueValidator(5), MinValueValidator(1)])
    body = models.TextField('Comment Body')
    status = models.CharField("Status", max_length=255 , choices=STATUS)
    date = models.DateTimeField('Date')

    def __str__(self):
        return self.user.username + " | " + self.body

    def save(self, *args, **kwargs):
        super(Comments, self).save(*args, **kwargs)



@receiver(post_save, sender=Comments)
def set_rating(sender, instance, created, **kwargs):
    if created:
        ratings = instance.product.comments.filter(status='Published')
        ratings_count = ratings.count()
        if ratings_count == 0:
            ratings_count = 1

        rat_sum = sum([it.rating for it in ratings])

        if rat_sum == 0:
            rat_sum = instance.rating

        rating = rat_sum // ratings_count

        instance.product.rating = rating
        instance.product.save()
