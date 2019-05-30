from django.db import models
from django.utils.text import slugify

class ProductQuerySet(models.QuerySet):
    def last(self):
        return self.order_by('-created_at')

    def active(self):
        return self.filter(active=True)
    
class Product(models.Model):
    title = models.CharField(null=False, blank=False, max_length=120)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=20, default=0.00)
    slug = models.SlugField(null=False, blank=False, unique=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    active = models.BooleanField(null=False, blank=False, default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = ProductQuerySet.as_manager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)

        super(Product, self).save(*args, **kwargs)
