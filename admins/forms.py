from dataclasses import fields
from django.forms import ModelForm
from django import forms 
from main.models import Category, Products, Comments, ProductVariants, Atributs, AtributOptions
from django.forms.widgets import NumberInput, TextInput, FileInput, Textarea,  EmailInput
from django.contrib.auth.models import User, Group
import django_filters


class EditProduct(forms.ModelForm):
    price = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'form-control mb-2',
        'min': 1,
    }))
    qty = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'form-control mb-2',
        'min': 0,
    }))

    class Meta:
        model = Products
        fields = ['name', 'deskription', 'status', 'information']


        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control mb-2',
            }),
            'status': forms.Select(attrs={
                'class': 'form-select mb-2'
            }),
            'deskription': forms.Textarea(attrs={
                'class': 'form-control mb-2',
                'style': "resize: none",
                'placeholder': 'Text product\'s description...'
            }),
            'post_category': forms.Select(attrs={
                'class': 'form-select mb-2',
                'id': 'post_ctg'
            }),
            'information': forms.Textarea(attrs={
                'class': 'form-control mb-2',
                'style': "resize: none",
                'placeholder': 'Text product\'s description...'
            }),

        }


class AddCtg(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


        widgets = {
            'category_name': forms.TextInput(attrs={
                'class': "form-control mb-2",
       			'placeholder': "Category name"
            }),
            'ctg_avatar': forms.FileInput(attrs={
                'accept':".png, .jpg, .jpeg"
            }),
            'deskription': forms.Textarea(attrs={
                'class': 'form-control mb-2',
                'style': "resize: none",
                'placeholder': 'Text category description...'
            }),
        }


class FilterUsers(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ['groups']



class FilterProducts(django_filters.FilterSet):
    class Meta:
        model = Products
        fields = ['status', 'name']



class ProdVariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariants
        fields = ['product', 'qty', 'price', 'color']


        widgets = {
            'product': forms.Select(attrs={
                'class': 'form-select mb-2'
            }),
            'qty': forms.NumberInput(attrs={
                'class': 'form-control mb-2'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control mb-2'
            })
        }