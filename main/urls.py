from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('popular_products', views.PopularProducts.as_view()),
    path('popular_brand', views.PopularBrands.as_view()),
    path('populat_ctg', views.PopularCategoriesView.as_view()),
    path('hit_products', views.HitProductView.as_view()),
    path("product_of_day", views.ProductsOfDay.as_view()),
    path("category/<int:pk>", views.CategoryDeteilView.as_view()),
    path('product/<int:pk>', views.ProductDetailView.as_view()),
    path("categories", views.GetCategories.as_view()),
    path('like', views.Like.as_view()),
    path("cart", views.AddToCart.as_view()),
    path('get_modal/<int:pk>', views.GetModalData.as_view()),
    path("change-count", views.ChangeCount.as_view()),
    path('search', views.SearchView.as_view()),
    path("filter", views.FilterApiView.as_view()),
    path("products", views.ProductsList.as_view()),
    path("matching", views.Matching.as_view()),
    path('comments', views.CommentsView.as_view()),
    path('brands', views.BrandList.as_view()),
    path('brands/<int:pk>', views.BrandDetailView.as_view()),
    path('brand_ctg/<int:pk>', views.BrandCategoriew.as_view())
]
