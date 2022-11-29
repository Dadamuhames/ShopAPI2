from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('home', views.HomePage.as_view()),
    path('cotalog', views.CotalogView.as_view()),
    path("category/<int:pk>", views.CategoryDeteilView.as_view()),
    path('category-products/<int:pk>', views.CategoryProducts.as_view()),
    path('product/<int:pk>', views.ProductDetailView.as_view()),
    path("all_categories", views.GetCategories.as_view()),
    path('like', views.Like.as_view()),
    path('unlike', views.UnLike.as_view()),
    path("add_to_cart", views.AddToCart.as_view()),
    path("cart_view", views.CartView.as_view()),
    path('wishlist_view', views.WishlistView.as_view()),
    path("del_from_cart", views.RemoveFromCart.as_view()),
    path('get_modal/<int:pk>', views.GetModalData.as_view()),
    path("change-count", views.ChangeCount.as_view()),
    path('search', views.SearchView.as_view())
]
