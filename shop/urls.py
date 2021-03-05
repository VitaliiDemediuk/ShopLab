from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index),
    path('index/', index),
    path('brands/', brands),
    path('brands/<str:brand_link_name>', brand),
    path('product/<int:product_id>', product),
    path('section/<str:section_link_name>', section),
    path('section/<str:section_link_name>/<str:category_link_name>', category),
]