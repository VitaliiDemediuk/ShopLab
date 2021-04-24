from shop.services.all_moduls_for_service import *
from enum import Enum

import os
from django.core.files import File
from urllib.request import urlopen
from tempfile import NamedTemporaryFile
from django.db import DatabaseError, transaction
from django.core.exceptions import ValidationError

# EXPORT FILE-----------------------------------------------------------------------------------------------------------

def __get_max_number_characteristics_in_product():
    max = CharacteristicsGoods.objects.values('fk_goods_id')\
                               .annotate(total=Count('fk_characteristic_id'))\
                               .aggregate(max=Max('total'))['max']
    return max if max else 0


def __get_max_number_photos_in_product():
    max = PhotoForGoods.objects.values('fk_goods_id')\
                       .annotate(total=Count('file_name'))\
                       .aggregate(max=Max('total'))['max']
    return max if max else 0


def __add_hearer_to_spreadsheet(ws_products, column_list, max_number_characteristics, max_number_photos):
    ws_products.append(column_list)
    column_list_number = len(column_list)

    for i in range(max_number_characteristics):
        ws_products.cell(row=1, column=column_list_number + 2 * i + 1,
                         value=f"ch_name_{i + 1}")
        ws_products.cell(row=1, column=column_list_number + 2 * i + 2,
                         value=f"ch_value_{i + 1}")

    for i in range(max_number_photos):
        ws_products.cell(row=1,
                         column=column_list_number + 2 * max_number_characteristics + i + 1,
                         value=f"photo_{i + 1}")


def __add_products_to_spreadsheet(ws_products, products, column_list_number, max_number_characteristics):
    for k, product in enumerate(products, start=2):
        product_data_list = [product.sku, product.title, product.price, product.sale_price,
                             product.description, product.count, product.sale_price != 0, product.in_stock,
                             product.is_enable, product.fk_brand_id.name, product.fk_category_id.fk_section_id.name,
                             product.fk_category_id.name, product.fk_color_id.name, product.main_photo.url]
        ws_products.append(product_data_list)
        characteristics = goods_service.get_characteristics_by_id(product.id)
        for i, characteristic in enumerate(characteristics):
            ws_products.cell(row=k, column=column_list_number + 2 * i + 1,
                             value=f"{characteristic['name']}")
            ws_products.cell(row=k, column=column_list_number + 2 * i + 2,
                             value=f"{characteristic['value']}")

        photos = goods_service.get_photos_by_id(product.id)
        for i, photo in enumerate(photos):
            ws_products.cell(row=k,
                             column=column_list_number + 2 * max_number_characteristics + i + 1,
                             value=f"{photo}")


def get_products_workbook(section_link_name = None, category_id = None, brand_id = None):
    wb = openpyxl.Workbook()
    ws_products = wb.active
    ws_products.title = "Products"

    column_list = ['sku', 'title', 'price', 'sale_price', 'description', 'count', 'is_sale', 'in_stock',
                   'is_enable', 'brand', 'section', 'category', 'color', 'main photo']
    max_number_characteristics = __get_max_number_characteristics_in_product()
    max_number_photos = __get_max_number_photos_in_product()
    __add_hearer_to_spreadsheet(ws_products, column_list, max_number_characteristics, max_number_photos)

    products = goods_service.get_goods_query_set(section_link_name, category_id= category_id, brand_id= brand_id)
    __add_products_to_spreadsheet(ws_products, products, len(column_list), max_number_characteristics)

    return wb


def get_products_document(section_link_name = None, category_id = None, brand_id = None):
    document = docx.Document()
    products = goods_service.get_goods_query_set(section_link_name, category_id= category_id, brand_id= brand_id)
    for product in products:
        if product.is_enable:
            document.add_heading(f'SKU: {product.sku}', 2)
            document.add_heading(product.title, 0)
            document.add_picture(f'{product.main_photo.path}', width=docx.shared.Cm(10))
            document.add_heading(f'Price: {product.price}', 2)
            if product.sale_price != 0:
                run = document.add_paragraph().add_run(f'Sale price: {product.sale_price}')
                font = run.font
                font = run.font
                font.color.rgb = RGBColor.from_string('FF0000')
            document.add_heading(f'Color: {product.fk_color_id.name}', 2)
            document.add_heading(f'Brand: {product.fk_brand_id.name}', 2)
            document.add_heading(f'Section: {product.fk_category_id.fk_section_id.name}', 2)
            document.add_heading(f'Category: {product.fk_category_id.name}', 2)
            document.add_heading(f'Description:', 2)
            document.add_paragraph(product.description)
            photos = goods_service.get_photos_by_id(product.id)
            for photo in photos:
                document.add_picture(f'{MEDIA_ROOT}/{photo}', width=docx.shared.Cm(7))
            characteristics = goods_service.get_characteristics_by_id(product.id)
            table = document.add_table(rows=len(characteristics), cols=2)
            for i, characteristic in enumerate(characteristics):
                cell = table.cell(i, 0)
                cell.text = characteristic['name']
                cell = table.cell(i, 1)
                cell.text = characteristic['value']

    return document

# IMPORT FILE-----------------------------------------------------------------------------------------------------------

# Header ---
HEADER_TUPLE = ('sku', 'title', 'price',
                'sale_price', 'description',
                'count', 'is_sale', 'in_stock',
                'is_enable', 'brand', 'section',
                'category', 'color', 'main photo')

def __check_header(header: tuple) -> bool:
    return_value = len(header) < len(HEADER_TUPLE)
    if not return_value:
        return header[:len(HEADER_TUPLE)] == HEADER_TUPLE
    return return_value

# return -1 if header is not correct
def __get_characteristic_count(header: tuple) -> int:
    count = 0
    column_i = len(HEADER_TUPLE)
    while column_i+1 < len(header) and \
          'ch_name_' + str(count+1) == header[column_i]:
        if 'ch_value_' + str(count+1) != header[column_i+1]:
            count = -1
            break
        count += 1
        column_i += 2

    return count


# return -1 if header is not correct
def __get_photo_count(header: tuple, characteristic_count) -> int:
    count = 0
    start_i = len(HEADER_TUPLE) + characteristic_count * 2
    for i in range(start_i, len(header)):
        count += 1
        if 'photo_' + str(count) != header[i]:
            count = -1
            break

    return count

# Product ---
def __get_dict_from_product_tuple(product: tuple, characteristic_count):
    result = dict()
    result['characteristics'] = list()
    result['photos'] = list()
    for i, attr in enumerate(HEADER_TUPLE):
        result[attr] = product[i]
    for i in range(len(HEADER_TUPLE), len(HEADER_TUPLE) + characteristic_count*2, 2):
        if not product[i]:
            break
        result['characteristics'].append((product[i], product[i+1]))
    for i in range(len(HEADER_TUPLE)+characteristic_count*2, len(product)):
        if not product[i]:
            break
        result['photos'].append((product[i]))

    return result

# adding new brand if brand not exist in the table
def __get_brand_instance(brand_name: str):
    result = None
    brand_query_set = Brand.objects.filter(name=brand_name)
    if len(brand_query_set) > 0:
        result = brand_query_set[0]
    else:
        result = Brand(name=brand_name, name_for_link=brand_name)
        result.save()
    return result

# adding new section if section not exist in the table
def __get_section_instance(section_name: str):
    result = None
    section_query_set = Section.objects.filter(name=section_name)
    if len(section_query_set) > 0:
        result = section_query_set[0]
    else:
        result = Section(name=section_name)
        result.save()
    return result

# adding new category if category not exist in the table
def __get_category_instance(category_name: str, section_name: str):
    result = None
    section_instance = __get_section_instance(section_name)
    category_query_set = Category.objects.filter(name=category_name, fk_section_id=section_instance)
    if len(category_query_set) > 0:
        result = category_query_set[0]
    else:
        result = Category(name=category_name, name_for_link=category_name, fk_section_id=section_instance)
        result.save()
    return result

# adding new color if color not exist in the table
def __get_color_instance(color_name: str):
    result = None
    color_query_set = Color.objects.filter(name=color_name)
    if len(color_query_set) > 0:
        result = color_query_set[0]
    else:
        result = Color(name=color_name, hex="#000000")
        result.save()
    return result

# adding new characteristic if characteristic not exist in the table
def __get_characteristic_instance(characteristic_name: str):
    result = None
    characteristic_query_set = Characteristic.objects.filter(name=characteristic_name)
    if len(characteristic_query_set) > 0:
        result = characteristic_query_set[0]
    else:
        result = Characteristic(name=characteristic_name)
        result.save()
    return result


def __add_characteristics_for_product(goods_instance, characteristics):
    old_characteristics_query = CharacteristicsGoods.objects.filter(fk_goods_id=goods_instance)
    old_characteristics_query.delete()
    for name, value in characteristics:
        characteristic_instance = __get_characteristic_instance(name)
        new_instance = CharacteristicsGoods(fk_characteristic_id=characteristic_instance,
                                            fk_goods_id=goods_instance,
                                            value=value)
        new_instance.save()


def __add_photos_for_product(goods_instance, photos):
    old_photos_query = PhotoForGoods.objects.filter(fk_goods_id=goods_instance)
    old_photos_query.delete()
    for photo in photos:
        photo_instance = PhotoForGoods(fk_goods_id=goods_instance)
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(urlopen(photo).read())
        img_temp.flush()
        photo_instance.file_name.save(os.path.basename(photo), File(img_temp))
        photo_instance.save()


def __add_product(product_dict: dict) -> bool:
    new_goods = Goods(sku=product_dict['sku'],
                      title=product_dict['title'],
                      price=product_dict['price'],
                      sale_price=product_dict['sale_price'],
                      description=product_dict['description'],
                      count=product_dict['count'],
                      fk_brand_id=__get_brand_instance(product_dict['brand']),
                      fk_category_id=__get_category_instance(product_dict['category'], product_dict['section']),
                      fk_color_id=__get_color_instance(product_dict['color']))

    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(urlopen(product_dict['main photo']).read())
    img_temp.flush()
    new_goods.main_photo.save(os.path.basename(product_dict['main photo']), File(img_temp))
    new_goods.save()
    __add_photos_for_product(new_goods, product_dict['photos'])
    __add_characteristics_for_product(new_goods, product_dict['characteristics'])
    return True


def __update_product(product_dict: dict) -> bool:
    goods_to_update = Goods.objects.get(sku=product_dict['sku'])

    goods_to_update.title = product_dict['title']
    goods_to_update.price = product_dict['price']
    goods_to_update.sale_price = product_dict['sale_price']
    goods_to_update.description = product_dict['description']
    goods_to_update.count = product_dict['count']
    goods_to_update.fk_brand_id = __get_brand_instance(product_dict['brand'])
    goods_to_update.fk_category_id = __get_category_instance(product_dict['category'], product_dict['section'])
    goods_to_update.fk_color_id = __get_color_instance(product_dict['color'])

    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(urlopen(product_dict['main photo']).read())
    img_temp.flush()
    goods_to_update.main_photo.save(os.path.basename(product_dict['main photo']), File(img_temp))
    goods_to_update.save()
    __add_photos_for_product(goods_to_update, product_dict['photos'])
    __add_characteristics_for_product(goods_to_update, product_dict['characteristics'])
    return True


class ImportProductStatus(Enum):
    ERROR = 0
    ADDED = 1
    UPDATED = 2


def __import_product(product: tuple, characteristic_count, log: list) -> ImportProductStatus:
    product_dict = __get_dict_from_product_tuple(product, characteristic_count)
    status = ImportProductStatus.ADDED
    try:
        with transaction.atomic():
            if len(Goods.objects.filter(sku=product_dict['sku'])) > 0:
                status = ImportProductStatus.UPDATED
                if not __update_product(product_dict):
                    status = ImportProductStatus.ERROR
                    log.append(f'Successfully added the product with sku={product_dict["sku"]}')
                log.append(f'Unsuccessfully added the product with sku={product_dict["sku"]}')
            else:
                if not __add_product(product_dict):
                    status = ImportProductStatus.ERROR
                    log.append(f'Unsuccessfully added the product with sku={product_dict["sku"]}')
                log.append(f'Successfully added the product with sku={product_dict["sku"]}')
    except DatabaseError as err:
        status = ImportProductStatus.ERROR
        log.append(str(err))
        log.append(f'Unsuccessfully added the product with sku={product_dict["sku"]}')
    except ValidationError as err:
        status = ImportProductStatus.ERROR
        log.append(str(err))
        log.append(f'Unsuccessfully added the product with sku={product_dict["sku"]}')
    return status


def import_xlsx_file(xlsx_file):
    wb = openpyxl.load_workbook(xlsx_file)
    ws = wb.worksheets[0]
    table = list(ws.values)
    is_correct_header = False
    characteristic_count, photo_count = 0, 0
    errors, added, updated = 0, 0, 0
    log = list()

    if len(table):
        is_correct_header = __check_header(table[0])

    if is_correct_header:
        characteristic_count = __get_characteristic_count(table[0])
        is_correct_header = characteristic_count != -1

    if is_correct_header:
        photo_count = __get_photo_count(table[0], characteristic_count)
        is_correct_header = photo_count != -1

    if is_correct_header:
        for i in range(1, len(table)):
            if table[i] != (None,) * len(table[i]):
                status = __import_product(table[i], characteristic_count, log)
                if status == ImportProductStatus.ERROR:
                    errors += 1
                elif status == ImportProductStatus.ADDED:
                    added += 1
                else:
                    updated += 1
            else:
                log.append("Empty row")
    else:
        log.append("Incorrect header!")
    import_report = {'is_correct_header': is_correct_header,
                     'errors': errors,
                     'added': added,
                     'updated': updated,
                     'log': log}
    return import_report