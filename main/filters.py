from django_filters import rest_framework as filter
from .models import ProductVariants
from .models import Category, ProductVariants


class ProductVariantFilter(filter.FilterSet):
    price = filter.RangeFilter()

    class Meta:
        model = ProductVariants
        fields = ['price']
        

