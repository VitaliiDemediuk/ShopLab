from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class City(models.Model):
    name = models.CharField(max_length=100)


class Brand(models.Model):
    name = models.CharField(max_length=100)
    name_for_link = models.CharField(max_length=100)
    about = models.TextField()
    fk_country_id = models.ForeignKey('City', on_delete=models.CASCADE)


class Category(models.Model):
    name = models.CharField(max_length=100)
    name_for_link = models.CharField(max_length=100)
    parent_category_id = models.IntegerField()
    about = models.TextField()


class Characteristic(models.Model):
    name = models.CharField(max_length=100)
    brands = models.ManyToManyField('Goods', through='CharacteristicsGoods')


class Goods(models.Model):
    tittle = models.CharField(max_length=256)
    price = models.IntegerField(validators=[MinValueValidator(0)])
    sale_price = models.IntegerField(validators=[MinValueValidator(0)])
    is_sale = models.BooleanField(default=False)
    in_stock = models.BooleanField(default=True)
    is_enable = models.BooleanField(default=True)
    description = models.TextField()
    count = models.IntegerField(validators=[MinValueValidator(0)])
    add_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
    fk_brand_id = models.ForeignKey('Brand', on_delete=models.CASCADE)
    fk_category_id = models.ForeignKey('Category', on_delete=models.CASCADE)


class PhotoForGoods(models.Model):
    file_name = models.ImageField(upload_to="photos_for_goods/%Y/%m/%d/")
    fk_goods_id = models.ForeignKey('Goods', on_delete=models.CASCADE)
    numbers = models.IntegerField(validators=[MinValueValidator(0)])


class CharacteristicsGoods(models.Model):
    fk_characteristic_id = models.ForeignKey('Characteristic', on_delete=models.CASCADE)
    fk_goods_id = models.ForeignKey('Goods', on_delete=models.CASCADE)
    value = models.CharField(max_length=100)


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
    ddd_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)


class PhotoForReview(models.Model):
    file_name = models.ImageField(upload_to="photos_for_review/%Y/%m/%d/")
    fk_goods_id = models.ForeignKey('Review', on_delete=models.CASCADE)
    numbers = models.IntegerField(validators=[MinValueValidator(0)])