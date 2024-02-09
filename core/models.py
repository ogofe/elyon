from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, User
import os


def make_invoice_id(lim=5):
    char = os.urandom(5).hex()
    # char = hash(os.urandom(5).hex())
    return char

# Create your models here.
class DbModel(models.Model):
    date_created = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True



class Message(DbModel):
    sender_name = models.CharField(max_length=200)
    sender_email = models.EmailField()
    message_subject = models.CharField(max_length=200)
    message_body = models.TextField()
    read_status = models.BooleanField(default=False)

    def __str__(self):
        return self.message_subject


class Notification(DbModel):
    icon = models.CharField(max_length=50, default="bi bi-info-circle")
    title = models.CharField(max_length=100)
    body = models.TextField()
    object_link = models.URLField(blank=True, null=True)
    read_status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title


class Customer(DbModel):
    full_name = models.CharField(max_length=400)
    address = models.CharField(max_length=400)
    phone_number = models.CharField(max_length=400)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.full_name


FILE_TYPES = (
    ('image', 'Image File'),
    ('video', 'Video File'),
    ('doc', 'Document File'),
    ('other', 'Other File Type'),
)

ORDER_STATUSES = (
    ('pending', 'Pending'),
    # ('pending', 'Pending'),
    # ('pending', 'Pending'),
    # ('pending', 'Pending'),
    # ('pending', 'Pending'),
)

class File(DbModel):
    name = models.CharField(max_length=200, blank=True, null=True)
    file = models.ImageField(upload_to='images/')
    file_type = models.CharField(max_length=20, default='image', choices=FILE_TYPES)


class Receivable(DbModel):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    unit = models.CharField(max_length=100)
    images = models.ManyToManyField("File", blank=True, limit_choices_to={'file_type': 'image' })

    def __str__(self):
        return self.name


# Base product model
class Product(DbModel):
    reiceivable = models.ForeignKey("Receivable", on_delete=models.CASCADE, related_name='parent')
    price = models.DecimalField(max_digits=1000, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def name(self):
        return self.reiceivable.name

    @property
    def stock_quantity(self):
        return self.reiceivable.stock_quantity    

    @property
    def unit(self):
        return self.reiceivable.unit

    @property
    def images(self):
        return self.reiceivable.images

    


class DeliveryItem(DbModel):
    receivable = models.ForeignKey("Receivable", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit = models.CharField(max_length=200)



class Delivery(DbModel):
    date_recorded = models.DateTimeField(auto_now=True)
    arrival_date = models.DateTimeField(blank=True, null=True)
    date_recorded = models.DateTimeField(auto_now=True)
    items = models.ManyToManyField(DeliveryItem, blank=True)


class CustomerOrder(DbModel):
    invoice_id = models.ForeignKey("Invoice", on_delete=models.CASCADE)
    status = models.CharField(max_length=30, default='pending', choices=ORDER_STATUSES)
    cancelled = models.BooleanField(default=False)
    delivery_status = models.BooleanField(default=False)



class OrderItem(DbModel):
    invoice_id = models.ForeignKey("Invoice", on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.product.name



class Invoice(DbModel):
    invoice_id = models.CharField(unique=True, max_length=10, default=make_invoice_id)
    invoiced_to = models.ForeignKey("Customer", on_delete=models.CASCADE)
    payment_status = models.BooleanField(default=False)
    order_items = models.ManyToManyField("OrderItem", related_name='items', blank=True)
    include_taxes = models.BooleanField(default=True)
    vat = models.DecimalField(max_digits=4, decimal_places=2, default=7.50, blank=True, null=True)
    
    def subtotal(self):
        amt = 0
        for item in self.order_items.all():
            amt += (item.product.price * item.quantity)
        if self.include_taxes:
            amt += self.vat
        return amt

    def __str__(self):
        return self.invoice_id


# Site
class CatalogImage(DbModel):
    catalog = models.ForeignKey("CatalogItem", on_delete=models.CASCADE, )
    image = models.ImageField(upload_to='catalog/')

    def __str__(self) -> str:
        return f'{self.catalog.name} image {self.id}'

class CatalogItem(DbModel):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    site_preview = models.BooleanField(default=True)
    images = models.ManyToManyField("CatalogImage", blank=True)

    def __str__(self) -> str:
        return f'{self.name}'
    
    @property
    def slug(self):
        return self.name.lower().replace(' ', '-').replace('.', '').replace("'", '')


# class StaffAccount(DbModel):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.user.first_name



# class Permission(DbModel):pass


