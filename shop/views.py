import ast
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from ShopLabWork.settings import DOMAIN, MEDIA_URL
from shop.services.shop_services import *

IMG_LINK_PREFIX = DOMAIN + MEDIA_URL

def index(request):
    sections = get_sections_with_categories()
    photo_for_slider = get_photos_for_slider()
    return render(request, 'shop/index.html', {'sections': sections,
                                               "photo_count_range": range(1, len(photo_for_slider)),
                                               "photo_for_slider": photo_for_slider,
                                               'img_link_prefix': IMG_LINK_PREFIX})


def brands(request):
    sections = get_sections_with_categories()
    all_brands = get_brands()
    return render(request, 'shop/brands.html', {'sections': sections,
                                                'brands': all_brands,
                                                'img_link_prefix': IMG_LINK_PREFIX})


def product(request, product_id):
    sections = get_sections_with_categories()
    goods = get_goods_by_id(product_id)
    if goods is None or not goods['is_enable']:
        return HttpResponse("Product not found!")
    else:
        return render(request, 'shop/product.html', {'sections': sections,
                                                     'goods': goods,
                                                     'img_link_prefix': IMG_LINK_PREFIX})


def section(request, section_link_name):
    sections = get_sections_with_categories()
    goods_list = get_goods_list(section_link_name=section_link_name)
    if goods_list is None:
        return HttpResponse("Section not found!")
    else:
        return render(request, 'shop/product_list.html', {'sections': sections,
                                                          'goods_list': goods_list,
                                                          'img_link_prefix': IMG_LINK_PREFIX})


def category(request, section_link_name, category_link_name):
    sections = get_sections_with_categories()
    goods_list = get_goods_list(section_link_name=section_link_name, category_link_name=category_link_name)
    if goods_list is None:
        return HttpResponse("Category not found!")
    else:
        return render(request, 'shop/product_list.html', {'sections': sections,
                                                          'goods_list': goods_list,
                                                          'img_link_prefix': IMG_LINK_PREFIX})


def brand(request, brand_link_name):
    sections = get_sections_with_categories()
    goods_list = get_goods_list(brand_link_name=brand_link_name)
    if goods_list is None:
        return HttpResponse("Brand not found!")
    else:
        return render(request, 'shop/product_list.html', {'sections': sections,
                                                          'goods_list': goods_list,
                                                          'img_link_prefix': IMG_LINK_PREFIX,
                                                          'link_prefix': DOMAIN})


def stats(request):
    sections = get_sections_with_categories()
    number_of_products_in_each_section = get_number_of_products_in_each_section
    number_of_products_in_each_category = get_number_of_products_in_each_category()
    return render(request, 'shop/stats.html', {'sections': sections,
                                               'number_of_products_in_each_section': number_of_products_in_each_section,
                                               'number_of_products_in_each_category': number_of_products_in_each_category,})


def import_export(request):
    sections = get_sections_with_categories()
    sections_for_tree = get_sections_with_categories_for_tree()
    brands_for_tree = get_brands_for_tree()
    return render(request, 'shop/import-export.html', {'sections': sections,
                                                       'sections_for_tree': sections_for_tree,
                                                       'brands_for_tree': brands_for_tree})


def _get_categories_id_from_request(request):
    categories_id = request.GET.get('categories')
    if categories_id:
        categories_id = ast.literal_eval(categories_id)
    return categories_id


def _get_brands_id_from_request(request):
    brands_id = request.GET.get('brands')
    if brands_id:
        brands_id = ast.literal_eval(brands_id)
    return brands_id


def get_products_xlsx(request):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    now = datetime.today().strftime("%d_%m_%Y-%H_%M_%S")
    response['Content-Disposition'] = f'attachment; filename=products-{now}.xlsx'

    categories_id = _get_categories_id_from_request(request)
    brands_id = _get_brands_id_from_request(request)

    wb = get_products_workbook(category_id=categories_id, brand_id=brands_id)
    wb.save(response)

    return response


def get_products_docx(request):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    now = datetime.today().strftime("%d_%m_%Y-%H_%M_%S")
    response['Content-Disposition'] = f'attachment; filename=products-{now}.docx'

    categories_id = _get_categories_id_from_request(request)
    brands_id = _get_brands_id_from_request(request)
    print(brands_id)

    document = get_products_document(category_id=categories_id, brand_id=brands_id)
    document.save(response)

    return response