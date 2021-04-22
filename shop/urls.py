from django.urls import path, include
import shop.views.import_export_views as import_export_views
import shop.views.views as views

urlpatterns = [
    path('', views.index),
    path('index/', views.index),
    path('brands/', views.brands),
    path('stats/', views.stats),
    path('import-export', import_export_views.import_export),
    path('get-products-xlsx', import_export_views.get_products_xlsx),
    path('get-products-docx', import_export_views.get_products_docx),
    path('import-xlsx', import_export_views.import_xlsx),
    path('brands/<str:brand_link_name>', views.brand),
    path('product/<int:product_id>', views.product),
    path('section/<str:section_link_name>', views.section),
    path('section/<str:section_link_name>/<str:category_link_name>', views.category),
]