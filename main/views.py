from django.shortcuts import render
from rest_framework import viewsets, views, generics, mixins, status, filters
from .models import Products, ProductVariants, Category
from .serializers import HomePageSerializer, CotalogSerializer, CtegoryDeteilSerializer, CategoryProductsSerializer, ProductVeriantDetailSerializer, AllCetegories
from .serializers import CartViewSerializer, WishlistSerializer, ProductVariantSerializer
from rest_framework.response import Response
from django.db.models import Q
# Create your views here.

# view for home page
class HomePage(views.APIView):
    def get(self, request, *args, **kwargs):
        data = {}

        data['products'] = ProductVariants.objects.filter(default=True).filter(Q(product__status='Published')).filter(popular=True)[:12]
        data['hits'] = ProductVariants.objects.filter(default=True).filter(Q(product__status='Published')).filter(hit=True)[:6]
        data['categories'] = Category.objects.filter(parent=None).filter(popular=True).exclude(brand=True)[:12]
        data['brands'] = Category.objects.filter(brand=True).filter(popular=True)[:12]
        data['product_of_day'] = Products.objects.filter(prod_of_day=True).first().get_default()

        serializer = HomePageSerializer(data)

        return Response(serializer.data)


# view for cotalog page
class CotalogView(views.APIView):
    def get(self, request, *args, **kwargs):
        data = {}

        data['products'] = ProductVariants.objects.filter(default=True).filter(Q(product__status='Published')).exclude(hit=True)
        data['hit_products'] = ProductVariants.objects.filter(default=True).filter(Q(product__status='Published')).filter(hit=True)

        serializer = CotalogSerializer(data)

        return Response(serializer.data)



# view for categories without parents
class CategoryDeteilView(generics.RetrieveAPIView):
    queryset = Category.objects.exclude(brand=True).filter(parent=None)
    serializer_class = CtegoryDeteilSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)



# view for categories with parent
class CategoryProducts(generics.RetrieveAPIView):
    queryset = Category.objects.exclude(parent=None).exclude(brand=True)
    serializer_class = CategoryProductsSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)



# product-variant detail view
class ProductDetailView(generics.RetrieveAPIView):
    queryset = ProductVariants.objects.filter(Q(product__status='Published'))
    serializer_class = ProductVeriantDetailSerializer



# for dropdown window with categories
class GetCategories(generics.ListAPIView):
    queryset = Category.objects.filter(parent=None).filter(brand=False)
    serializer_class = AllCetegories



# add to wishlist
class Like(views.APIView):
    def get(self, request, format=None):
        if not request.session.get('wishlist'):
            request.session['wishlist'] = list()
        else:
            request.session['wishlist'] = list(request.session.get('wishlist'))

        return Response(request.session['wishlist'], status=status.HTTP_201_CREATED)


    def post(self, request, format=None):
        if not request.session.get('wishlist'):
            request.session['wishlist'] = list()
        else:
            request.session['wishlist'] = list(request.session.get('wishlist'))
        
        id = request.data.get('id')
        if id not in request.session['wishlist']:
            request.session['wishlist'].append(str(id))
            request.session.modified = True

        return Response(list(request.session['wishlist']), status=status.HTTP_201_CREATED)
        


# delete from wishlist
class UnLike(views.APIView):
    def post(self, request, format=None):
        if not request.session.get('wishlist'):
            request.session['wishlist'] = list()
        else:
            request.session['wishlist'] = list(request.session.get('wishlist'))

        id = request.data.get('id')
        if str(id) in request.session['wishlist']:
            request.session['wishlist'].remove(id)
        request.session.modified = True

        return Response(list(request.session['wishlist']), status=status.HTTP_201_CREATED)



# add to cart
class AddToCart(views.APIView):
    def post(self, request, format=None):
        if not request.session.get("cart"):
            request.session['cart'] = list()
        else:
            request.session['cart'] = list(request.session.get("cart"))

        id = request.data.get("id")
        variant = ProductVariants.objects.get(id=id)
        count = request.data.get('count')

        if None in [variant, count]:
            return Response({'error': 'Fields is invalid'})

        
        if not str(id).isnumeric() or not str(count).isnumeric():
            return Response({'error': 'Fields is invalid'})

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


# delete from cart
class RemoveFromCart(views.APIView):
    def post(self, request, format=None):
        if request.session.get("cart") is not None:
            id = request.data.get('id')
            for it in list(request.session.get("cart")):
                var_id = str(it['variant'])
                if var_id == str(id):
                    request.session['cart'].remove(it)
                    request.session.modified = True

        return Response(list(request.session['cart']), status=status.HTTP_200_OK)




# cart list view
class CartView(views.APIView):
    def get(self, request, format=None):
        if not request.session.get("cart"):
            request.session['cart'] = list()
        else:
            request.session['cart'] = list(request.session.get("cart"))


        data = {
            'cart': request.session['cart']
        }

        serializer = CartViewSerializer(data).data

        return Response(serializer)



# wishlist list view
class WishlistView(views.APIView):
    def get(self, request, format=None):
        if not request.session.get('wishlist'):
            request.session['wishlist'] = list()
        else:
            request.session['wishlist'] = list(request.session.get('wishlist'))

        data = {
            'wishlist': request.session['wishlist']
        }

        serializer = WishlistSerializer(data).data

        return Response(serializer)



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






        

        
