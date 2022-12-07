from django_filters import rest_framework as filter
from .models import ProductVariants
from .models import Category, ProductVariants


class ProductVariantFilter(filter.FilterSet):
    price = filter.RangeFilter()

    class Meta:
        model = ProductVariants
        fields = ['color', 'price']
        


class ProductFilterBackend(filter.DjangoFilterBackend):
    def filter_queryset(self, request, queryset, view):
        ctg_id = request.GET.get('ctg_id')

        if ctg_id is None or ctg_id == '':
            return queryset

        try:
            ctg = Category.objects.get(id=int(ctg_id))
        except:
            return queryset
            

        queryset = queryset.filter(product__category=ctg)

        for item in request.data:
            if 'atribut_' in item:
                queryset = queryset.filter(option=int(request.data[item]))

        return queryset