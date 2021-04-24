from django.urls import path, include
from django.contrib.auth import views as django_views
import shop.views.import_export_views as import_export_views
import shop.views.account_view as account_view
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
    path('account/', account_view.account, name='account'),
    path('registration/', account_view.registration, name='registration'),
    path('login/', account_view.user_login, name='login'),
    path('logout/', account_view.user_logout, name='logout'),
    path('password-reset/', django_views.PasswordResetView.as_view(), name='password-reset'),
]