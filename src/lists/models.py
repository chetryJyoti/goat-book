from django.db import models
from django.urls import reverse
from django.conf import settings

class List(models.Model):
    @property
    def name(self):
        return self.item_set.first().text
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="lists",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    
    shared_with = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='shared_lists',
        blank=True
    )

    def get_absolute_url(self):
        return reverse("view_list", args=[self.id])

class Item(models.Model):
    text = models.TextField(default="")
    list = models.ForeignKey(List,default="",on_delete=models.CASCADE)
    
    class Meta:
        ordering = ("id",)
        unique_together = ("list","text")
        
    def __str__(self):
        return self.text