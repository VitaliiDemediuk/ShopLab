from shop.services.all_moduls_for_service import *

# GOODS ----------------------------------------------------------------------------------------------------------------

def __get_sizes_by_id(id: int):
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
        goods['sizes'] = __get_sizes_by_id(id)
        goods['photos'] = get_photos_by_id(id)
        goods['characteristics'] = get_characteristics_by_id(id)

    return goods

# GOODS LIST -----------------------------------------------------------------------------------------------------------
def __filter_goods_by_section_link_name(goods_list_query_set, section_link_name):
    if section_link_name is not None:
        section_id = Section.objects.filter(name_for_link=section_link_name).values('id')
        if len(section_id) == 0:
            return None
        else:
            category_ids = list(Category.objects.filter(fk_section_id=section_id[0]['id']).values_list('id', flat=True))
            goods_list_query_set = goods_list_query_set.filter(fk_category_id__in=category_ids)
    return goods_list_query_set


def __filter_goods_by_category_link_name(goods_list_query_set, category_link_name):
    if category_link_name is not None:
        category_id = list(Category.objects.filter(name_for_link=category_link_name).values_list('id', flat=True))
        if len(category_id) == 0:
            return None
        else:
            goods_list_query_set = goods_list_query_set.filter(fk_category_id__in=category_id)
    return goods_list_query_set


def __filter_goods_by_category_id(goods_list_query_set, category_id):
    if category_id is not None:
        goods_list_query_set = goods_list_query_set.filter(fk_category_id__in=category_id)
    return goods_list_query_set


def __filter_goods_by_brand_link_name(goods_list_query_set, brand_link_name):
    if brand_link_name is not None:
        brand_id = list(Brand.objects.filter(name_for_link=brand_link_name).values('id'))
        if len(brand_id) == 0:
            return None
        else:
            brand_id = brand_id[0]['id']
            goods_list_query_set = goods_list_query_set.filter(fk_brand_id=brand_id)
    return goods_list_query_set


def __filter_goods_by_brand_id(goods_list_query_set, brand_id):
    if brand_id is not None:
        goods_list_query_set = goods_list_query_set.filter(fk_brand_id__in=brand_id)
    return goods_list_query_set


def get_goods_query_set(section_link_name = None, category_id = None, brand_id = None, category_link_name = None, brand_link_name = None):
    goods_list_query_set = Goods.objects.all()
    # Filter by section:
    goods_list_query_set = __filter_goods_by_section_link_name(goods_list_query_set, section_link_name)
    if goods_list_query_set is None:
        return None
    # Filter by category link name:
    goods_list_query_set = __filter_goods_by_category_link_name(goods_list_query_set, category_link_name)
    if goods_list_query_set is None:
        return None
    # Filter by category id:
    goods_list_query_set = __filter_goods_by_category_id(goods_list_query_set, category_id)
    if goods_list_query_set is None:
        return None
    # Filter by brand:
    goods_list_query_set = __filter_goods_by_brand_link_name(goods_list_query_set, brand_link_name)
    if goods_list_query_set is None:
        return None
    # Filter by brand id:
    goods_list_query_set = __filter_goods_by_brand_id(goods_list_query_set, brand_id)
    if goods_list_query_set is None:
        return None

    return goods_list_query_set


def get_goods_list(section_link_name = None, category_id = None, brand_id = None, category_link_name = None, brand_link_name = None):
    goods_list_query_set = get_goods_query_set(section_link_name=section_link_name, category_id = category_id, brand_id = brand_id,
                                               category_link_name=category_link_name, brand_link_name=brand_link_name)
    goods_list = list(goods_list_query_set.filter(is_enable=True).values('id', 'title', 'price',
                                                                         'sale_price', 'main_photo', 'in_stock'))
    return goods_list