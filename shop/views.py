from django.shortcuts import render
from django.http import HttpResponse
from ShopLabWork.settings import DOMAIN, MEDIA_URL
from shop.services.shop_services import *

def index(request):
    sections = get_sections_with_categories()
    return render(request, 'shop/index.html', {'sections': sections})


def brands(request):
    sections = get_sections_with_categories()
    all_brands = get_brands()
    return render(request, 'shop/brands.html', {'sections': sections,
                                                'brands': all_brands,
                                                'img_link_prefix': DOMAIN+MEDIA_URL})


def product(request, product_id):
    sections = get_sections_with_categories()
    goods = get_goods_by_id(product_id)
    if goods is None or not goods['is_enable']:
        return HttpResponse("Product not found!")
    else:
        return render(request, 'shop/product.html', {'sections': sections,
                                                     'goods': goods,
                                                     'img_link_prefix': DOMAIN + MEDIA_URL})


def section(request, section_link_name):
    sections = get_sections_with_categories()
    goods_list = get_goods_list(section_link_name=section_link_name)
    if goods_list is None:
        return HttpResponse("Section not found!")
    else:
        return render(request, 'shop/product_list.html', {'sections': sections,
                                                          'goods_list': goods_list,
                                                          'img_link_prefix': DOMAIN + MEDIA_URL})


def category(request, section_link_name, category_link_name):
    sections = get_sections_with_categories()
    goods_list = get_goods_list(section_link_name=section_link_name, category_link_name=category_link_name)
    if goods_list is None:
        return HttpResponse("Category not found!")
    else:
        return render(request, 'shop/product_list.html', {'sections': sections,
                                                          'goods_list': goods_list,
                                                          'img_link_prefix': DOMAIN + MEDIA_URL})


def brand(request, brand_link_name):
    sections = get_sections_with_categories()
    goods_list = get_goods_list(brand_link_name=brand_link_name)
    if goods_list is None:
        return HttpResponse("Brand not found!")
    else:
        return render(request, 'shop/product_list.html', {'sections': sections,
                                                          'goods_list': goods_list,
                                                          'img_link_prefix': DOMAIN + MEDIA_URL,
                                                          'link_prefix': DOMAIN})