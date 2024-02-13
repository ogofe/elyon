from collections.abc import Iterable
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, User
import os


def make_random_char(lim=5):
    char = os.urandom(5).hex()
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


FILE_TYPES = (
    ('image', 'Image File'),
    ('video', 'Video File'),
    ('doc', 'Document File'),
    ('other', 'Other File Type'),
)

class File(DbModel):
    name = models.CharField(max_length=200, blank=True, null=True)
    file = models.ImageField(upload_to='images/')
    file_type = models.CharField(max_length=20, default='image', choices=FILE_TYPES)


class OrderUnit(DbModel):
    # An order unit is a representation of how many pieces
    # make up the whole of a unit
    # e.g Score = 20 pieces, Dozen = 12 pieces, Gross = 120 pieces
    # so if a shipment is received for 15 scores of camouflage
    # then the recievable's stock_quantity += (15 * 20) ie 300 
    name = models.CharField(max_length=200)
    quantity_per_bundle = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return self.name
    

class Receivable(DbModel):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    stock_quantity = models.PositiveIntegerField(default=0) # in pieces
    images = models.ManyToManyField("File", blank=True, limit_choices_to={'file_type': 'image' })

    def __str__(self):
        return self.name
    
    @property
    def slug(self):
        slug = self.name.lower().replace(' ', '-').replace("'", '').replace('/', '')
        return slug


class ShipmentItem(DbModel):
    receivable = models.ForeignKey("Receivable", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit = models.ForeignKey('OrderUnit', on_delete=models.CASCADE)

    def __str__(self):
        return self.receivable.name


class ShipmentDelivery(DbModel):
    shipment_id = models.CharField(max_length=20, default=make_random_char)
    date_recorded = models.DateTimeField(auto_now=True)
    arrival_date = models.DateTimeField(blank=True, null=True)
    date_recorded = models.DateTimeField(auto_now=True)
    items = models.ManyToManyField(ShipmentItem, blank=True)
    saved = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.saved:
            for item in self.items.all():
                item.receivable.stock_quantity += int(
                    int(item.quantity) * int(item.unit.quantity_per_bundle)
                )
                item.receivable.save()
            self.saved = True
        super().save(*args, **kwargs)
            


class StaffAccount(User, DbModel):
    is_staff = True

    def __str__(self):
        return self.first_name





class SiteSettings(models.Model):
    catalog_items = models.ManyToManyField(Receivable, blank=True)

    def save(self, *args, **kwargs):
        if self.id == 1:
            return super().save(*args, **kwargs)
        else:
            return

SiteSettings().save()







