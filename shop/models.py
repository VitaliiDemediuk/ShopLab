from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from decimal import *
from .managers import CustomUserManager


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    name_for_link = models.CharField(max_length=100, unique=True)
    photo = models.ImageField(upload_to="photos_for_brand/%Y/%m/%d/", blank=True)
    about = models.TextField(blank=True)

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"
        ordering = ['id']

    def __str__(self):
        return self.name


class Section(models.Model):
    name = models.CharField(max_length=100, unique=True)
    name_for_link = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Section"
        verbose_name_plural = "Sections"
        ordering = ['id']

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    name_for_link = models.CharField(max_length=100)
    fk_section_id = models.ForeignKey('Section', on_delete=models.CASCADE, verbose_name="Section")
    about = models.TextField(blank=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['id']
        unique_together = (('name', 'name_for_link', 'fk_section_id'),)

    def __str__(self):
        return self.fk_section_id.name + ' / ' + self.name


class Goods(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=256)
    price = models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(Decimal('0.00'))])
    sale_price = models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(Decimal('0.00'))],
                                     blank=True, default=Decimal('0.00'))
    main_photo = models.ImageField(upload_to="main_photos_for_goods/%Y/%m/%d/", blank=True)
    in_stock = models.BooleanField(default=True)
    is_enable = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    count = models.IntegerField(validators=[MinValueValidator(0)])
    add_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
    fk_brand_id = models.ForeignKey('Brand', verbose_name='Brand', on_delete=models.CASCADE)
    fk_category_id = models.ForeignKey('Category', verbose_name='Category', on_delete=models.CASCADE)
    fk_color_id = models.ForeignKey("Color", verbose_name='Color', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Goods"
        verbose_name_plural = "Goods"
        ordering = ['add_date']


class PhotoForGoods(models.Model):
    file_name = models.ImageField(upload_to="photos_for_goods/%Y/%m/%d/")
    fk_goods_id = models.ForeignKey('Goods', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "PHOTO FOR GOODS"
        verbose_name_plural = "PHOTOS FOR GOODS"
        ordering = ['id']


class Color(models.Model):
    name = models.CharField(max_length=50, unique=True)
    hex = models.CharField(max_length=7)

    class Meta:
        verbose_name = "Color"
        verbose_name_plural = "Colors"
        ordering = ['name']

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=10, unique=True)
    fk_goods_id = models.ManyToManyField('Goods', through='SizesGoods')

    class Meta:
        verbose_name = "Size"
        verbose_name_plural = "Sizes"
        ordering = ['name']

    def __str__(self):
        return self.name


class SizesGoods(models.Model):
    fk_size_id = models.ForeignKey('Size', on_delete=models.CASCADE)
    fk_goods_id = models.ForeignKey('Goods', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Goods size"
        verbose_name_plural = "Goods sizes"


class Characteristic(models.Model):
    name = models.CharField(max_length=100, unique=True)
    fk_goods_id = models.ManyToManyField('Goods', through='CharacteristicsGoods')

    class Meta:
        verbose_name = "Characteristic"
        verbose_name_plural = "Characteristics"
        ordering = ['name']

    def __str__(self):
        return self.name


class CharacteristicsGoods(models.Model):
    fk_characteristic_id = models.ForeignKey('Characteristic', on_delete=models.CASCADE)
    fk_goods_id = models.ForeignKey('Goods', on_delete=models.CASCADE)
    value = models.CharField(max_length=100)

    class Meta:
        verbose_name = "GOODS Characteristic"
        verbose_name_plural = "GOODS Characteristics"
        unique_together = (('fk_characteristic_id', 'fk_goods_id'),)


class TypesOfPayment(models.Model):
    name = models.CharField(max_length=100)


class TypesOfDelivery(models.Model):
    name = models.CharField(max_length=100)


class CustomUser(AbstractUser):
    username = None
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField('email address', unique=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)  # validators should be a list
    is_verified = models.BooleanField(default=False)
    goods_for_basket = models.ManyToManyField('Goods', through='Basket', related_name='goods_for_basket')
    goods_for_review = models.ManyToManyField('Goods', through='Review', related_name='goods_for_review')
    reset_password_token = models.CharField(max_length=39, default="")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Check(models.Model):
    purchase_date = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=100)
    fk_buyers_id = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    fk_types_of_payment_id = models.ForeignKey('TypesOfPayment', on_delete=models.CASCADE)
    fk_types_of_delivery_id = models.ForeignKey('TypesOfDelivery', on_delete=models.CASCADE)
    goods = models.ManyToManyField('Goods', through='Purchase')


class Purchase(models.Model):
    fk_goods_id = models.ForeignKey('Goods', on_delete=models.CASCADE)
    fk_check_id = models.ForeignKey('Check', on_delete=models.CASCADE)
    count = models.IntegerField(validators=[MinValueValidator(0)])


class Basket(models.Model):
    fk_goods_id = models.ForeignKey('Goods', on_delete=models.CASCADE)
    fk_buyer_id = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    count = models.IntegerField(validators=[MinValueValidator(0)])
    date = models.DateTimeField(auto_now_add=True)
    fk_size_id = models.ForeignKey('Size', on_delete=models.CASCADE)


class Review(models.Model):
    fk_goods_id = models.ForeignKey('Goods', on_delete=models.CASCADE)
    fk_buyer_id = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    tittle = models.CharField(max_length=256)
    review_text = models.TextField()
    add_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)


class PhotoForReview(models.Model):
    file_name = models.ImageField(upload_to="photos_for_review/%Y/%m/%d/")
    fk_goods_id = models.ForeignKey('Review', on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']


class PhotoForSlider(models.Model):
    file_name = models.ImageField(upload_to="photos_for_slider/%Y/%m/%d/")

    class Meta:
        verbose_name = "Photo for slider"
        verbose_name_plural = "Photos for slider"
        ordering = ['id']

    def __str__(self):
        return self.file_name.url