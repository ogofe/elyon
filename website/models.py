from django.db import models

# Create your models here.
class Message(models.Model):
    sender = models.CharField(max_length=200, blank=False) #full name
    date_created = models.DateTimeField(auto_now=True)
    message = models.TextField()
    email = models.EmailField()

    def __str__(self) -> str:
        return self.sender    

    @property
    def full_name(self) -> str:
        return self.sender


class Visitor(models.Model):pass
# updates 