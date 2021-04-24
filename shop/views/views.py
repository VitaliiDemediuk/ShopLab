from shop.views.all_moduls_for_views import *

def index(request):
    sections = section_brand_service.get_sections_with_categories()
    photo_for_slider = shop_service.get_photos_for_slider()
    return render(request, 'shop/index.html', {'sections': sections,
                                               "photo_count_range": range(1, len(photo_for_slider)),
                                               "photo_for_slider": photo_for_slider,
                                               'img_link_prefix': IMG_LINK_PREFIX})


def brands(request):
    sections = section_brand_service.get_sections_with_categories()
    all_brands = section_brand_service.get_brands()
    return render(request, 'shop/brands.html', {'sections': sections,
                                                'brands': all_brands,
                                                'img_link_prefix': IMG_LINK_PREFIX})


def product(request, product_id):
    sections = section_brand_service.get_sections_with_categories()
    goods = goods_service.get_goods_by_id(product_id)
    if goods is None or not goods['is_enable']:
        return HttpResponse("Product not found!")
    else:
        return render(request, 'shop/product.html', {'sections': sections,
                                                     'goods': goods,
                                                     'img_link_prefix': IMG_LINK_PREFIX})


def section(request, section_link_name):
    sections = section_brand_service.get_sections_with_categories()
    goods_list = goods_service.get_goods_list(section_link_name=section_link_name)
    if goods_list is None:
        return HttpResponse("Section not found!")
    else:
        return render(request, 'shop/product_list.html', {'sections': sections,
                                                          'goods_list': goods_list,
                                                          'img_link_prefix': IMG_LINK_PREFIX})


def category(request, section_link_name, category_link_name):
    sections = section_brand_service.get_sections_with_categories()
    goods_list = goods_service.get_goods_list(section_link_name=section_link_name, category_link_name=category_link_name)
    if goods_list is None:
        return HttpResponse("Category not found!")
    else:
        return render(request, 'shop/product_list.html', {'sections': sections,
                                                          'goods_list': goods_list,
                                                          'img_link_prefix': IMG_LINK_PREFIX})


def brand(request, brand_link_name):
    sections = section_brand_service.get_sections_with_categories()
    goods_list = goods_service.get_goods_list(brand_link_name=brand_link_name)
    if goods_list is None:
        return HttpResponse("Brand not found!")
    else:
        return render(request, 'shop/product_list.html', {'sections': sections,
                                                          'goods_list': goods_list,
                                                          'img_link_prefix': IMG_LINK_PREFIX,
                                                          'link_prefix': DOMAIN})


def stats(request):
    sections = section_brand_service.get_sections_with_categories()
    number_of_products_in_each_section = shop_service.get_number_of_products_in_each_section
    number_of_products_in_each_category = shop_service.get_number_of_products_in_each_category()
    return render(request, 'shop/stats.html', {'sections': sections,
                                               'number_of_products_in_each_section': number_of_products_in_each_section,
                                               'number_of_products_in_each_category': number_of_products_in_each_category,})