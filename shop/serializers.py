from decimal import Decimal
from django.utils import timezone
from rest_framework import serializers
from hashid_field.rest import HashidSerializerCharField
from .models import (Product, Order, Discount)


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ('title', 'discount',)


class ProductSerializer(serializers.ModelSerializer):
    discount = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('name', 'description', 'unit', 'amount', 'price_sell', 'price_buy', 'discount',)

    def get_discount(self, obj):
        now = timezone.now()
        discount = Discount.objects.filter(products=obj, date_start__lt=now, date_end__gt=now)
        if discount.exists():
            data = DiscountSerializer(discount.first())
            return data.data
        return None


class OrderSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        pk_field=HashidSerializerCharField(
            source_field='shop.Order.id'), read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


class CreateOrderSerializer(OrderSerializer):
    class Meta:
        model = Order
        fields = ('id', 'buyer', 'product',)

    def create(self, validated_data):
        now = timezone.now()
        product = validated_data.get('product')
        discounts = Discount.objects.filter(products=product, date_start__lt=now, date_end__gt=now)
        amount = product.price_sell

        discount = Decimal(0)
        if discounts.exists():
            for dis in discounts:
                discount += dis.discount
        if discount > 0:
            discount += self.discount_for_oldest(product)
            amount = amount - (product.price_sell * discount) / 100

        order = Order(product=product, amount=amount)
        if validated_data.get('buyer'):
            order.buyer = validated_data.get('buyer')
        order.save()
        return order

    @staticmethod
    def discount_for_oldest(product):
        if product.date < (timezone.now() - timezone.timedelta(days=30)):
            return 20
        return 0


class PartialOrderUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('status',)
