from django.urls import path
from django.conf.urls import url
from rango import views

app_name = 'rango'

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
    path('add_category/', views.add_category, name='add_category'),
    path('product/<slug:product_name_slug>/', views.show_product, name='show_product'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('restricted/', views.restricted, name='restricted'),
    path('logout/', views.user_logout, name='logout'),
    path('buyer-my-account/', views.buyer_my_account, name='buyer_my_account'),
    path('cart/', views.cart, name='cart'),
    path('payment/', views.payment, name='payment'),
    path('seller-my-account/', views.seller_my_account, name='seller_my_account'),
    path('upload-product/', views.upload_product, name='upload_product'),
    path('remove-product/', views.remove_product, name='remove_product'),
    path('product-search/', views.product_search, name='product_search'),
]