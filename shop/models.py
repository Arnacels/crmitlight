from django.db import models
from django.contrib.auth.models import User
from hashid_field import HashidAutoField


class Product(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField(max_length=152)
    unit = models.CharField(max_length=10, default='шт.')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    price_sell = models.DecimalField(max_digits=10, decimal_places=2)
    price_buy = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_created=True)

    def __str__(self):
        return str(self.name)


class Order(models.Model):
    STATUSES = ((0, 'Отправлен'), (1, 'В обработке'), (2, 'Выполнено'), (3, 'Оплачен'),)

    id = HashidAutoField(primary_key=True, allow_int=False)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, )
    amount = models.DecimalField(max_digits=16, decimal_places=2)
    pay = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUSES, default=0)

    class Meta:
        ordering = ('-date',)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.status == 0:
            self.product.amount -= 1
            self.product.save()
        super().save(force_insert=False, force_update=False, using=None,
                     update_fields=None)

    def delete(self, using=None, keep_parents=False):
        self.product.amount += 1
        super().delete(using=None, keep_parents=False)


class Discount(models.Model):
    title = models.CharField(max_length=32)
    products = models.ManyToManyField(Product)
    discount = models.DecimalField(max_digits=3, decimal_places=0)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()

    class Meta:
        ordering = ('-date_start',)
