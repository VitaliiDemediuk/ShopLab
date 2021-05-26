import ast
from datetime import datetime
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from ShopLabWork.settings import DOMAIN, MEDIA_URL
from shop.services.shop_services import *

import shop.services.shop_services as shop_service
import shop.services.goods_service as goods_service
import shop.services.section_brand_service as section_brand_service
import shop.services.import_export_service as import_export_service
import shop.services.account_services as account_services

IMG_LINK_PREFIX = DOMAIN + MEDIA_URL