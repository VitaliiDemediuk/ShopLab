from shop.views.all_moduls_for_views import *
import openpyxl

def __get_categories_id_from_request(request):
    categories_id = request.GET.get('categories')
    if categories_id:
        categories_id = ast.literal_eval(categories_id)
    return categories_id


def __get_brands_id_from_request(request):
    brands_id = request.GET.get('brands')
    if brands_id:
        brands_id = ast.literal_eval(brands_id)
    return brands_id

def import_export(request):
    sections = section_brand_service.get_sections_with_categories()
    sections_for_tree = section_brand_service.get_sections_with_categories_for_tree()
    brands_for_tree = section_brand_service.get_brands_for_tree()
    return render(request, 'shop/import-export.html', {'sections': sections,
                                                       'sections_for_tree': sections_for_tree,
                                                       'brands_for_tree': brands_for_tree})


def get_products_xlsx(request):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    now = datetime.today().strftime("%d_%m_%Y-%H_%M_%S")
    response['Content-Disposition'] = f'attachment; filename=products-{now}.xlsx'

    categories_id = __get_categories_id_from_request(request)
    brands_id = __get_brands_id_from_request(request)

    wb = import_export_service.get_products_workbook(category_id=categories_id, brand_id=brands_id)
    wb.save(response)

    return response


def get_products_docx(request):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    now = datetime.today().strftime("%d_%m_%Y-%H_%M_%S")
    response['Content-Disposition'] = f'attachment; filename=products-{now}.docx'

    categories_id = __get_categories_id_from_request(request)
    brands_id = __get_brands_id_from_request(request)

    document = import_export_service.get_products_document(category_id=categories_id, brand_id=brands_id)
    document.save(response)

    return response


def import_xlsx(request):
    if request.method == 'POST' and request.user.is_staff:
        xlsx_file = request.FILES['spreadsheet']
        import_report = import_export_service.import_xlsx_file(xlsx_file)
        sections = section_brand_service.get_sections_with_categories()
        sections_for_tree = section_brand_service.get_sections_with_categories_for_tree()
        brands_for_tree = section_brand_service.get_brands_for_tree()
        return render(request, 'shop/import-xlsx.html', {'sections': sections,
                                                           'sections_for_tree': sections_for_tree,
                                                           'brands_for_tree': brands_for_tree,
                                                           'is_correct_header': import_report['is_correct_header'],
                                                           'errors': import_report['errors'],
                                                           'added': import_report['added'],
                                                           'updated': import_report['updated'],
                                                           'log': '\n'.join(import_report['log']),
                                                           'import_report': import_report})
    else:
        return HttpResponseNotFound()