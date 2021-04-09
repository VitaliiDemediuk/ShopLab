import ast
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from ShopLabWork.settings import DOMAIN, MEDIA_URL
from shop.services.shop_services import *

import shop.services.shop_services as shop_services
import shop.services.goods_services as goods_services
import shop.services.section_brand_services as section_brand_services
import shop.services.import_export_services as import_export_services

IMG_LINK_PREFIX = DOMAIN + MEDIA_URL