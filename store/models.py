from collections.abc import Iterable
from django.db import models
from core.models import DbModel
from django.contrib.auth.models import User
import os
# from django.contrib.sessions.models import 



def make_invoice_id(lim=5):
    char = os.urandom(5).hex()
    return char

ORDER_STATUSES = (
    ('pending', 'Pending'),
    ('confirmed', 'Confirmed'),
    ('on-route', 'On Route'),
    ('fulfilled', 'Fulfilled'),
)

#  Store models

class Product(DbModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price_per_piece = models.DecimalField(max_digits=1000, decimal_places=2)
    price_per_bundle = models.DecimalField(max_digits=1000, decimal_places=2, blank=True, null=True)
    receivable = models.ForeignKey("core.Receivable", on_delete=models.CASCADE, related_name='parent')
    images = models.ManyToManyField("core.File", blank=True)
    category = models.ForeignKey("Category", on_delete=models.CASCADE, blank=True, null=True)
    tags = models.ManyToManyField("Tag",  blank=True, related_name='tags')

    def stock_quantity(self):
        return self.receivable.stock_quantity
    
    def save(self, *args, **kwargs):
        self.slug=self.name.lower().replace(" ", '-').replace("'", '')
        super().save(*args, **kwargs)
    
    @property
    def image(self):
        return self.images.first()
    
    def __str__(self) -> str:
        return self.name
    

class ShoppingCart(models.Model):
    owner = models.ForeignKey('Customer', on_delete=models.CASCADE)
    items = models.ManyToManyField("OrderItem", blank=True)

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile', blank=True, null=True)
    session_id = models.CharField(max_length=200, blank=True, null=True, unique=True)
    full_name = models.CharField(max_length=400, blank=True, null=True)
    address = models.CharField(max_length=400, blank=True, null=True)
    phone_number = models.CharField(max_length=400, blank=True, null=True)
    cart = models.OneToOneField(ShoppingCart, on_delete=models.CASCADE, blank=True, null=True)
    orders = models.ManyToManyField("CustomerOrder", blank=True)

    def __str__(self):
        if self.user:
            return f'{self.user.get_full_name()}'

        return f'Customer {self.id}'
    


class CustomerOrder(DbModel):

    invoice_id = models.CharField(unique=True, max_length=10, default=make_invoice_id)
    invoiced_to = models.ForeignKey("Customer", on_delete=models.CASCADE)
    cancelled = models.BooleanField(default=False)
    delivery_status = models.BooleanField(default=False)
    status = models.CharField(max_length=30, default='pending', choices=ORDER_STATUSES)
    payment_status = models.BooleanField(default=False)
    order_items = models.ManyToManyField("OrderItem", related_name='items', blank=True)
    include_taxes = models.BooleanField(default=True)
    vat = models.DecimalField(max_digits=4, decimal_places=2, default=7.50, blank=True, null=True)
    
    @property
    def total(self):
        return self.subtotal
    
    @property
    def subtotal(self):
        from core.models import OrderUnit
        amt = 0
        for item in self.order_items.all():
            if item.quantity_type == 'pieces':
                amt += (item.product.price_per_piece * item.quantity)
            elif item.quantity_type == 'bundle':
                amt += (item.product.price_per_bundle * item.quantity)
        if self.include_taxes:
            amt += self.vat
        return amt

    def __str__(self):
        return self.invoice_id


class OrderItem(DbModel):
    ORDER_ITEM_TYPE = (
        ('pieces', 'Pieces'),
        ('bundle', 'Bundle'),
    )

    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    quantity_type = models.CharField(max_length=20, choices=ORDER_ITEM_TYPE, default='pieces')

    def __str__(self):
        return self.product.name
    
    def subtotal(self):
        amt = 0
        amt += (
            (self.product.price_per_piece if self.quantity_type == 'pieces' else self.product.price_per_bundle)
            * self.quantity
        )
        return amt

class Tag(DbModel):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name

class Category(DbModel):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name


