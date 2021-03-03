from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Brand(models.Model):
    name = models.CharField(max_length=100)
    name_for_link = models.CharField(max_length=100, unique=True)
    photo = models.ImageField(upload_to="photos_for_brand/%Y/%m/%d/")
    about = models.TextField()

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"
        ordering = ['id']

    def __str__(self):
        return self.name


class Section(models.Model):
    name = models.CharField(max_length=100)

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
        unique_together = (('name_for_link', 'fk_section_id'),)

    def __str__(self):
        return self.fk_section_id.name + ' / ' + self.name


class Goods(models.Model):
    tittle = models.CharField(max_length=256)
    price = models.IntegerField(validators=[MinValueValidator(0)])
    sale_price = models.IntegerField(validators=[MinValueValidator(0)])
    main_photo = models.ImageField(upload_to="main_photos_for_goods/%Y/%m/%d/")
    is_sale = models.BooleanField(default=False)
    in_stock = models.BooleanField(default=True)
    is_enable = models.BooleanField(default=True)
    description = models.TextField()
    count = models.IntegerField(validators=[MinValueValidator(0)])
    add_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
    fk_brand_id = models.ForeignKey('Brand', verbose_name='Brand', on_delete=models.CASCADE)
    fk_category_id = models.ForeignKey('Category', verbose_name='Category', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Goods"
        verbose_name_plural = "Goods"
        ordering = ['add_date']


class PhotoForGoods(models.Model):
    file_name = models.ImageField(upload_to="photos_for_goods/%Y/%m/%d/")
    fk_goods_id = models.ForeignKey('Goods', on_delete=models.CASCADE)
    numbers = models.IntegerField(validators=[MinValueValidator(0)])


class Color(models.Model):
    name = models.CharField(max_length=50)
    hex = models.CharField(max_length=7)
    fk_goods_id = models.ManyToManyField('Goods', through='ColorsGoods')

    class Meta:
        verbose_name = "Color"
        verbose_name_plural = "Colors"
        ordering = ['name']

    def __str__(self):
        return name


class ColorsGoods(models.Model):
    fk_color_id = models.ForeignKey('Color', on_delete=models.CASCADE)
    fk_goods_id = models.ForeignKey('Goods', on_delete=models.CASCADE)


class Size(models.Model):
    name = models.CharField(max_length=10)
    fk_goods_id = models.ManyToManyField('Goods', through='SizesGoods')

    class Meta:
        verbose_name = "Size"
        verbose_name_plural = "Sizes"
        ordering = ['name']

    def __str__(self):
        return name


class SizesGoods(models.Model):
    fk_size_id = models.ForeignKey('Size', on_delete=models.CASCADE)
    fk_goods_id = models.ForeignKey('Goods', on_delete=models.CASCADE)


class Characteristic(models.Model):
    name = models.CharField(max_length=100)
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
        unique_together = (('fk_characteristic_id', 'fk_goods_id'),)


class LoyaltyCardType(models.Model):
    name = models.CharField(max_length=100)
    sale = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])


class LoyaltyCard(models.Model):
    bonus_account = models.IntegerField(validators=[MinValueValidator(0)])
    fk_loyalty_card_type = models.ForeignKey('LoyaltyCardType', on_delete=models.CASCADE)


class TypesOfPayment(models.Model):
    name = models.CharField(max_length=100)


class TypesOfDelivery(models.Model):
    name = models.CharField(max_length=100)


class Buyer(models.Model):
    second_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password_hash = models.CharField(max_length=256)
    tel_number = models.CharField(max_length=13)
    fk_loyalty_card_id = models.ForeignKey('LoyaltyCard', on_delete=models.CASCADE)
    goods_for_basket = models.ManyToManyField('Goods', through='Basket', related_name='goods_for_basket')
    goods_for_review = models.ManyToManyField('Goods', through='Review', related_name='goods_for_review')


class Check(models.Model):
    purchase_date = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=100)
    fk_buyers_id = models.ForeignKey('Buyer', on_delete=models.CASCADE)
    fk_types_of_payment_id = models.ForeignKey('TypesOfPayment', on_delete=models.CASCADE)
    fk_types_of_delivery_id = models.ForeignKey('TypesOfDelivery', on_delete=models.CASCADE)
    goods = models.ManyToManyField('Goods', through='Purchase')


class Purchase(models.Model):
    fk_goods_id = models.ForeignKey('Goods', on_delete=models.CASCADE)
    fk_check_id = models.ForeignKey('Check', on_delete=models.CASCADE)
    count = models.IntegerField(validators=[MinValueValidator(0)])


class Basket(models.Model):
    fk_goods_id = models.ForeignKey('Goods', on_delete=models.CASCADE)
    fk_buyer_id = models.ForeignKey('Buyer', on_delete=models.CASCADE)
    count = models.IntegerField(validators=[MinValueValidator(0)])
    date = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    fk_goods_id = models.ForeignKey('Goods', on_delete=models.CASCADE)
    fk_buyer_id = models.ForeignKey('Buyer', on_delete=models.CASCADE)
    tittle = models.CharField(max_length=256)
    review_text = models.TextField()
    add_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)


class PhotoForReview(models.Model):
    file_name = models.ImageField(upload_to="photos_for_review/%Y/%m/%d/")
    fk_goods_id = models.ForeignKey('Review', on_delete=models.CASCADE)
    numbers = models.IntegerField(validators=[MinValueValidator(0)])