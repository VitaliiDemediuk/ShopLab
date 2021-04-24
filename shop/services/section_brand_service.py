from shop.services.all_moduls_for_service import *


def get_sections_with_categories():
    sections = list(Section.objects.all().values('id', 'name', 'name_for_link'))
    for section in sections:
        section['category'] = list(Category.objects.filter(fk_section_id=section['id']).values('name', 'name_for_link'))
    return sections


def get_sections_with_categories_for_tree():
    sections = list(Section.objects.extra(select={'text': 'name'}).values('id', 'text'))
    for section in sections:
        section['children'] = list(Category.objects.filter(fk_section_id=section['id'])
                                           .extra(select={'text': 'name'}).values('id', 'text'))
        section['id'] = 'section-' + str(section['id'])
    return sections


def get_brands():
    brands = list(Brand.objects.all().values('name', 'name_for_link', 'photo'))
    return brands

def get_brands_for_tree():
    brands = list(Brand.objects.all().extra(select={'text': 'name'}).values('id', 'text'))
    return brands