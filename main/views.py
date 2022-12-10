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
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 20


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
    queryset = ProductVariants.objects.filter(product__prod_of_day=True)
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

        for product in queryset:
            for option in product.options.all():
                if options:
                    pass
        
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




# product-variant detail view
class ProductDetailView(generics.RetrieveAPIView):
    queryset = ProductVariants.objects.filter(Q(product__status='Published'))
    serializer_class = ProductVeriantDetailSerializer



# for dropdown window with categories
class GetCategories(generics.ListAPIView):
    queryset = Category.objects.filter(parent=None)
    serializer_class = AllCetegories



# wishlist
class Like(views.APIView):
    # wishlist view
    def get(self, request, format=None):
        request.session['wishlist'] = request.session.get('wishlist', list())

        data = {
            'list': request.session['wishlist']
        }

        serializer = WishlistSerializer(data).data
        return Response(serializer)

    # add to wishlist
    def post(self, request, format=None):
        request.session['wishlist'] = request.session.get('wishlist', list())
        
        id = request.data.get('id')

        try:
            product = ProductVariants.objects.get(id=int(id))
        except:
            product = None

        if id not in request.session['wishlist'] and product is not None:
            request.session['wishlist'].append(str(id))
            request.session.modified = True
        else:
            return Response({'error': 'Id is invalid'})

        return Response(list(request.session['wishlist']), status=status.HTTP_201_CREATED)

    # remove from wishlist
    def delete(self, request, format=None):
        request.session['wishlist'] = request.session.get('wishlist', list())

        id = request.data.get('id')
        if str(id) in request.session['wishlist']:
            request.session['wishlist'].remove(id)
        request.session.modified = True

        return Response(list(request.session['wishlist']), status=status.HTTP_201_CREATED)

        
# cart
class AddToCart(views.APIView):
    # add to cart
    def post(self, request, format=None):
        request.session['cart'] = request.session.get("cart", list())

        id = request.data.get("id")
        count = request.data.get('count')

        if None in [id, count]:
            return Response({'error': 'Fields is invalid'})

        
        if not str(id).isnumeric() or not str(count).isnumeric():
            return Response({'error': 'Fields is invalid'})

        variant = ProductVariants.objects.get(id=id)
        price = str(float(variant.price) * int(count))

        if str(id) not in [str(it['variant']) for it in request.session['cart']]:
            request.session['cart'].append(
                {
                    'variant': str(id),
                    'count': count,
                    'price': price
                }
            )
            request.session.modified = True

        return Response(list(request.session['cart']), status=status.HTTP_201_CREATED)

    # cart view
    def get(self, request, format=None):
        request.session['cart'] = request.session.get("cart", list())

        if not request.session.session_key:
            request.session.cycle_key()
        sk = request.session.session_key
        print(request.session['cart'])


        data = {
            'session': sk
        }

        #serializer = CartViewSerializer(data).data

        return Response(data)

    # delete from cart
    def delete(self, request, format=None):
        if request.session.get("cart") is not None:
            id = request.data.get('id')



            for it in list(request.session.get("cart")):
                var_id = str(it['variant'])
                if var_id == str(id):
                    request.session['cart'].remove(it)
                    request.session.modified = True

        return Response(list(request.session['cart']), status=status.HTTP_200_OK)


# product variant for modal
class GetModalData(generics.RetrieveAPIView):
    queryset = ProductVariants.objects.filter(Q(product__status='Published'))
    serializer_class = ProductVariantSerializer


# change count in cart
class ChangeCount(views.APIView):
    def put(self, request, format=None):
        if request.session.get("cart") is None:
            return Response(status=status.HTTP_204_NO_CONTENT)

        id = str(request.data.get("id"))
        type = request.data.get("type")

        if id is None or id not in [str(it['variant']) for it in request.session['cart']]:
            return Response(status=status.HTTP_204_NO_CONTENT)

        
        for it in request.session['cart']:
            if str(id) == str(it['variant']):
                if type == '_up':
                    it['count'] = str(int(it['count']) + 1)
                elif type == '_down':
                    it['count'] = str(int(it['count']) - 1)

                request.session.modified = True
        
        return Response(list(request.session['cart']), status=status.HTTP_200_OK)


# search
class SearchView(generics.ListAPIView):
    queryset = ProductVariants.objects.filter(product__status='Published').filter(default=True)
    serializer_class = ProductVariantSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['$product__name', '$product__manufacturer', '$product__model']
    pagination_class = CotalogPagination



# matching
class Matching(views.APIView): 
    # add to matching
    def post(self, request, format=None):
        request.session['matching'] = request.session.get('matching', list())
        id = request.data.get('id')

        try:
            product = ProductVariants.objects.get(id=int(id))
        except:
            product = None


        if product is not None and str(id) not in request.session['matching']:
            request.session['matching'].append(id)
        else:
            return Response({'error': 'Id is Invalid'})

        
        data = {'matching': request.session['matching']}
        
        return Response(data)

    # matching view
    def get(self, request, format=None):
        lst = request.session.get('matching', list())

        data = {'list': lst}
        serializer = WishlistSerializer(data).data

        return Response(serializer)

    # remove from matching
    def delete(self, request, format=None):
        request.session['matching'] = request.session.get('matching', list())
        id = request.data.get('id')

        if id is not None and str(id)in request.session['matching']:
            request.session['matching'].remove(str(id))

        data = {'matching': request.session['matching']}

        return Response(data)
        

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







        

        
