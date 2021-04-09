from shop.services.all_moduls_for_services import *

# Export file
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
        characteristics = goods_services.get_characteristics_by_id(product.id)
        for i, characteristic in enumerate(characteristics):
            ws_products.cell(row=k, column=column_list_number + 2 * i + 1,
                             value=f"{characteristic['name']}")
            ws_products.cell(row=k, column=column_list_number + 2 * i + 2,
                             value=f"{characteristic['value']}")

        photos = goods_services.get_photos_by_id(product.id)
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

    products = goods_services.get_goods_query_set(section_link_name, category_id= category_id, brand_id= brand_id)
    __add_products_to_spreadsheet(ws_products, products, len(column_list), max_number_characteristics)

    return wb


def get_products_document(section_link_name = None, category_id = None, brand_id = None):
    document = docx.Document()
    products = goods_services.get_goods_query_set(section_link_name, category_id= category_id, brand_id= brand_id)
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
            photos = goods_services.get_photos_by_id(product.id)
            for photo in photos:
                document.add_picture(f'{MEDIA_ROOT}/{photo}', width=docx.shared.Cm(7))
            characteristics = goods_services.get_characteristics_by_id(product.id)
            table = document.add_table(rows=len(characteristics), cols=2)
            for i, characteristic in enumerate(characteristics):
                cell = table.cell(i, 0)
                cell.text = characteristic['name']
                cell = table.cell(i, 1)
                cell.text = characteristic['value']

    return document