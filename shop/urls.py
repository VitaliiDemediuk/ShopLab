from django.urls import path, include
from django.contrib.auth import views as django_views
import shop.views.import_export_views as import_export_views
import shop.views.account_views as account_views
import shop.views.views as views

urlpatterns = [
    path('', views.index),
    path('index/', views.index, name='index'),
    path('brands/', views.brands, name='brands'),
    path('stats/', views.stats, name='stats'),
    path('import-export/', import_export_views.import_export, name='import-export'),
    path('get-products-xlsx/', import_export_views.get_products_xlsx, name='get-products-xlsx'),
    path('get-products-docx/', import_export_views.get_products_docx, name='get-products-docx'),
    path('import-xlsx/', import_export_views.import_xlsx, name='import-xlsx'),
    path('brands/<str:brand_link_name>/', views.brand),
    path('product/<int:product_id>/', views.product),
    path('section/<str:section_link_name>/', views.section),
    path('section/<str:section_link_name>/<str:category_link_name>/', views.category),
    path('account/', account_views.account, name='account'),
    path('registration/', account_views.registration, name='registration'),
    path('login/', account_views.user_login, name='login'),
    path('logout/', account_views.user_logout, name='logout'),
    path('email-verification/', account_views.email_verification, name='email-verification'),
    path('forgot-password', account_views.forgot_password, name='forgot-password'),
    path('reset-password/', account_views.reset_password, name='reset-password'),
    path('basket/', views.basket, name='basket'),
]