from shop.services.all_moduls_for_services import *

def get_photos_for_slider():
    photos = list(PhotoForSlider.objects.all().values('file_name'))
    return photos

def get_photos_path_by_id(id: int):
    photos = list(PhotoForGoods.objects.filter(fk_goods_id=id).values_list('file_name', flat=True))
    return photos


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