from shop.models import *


def get_sections_with_categories():
    sections = list(Section.objects.all().values('id', 'name', 'name_for_link'))
    for section in sections:
        section['category'] = list(Category.objects.filter(fk_section_id=section['id']).values('name', 'name_for_link'))
    return sections


def get_brands():
    brands = list(Brand.objects.all().values('name', 'name_for_link', 'photo'))
    return brands


def get_sizes_by_id(id: int):
    sizes = []
    sizes_query_set = SizesGoods.objects.filter(fk_goods_id=id)
    for size in sizes_query_set:
        sizes.append({'id': size.fk_size_id.id, 'name': size.fk_size_id.name})
    return sizes


def get_photos_by_id(id: int):
    photos = list(PhotoForGoods.objects.filter(fk_goods_id=id).values_list('file_name', flat=True))
    return photos


def get_characteristics_by_id(id: int):
    characteristics = []
    characteristics_query_set = CharacteristicsGoods.objects.filter(fk_goods_id=id)
    for characteristic in characteristics_query_set:
        characteristics.append({'name': characteristic.fk_characteristic_id.name, 'value': characteristic.value})
    return characteristics


def get_goods_by_id(id: int):
    goods_query_set = Goods.objects.filter(pk=id)
    goods = None
    if len(goods_query_set) != 0:
        goods = list(goods_query_set.values('id', 'title', 'price', 'sale_price', 'main_photo',
                                            'in_stock', 'is_enable', 'description'))[0]
        goods['brand'] = str(goods_query_set[0].fk_brand_id)
        goods['category'] = str(goods_query_set[0].fk_category_id)
        goods['color'] = str(goods_query_set[0].fk_color_id)
        goods['sizes'] = get_sizes_by_id(id)
        goods['photos'] = get_photos_by_id(id)
        goods['characteristics'] = get_characteristics_by_id(id)

    return goods


def get_number_of_products_in_each_category():
    sql_query = 'SELECT "shop_goods"."fk_category_id_id" AS "id", ' \
                'CONCAT("shop_section"."name", \' / \' ,"shop_category"."name") AS "full_name", ' \
                'COUNT("shop_goods"."id") AS "number" FROM "shop_goods" ' \
                'INNER JOIN "shop_category" ON ("shop_goods"."fk_category_id_id" = "shop_category"."id") ' \
                'INNER JOIN "shop_section" ON ("shop_category"."fk_section_id_id" = "shop_section"."id") ' \
                'GROUP BY "shop_goods"."fk_category_id_id", "shop_section"."name", "shop_category"."name";'
    number_of_products = Goods.objects.raw(sql_query)
    return number_of_products


def get_number_of_products_in_each_section():
    sql_query = 'SELECT "shop_section"."id" AS "id", ' \
                '"shop_section"."name", ' \
                'COUNT("shop_goods"."id") AS "number" FROM "shop_goods" ' \
                'INNER JOIN "shop_category" ON ("shop_goods"."fk_category_id_id" = "shop_category"."id") ' \
                'INNER JOIN "shop_section" ON ("shop_category"."fk_section_id_id" = "shop_section"."id") ' \
                'GROUP BY "shop_section"."id", "shop_section"."name";'
    number_of_products = Goods.objects.raw(sql_query)
    return number_of_products

# GOODS LIST
def filter_goods_by_section_link_name(goods_list_query_set, section_link_name):
    if section_link_name is not None:
        section_id = Section.objects.filter(name_for_link=section_link_name).values('id')
        if len(section_id) == 0:
            return None
        else:
            category_ids = list(Category.objects.filter(fk_section_id=section_id[0]['id']).values_list('id', flat=True))
            goods_list_query_set = goods_list_query_set.filter(fk_category_id__in=category_ids)
    return goods_list_query_set


def filter_goods_by_category_link_name(goods_list_query_set, category_link_name):
    if category_link_name is not None:
        category_id = list(Category.objects.filter(name_for_link=category_link_name).values_list('id', flat=True))
        if len(category_id) == 0:
            return None
        else:
            goods_list_query_set = goods_list_query_set.filter(fk_category_id__in=category_id)
    return goods_list_query_set


def filter_goods_by_brand_link_name(goods_list_query_set, brand_link_name):
    if brand_link_name is not None:
        brand_id = list(Brand.objects.filter(name_for_link=brand_link_name).values('id'))
        if len(brand_id) == 0:
            return None
        else:
            brand_id = brand_id[0]['id']
            goods_list_query_set = goods_list_query_set.filter(fk_brand_id=brand_id)
    return goods_list_query_set


def get_goods_list(section_link_name = None, category_link_name = None, brand_link_name = None):
    goods_list_query_set = Goods.objects.all()
    # Filter by section:
    goods_list_query_set = filter_goods_by_section_link_name(goods_list_query_set, section_link_name)
    if goods_list_query_set is None:
        return None
    # Filter by category:
    goods_list_query_set = filter_goods_by_category_link_name(goods_list_query_set, category_link_name)
    if goods_list_query_set is None:
        return None
    # Filter by brand:
    goods_list_query_set = filter_goods_by_brand_link_name(goods_list_query_set, brand_link_name)
    if goods_list_query_set is None:
        return None

    goods_list = list(goods_list_query_set.filter(is_enable=True).values('id', 'title', 'price',
                                                                         'sale_price', 'main_photo', 'in_stock'))
    return goods_list