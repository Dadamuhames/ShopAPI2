from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, views, generics, mixins, status, filters
from .models import Products, ProductVariants, Category, Color, Brand, AtributOptions
from .serializers import CtegoryDeteilSerializer, ProductVeriantDetailSerializer, AllCetegories, CommentsSerializer, BrandSerializer, ColorSerializer
from .serializers import CartViewSerializer, WishlistSerializer, ProductVariantSerializer, CategorySerializer, ProductVeriantRepresent
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from .filters import ProductVariantFilter
from django_filters import rest_framework as filter
# Create your views here.


# paginators
class CotalogPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 1000


# colors 
class ColorsView(generics.ListAPIView):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer


# popular products
class PopularProducts(generics.ListAPIView):
    queryset = Products.objects.filter(status='Published').filter(popular=True)
    serializer_class = ProductVeriantRepresent


# hit products
class HitProductView(generics.ListAPIView):
    queryset = Products.objects.filter(status='Published').filter(hit=True)
    serializer_class = ProductVeriantRepresent


# popular categories
class PopularCategoriesView(generics.ListAPIView):
    queryset = Category.objects.filter(parent=None).filter(popular=True)
    serializer_class = CategorySerializer
    

# brand view
class PopularBrands(generics.ListAPIView):
    queryset = Brand.objects.filter(popular=True)[:12]
    serializer_class = BrandSerializer


# brand list
class BrandList(generics.ListAPIView):
    queryset = Brand.objects.order_by('-id')
    serializer_class = BrandSerializer
    pagination_class = CotalogPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['^name']


# brand deteil view
class BrandDetailView(generics.RetrieveAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer



# get brand categories
class BrandCategoriew(views.APIView):
    def get(self, request, pk, format=None):
        brand = get_object_or_404(Brand.objects.all(), pk=pk)
        products = brand.products.all()

        ctg = []
        for prod in products:
            try:
                category = prod.category.get(children=None)
                ctg.append(category)
            except:
                continue
        print(ctg)
        
        serializer = CategorySerializer(ctg, many=True).data

        return Response(serializer)


# product of day
class ProductsOfDay(generics.ListAPIView):
    queryset = ProductVariants.objects.filter(prod_of_day=True)
    serializer_class = ProductVariantSerializer


# view for categories without parents
class CategoryDeteilView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CtegoryDeteilSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)



# filter view
class FilterApiView(generics.ListAPIView):
    serializer_class = ProductVariantSerializer
    filter_backends = [filter.DjangoFilterBackend]
    pagination_class = CotalogPagination
    filterset_class = ProductVariantFilter

    def get_queryset(self):
        queryset = ProductVariants.objects.filter(product__status='Published')
        ctg_id = self.request.GET.get('ctg_id')
    
        if ctg_id == None or ctg_id == '':          
            return queryset                 

        try:
            ctg = Category.objects.get(id=int(ctg_id))
        except:
            return queryset


        queryset = queryset.filter(product__category=ctg)
        options = []
        for item in self.request.GET:
            if 'atribut_' in item:
                options.append(self.request.GET[item])

        products = []
        for product in queryset:
            for option in product.options.all():
                if option in options:
                    products.append(product)

        
        for product in queryset:
            if product not in products:
                queryset.exclude(id=product.id)


        
        colors = []
        for item in self.request.GET:
            if 'color_' in str(item):
                try:
                    color = Color.objects.get(id=int(self.request.GET[item]))
                    colors.append(color)
                except:
                    pass

        
        for product in queryset:
            if product.color not in colors:
                queryset = queryset.exclude(id=product.id)
            

        return queryset


# products list
class ProductsList(generics.ListAPIView):
    serializer_class = ProductVariantSerializer
    pagination_class = CotalogPagination


    def get_queryset(self):
        id = self.request.GET.get('category', 0)
        brand = self.request.GET.get('brand', 0)
        products = ProductVariants.objects.filter(default=True).filter(product__status='Published')

        if id == '':
            id = 0
        
        if brand == '':
            brand = 0
        

        if id != 0 and brand != 0:
            brand = get_object_or_404(Brand.objects.all(), id=int(brand))
            ctg = get_object_or_404(Category.objects.all(), id=int(id))
            products.filter(product__category=ctg, product__brand=brand)
        elif id != 0:
            ctg = get_object_or_404(Category.objects.all(), id=int(id))
            products.filter(product__category=ctg)
        elif brand != 0:
            brand = get_object_or_404(Brand.objects.all(), id=int(brand))
            products.filter(product__brand=brand)

        return products


#product list new
class ProductsView(generics.ListAPIView):
    serializer_class = ProductVariantSerializer
    pagination_class = CotalogPagination
    filter_backends = [filter.DjangoFilterBackend]
    filterset_class = ProductVariantFilter

    def get_queryset(self):   
        if 'filter' in self.request.GET:
            queryset = ProductVariants.objects.all()
        else:
            queryset = ProductVariants.objects.filter(default=True)

        ctg_id = self.request.GET.get("category", 0)
        brand_id = self.request.GET.get("brand", 0)

        if ctg_id == '':
            ctg_id = 0

        try:
            category = Category.objects.get(id=ctg_id)
            queryset = queryset.filter(product__category=category)
        except:
            if brand_id == 0:
                return Response({'error': 'category is required'})


        if brand_id == '':
            brand_id = 0


        try:
            brand = Brand.objects.get(id=brand_id)
            queryset = queryset.filter(product_brand=brand)
        except:
            pass


        options = []
        for item in self.request.GET:
            if 'atribut_' in item:
                options.append(self.request.GET[item])

        products = []
        for product in queryset:
            for option in product.options.all():
                if option in options:
                    products.append(product)

        for product in queryset:
            if product not in products:
                queryset.exclude(id=product.id)

        colors = []
        for item in self.request.GET:
            if 'color_' in str(item):
                try:
                    color = Color.objects.get(id=int(self.request.GET[item]))
                    colors.append(color)
                except:
                    pass

        for product in queryset:
            if product.color not in colors:
                queryset = queryset.exclude(id=product.id)





        return queryset



# product-variant detail view
class ProductDetailView(generics.RetrieveAPIView):
    queryset = ProductVariants.objects.filter(Q(product__status='Published'))
    serializer_class = ProductVeriantDetailSerializer



# for dropdown window with categories
class GetCategories(generics.ListAPIView):
    queryset = Category.objects.filter(parent=None)
    serializer_class = AllCetegories


# search
class SearchView(generics.ListAPIView):
    queryset = ProductVariants.objects.filter(product__status='Published').filter(default=True)
    serializer_class = ProductVariantSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['$product__name', '$product__brand__name', '$product__model']
    pagination_class = CotalogPagination


# get product comments
class CommentsView(generics.ListAPIView):
    serializer_class = CommentsSerializer
    pagination_class = CotalogPagination


    def get_queryset(self):
        id = self.request.GET.get("id", 0)
        if id == '':
            id = 0
        product = get_object_or_404(ProductVariants.objects.all(), id=int(id))

        return product.comments.filter(status='Published')





# list serializer view
class ListSerializeView(views.APIView):
    def post(self, request, format=None):
        lst = request.data.get('products', [])
        products = []
        
        for it in lst:
            try:
                product = ProductVariants.objects.get(id=int(it))
                products.append(product)
            except:
                pass

        serializer = ProductVariantSerializer(products, many=True)

        return Response(serializer.data)



# test session
class TesTSession(views.APIView):
    def get(self, request, format=None):
        if not self.request.session.session_key:
            self.request.session.cycle_key()
        sk = self.request.session.session_key

        return Response({'session': sk})

        
