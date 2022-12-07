from re import template
from django.urls import path, include
from . import views
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Permission

urlpatterns = [
    path('', views.open_main, name='home-page'),
    path('', 
        user_passes_test(lambda u: u.has_perm('auth.view_admin'), login_url='home-page')(views.open_main),
        name='admin-page'),
    path('products', user_passes_test(lambda u: u.has_perm("main.view_products"), login_url='home-page')(views.ProductsView.as_view()), name='products-admin'),
    path('products_edit/<int:pk>', user_passes_test(lambda u: u.has_perm("main.change_products"), login_url='home-page')(views.EditProductAdmin.as_view()), name='edit-product'),
    path('delete-products/<int:pk>', user_passes_test(lambda u: u.has_perm("main.delete_products"), login_url='home-page')(views.DeleteProducts), name='del-prod'),
    path('del-image/<int:pk>', user_passes_test(lambda u: u.has_perm('main.add_products'), login_url='home-page')(views.del_products_image), name='del-image'),
    path("add_ctg", user_passes_test(lambda u: u.has_perm("main.add_categories"), login_url='home-page')(views.AddCateg.as_view()), name='add-ctg'),
    path('categories', user_passes_test(lambda u: u.has_perm("main.view_categories"), login_url='home-page')(views.CategoriesView.as_view()), name='categories'),
    path('update-category/<int:pk>', user_passes_test(lambda u: u.has_perm("main.change_categories"), login_url='home-page')(views.EditCtg.as_view()), name='update-ctg'),
    path("add_product", user_passes_test(lambda u: u.has_perm("main.add_products"), login_url='home-page')(views.AddProduct.as_view()), name='add_product'),
    path("orders_listing", user_passes_test(lambda u: u.has_perm("palpay.view_orders"), login_url='home-page')(views.OrdersView.as_view()), name='orders_listing'),
    path('order/<int:pk>', user_passes_test(lambda u: u.has_perm("palpay.change_orders"), login_url='home-page')(views.OrderDeteils.as_view()), name='order_details'),
    path("delete_order/<int:pk>", user_passes_test(lambda u: u.has_perm("palpay.delete_orders"), login_url='home-page')(views.delete_order), name='del_order'),
    path('FAQ', user_passes_test(lambda u: u.has_perm("admin.add_faq"), login_url='home-page')(views.AddFaq.as_view()), name='FAQ'),
    path("users_list", user_passes_test(lambda u: u.has_perm("auth.view_user"), login_url='home-page')(views.UsersList.as_view()), name='users_listing'),
    path("user/<int:pk>", user_passes_test(lambda u: u.has_perm("auth.change_user"), login_url='home-page')(views.UserDetails.as_view()), name='user_details'),
    path('roles', user_passes_test(lambda u: u.has_perm("auth.view_group"), login_url='home-page')(views.RolesList.as_view()), name='roles_list'),
    path("add_group", user_passes_test(lambda u: u.has_perm("auth.add_group"), login_url='home-page')(views.addGroup), name='add_group'),
    path("update-group/<int:pk>", user_passes_test(lambda u: u.has_perm("auth.change_group"), login_url='home-page')(views.UpdateRoles.as_view()), name='update-group'),
    path("del_user/<int:pk>", user_passes_test(lambda u: u.has_perm("auth.delete_user"),login_url='home-page')(views.del_user), name='del_user'),
    path('change_group', user_passes_test(lambda u: u.has_perm("auth.change_user"), login_url='home-page')(views.change_group), name='change_group'),
    path("create_user", user_passes_test(lambda u: u.has_perm("auth.add_user"), login_url='home-page')(views.ceate_user), name='create_user'),
    path('del_ctg/<int:pk>', user_passes_test(lambda u: u.has_perm("main.delete_category"), login_url='home-page')(views.del_ctg), name='del_ctg'),
    path('del_faq/<int:pk>', user_passes_test(lambda u: u.has_perm("admin.delete_faq"), login_url='home-page')(views.del_faq), name='del_faq'),
    path('create_variant', user_passes_test(lambda u: u.has_perm("main.add_productvariants"), login_url='home-page')(views.CreateVariant.as_view()), name='create-var-page'),
    path('get_atr', views.get_atribut, name='get_atrs'),
    path('del_var/<int:pk>', user_passes_test(lambda u: u.has_perm("main.delete_productvariants"), login_url='home-page')(views.del_variant), name='del_var'),
    path('variant_view/<int:pk>', user_passes_test(lambda u: u.has_perm("main.change_productvariants"), login_url='home-page')(views.UpdateVariant.as_view()), name='var_view'),
    path('varian_add', views.create_variant, name='create-variant-modal'),
    path('get_category/<int:id>', views.get_categories, name='get-ctg')
]