from shop.services.all_moduls_for_service import *

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


def get_basket_items_by_user(user):
    basket_items = []
    for item in Basket.objects.filter(fk_buyer_id=user):
        basket_items.append({'basket_item_id': item.id, 'photo_url': item.fk_goods_id.main_photo.url,
                             'goods_name': item.fk_goods_id.title, 'goods_id': item.fk_goods_id.id,
                             'size': item.fk_size_id.name, 'count': item.count})
    return basket_items

def delete_basket_item_by_id(id, user):
    basket_item = Basket.objects.filter(pk=id)
    if basket_item:
        basket_item = basket_item[0]
        if basket_item.fk_buyer_id == user:
            basket_item.delete()


def add_product_to_basket(goods_id: int, user, size_id: int, count: int):
    size = Size.objects.get(pk=size_id)
    goods = Goods.objects.get(pk=goods_id)
    basket_item = Basket(fk_goods_id=goods, fk_buyer_id=user, fk_size_id=size, count=count)
    basket_item.save()

