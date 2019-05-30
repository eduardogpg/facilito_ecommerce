from django.db import models
from django.utils.text import slugify

from products.models import Product

class Tag(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)

        super(Tag, self).save(*args, **kwargs)
