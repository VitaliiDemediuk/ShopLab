import openpyxl
import docx
from docx.shared import RGBColor
from shop.models import *
from ShopLabWork.settings import MEDIA_ROOT
from django.db.models import Count, Max

import shop.services.shop_service as shop_services
import shop.services.goods_service as goods_services
import shop.services.import_export_service as import_export_services
import shop.services.section_brand_service as section_brand_services