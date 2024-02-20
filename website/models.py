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



class SiteVisit(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    url = models.URLField(blank=True, null=True)


class Visitor(models.Model):
    cookie_id = models.CharField(max_length=200)
    date_visited = models.DateField(auto_now=True, auto_now_add=False)
    metainfo = models.TextField(blank=True, null=True)
    visits = models.ManyToManyField("SiteVisit", blank=True)



class CarouselItem(models.Model):
    image = models.ForeignKey("core.File", on_delete=models.SET_NULL, blank=True, null=True)
    background_color = models.CharField(max_length=200, blank=True, null=True)
    name = models.CharField(max_length=200)
    display_title = models.CharField(max_length=200, blank=True, null=True)
    cta = models.CharField(max_length=200, blank=True, null=True)
    display_content = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name


