from django.contrib import admin
from main.models import Products, ProductImages, ProductVariants, Comments, Category, Atributs, AtributOptions, Color
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = [it.name for it in Products._meta.fields]
    filter_horizontal = ['category', 'colors']


    class Meta:
        models = Products


admin.site.register(Products, ProductAdmin)
admin.site.register(ProductImages)


class ProductVariantsAdmin(admin.ModelAdmin):
    list_display = [it.name for it in ProductVariants._meta.fields]
    filter_horizontal = ['options']

    class Meta:
        models = ProductVariants

admin.site.register(ProductVariants, ProductVariantsAdmin)
admin.site.register(Comments)


class CategoryAdmin(admin.ModelAdmin):
    list_display = [it.name for it in Category._meta.fields]
    filter_horizontal = ['atributs']

    class Meta:
        models = Category


admin.site.register(Category, CategoryAdmin)
admin.site.register(Atributs)
admin.site.register(AtributOptions)
admin.site.register(Color)
