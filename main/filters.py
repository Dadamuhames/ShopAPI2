from django_filters import rest_framework as filter
from .models import ProductVariants


class ProductVariantFilter(filter.FilterSet):
    price = filter.RangeFilter()

    class Meta:
        model = ProductVariants
        fields = ['price']
        

