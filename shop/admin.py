from django.contrib import admin
from .models import *

from django.contrib.auth.admin import UserAdmin
from shop.forms.forms import CustomUserCreationForm, CustomUserChangeForm

#Characteristic
@admin.register(Characteristic)
class CharacteristicAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    search_field = ['name']
    save_on_top = True


#Color
@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'hex']
    list_display_links = ['id', 'name']
    search_field = ['name']
    save_on_top = True

#Size
@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    search_field = ['name']
    save_on_top = True

#Brand
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'name_for_link']
    list_display_links = ['id', 'name', 'name_for_link']
    search_field = ['name', 'name_for_link']
    save_on_top = True

#Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id',  'name', 'name_for_link', 'fk_section_id']
    list_display_links = ['id',  'name', 'name_for_link']
    search_field = ['name', 'name_for_link']
    save_on_top = True

#Section
@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'name_for_link']
    list_display_links = ['id', 'name', 'name_for_link']
    search_field = ['name']

#Goods
class SizeForGoodsInline(admin.TabularInline):
    model = SizesGoods
    extra = 0


class PhotoForGoodsInline(admin.TabularInline):
    model = PhotoForGoods
    extra = 0


class CharacteristicsGoodsInline(admin.TabularInline):
    model = CharacteristicsGoods
    extra = 0

@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    list_display = ['id', 'sku', 'title', 'price', 'sale_price', 'in_stock',
                    'is_enable', 'count', 'fk_brand_id', 'fk_category_id']
    list_display_links = ['id', 'title']
    search_field = ['id', 'title']

    inlines = [
        SizeForGoodsInline,
        PhotoForGoodsInline,
        CharacteristicsGoodsInline,
    ]
    save_on_top = True

#Photo for slider
@admin.register(PhotoForSlider)
class PhotoForSliderAdmin(admin.ModelAdmin):
    list_display = ['id', 'file_name']
    list_display_links = ['id', 'file_name']

#Custom user
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('first_name', 'last_name', 'email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')
    ordering = ('first_name', 'last_name', 'email', 'phone_number')