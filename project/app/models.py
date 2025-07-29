from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField(help_text="Price in cents") 
    currency = models.CharField(max_length=3, default='usd')

    def __str__(self):
        return self.name
