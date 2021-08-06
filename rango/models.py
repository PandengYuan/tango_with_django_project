from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class Category(models.Model):
    NAME_MAX_LENGTH = 128
    CHAR_MAX_LENGTH = 128
    id = models.CharField(max_length=CHAR_MAX_LENGTH, primary_key=True)
    name = models.CharField(max_length=CHAR_MAX_LENGTH, unique=True)
    slug = models.SlugField(unique=True)
    sales = models.IntegerField(default=0)
    picture = models.ImageField(upload_to='product_images', blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Product(models.Model):
    CHAR_MAX_LENGTH = 128
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    id = models.CharField(max_length=CHAR_MAX_LENGTH, primary_key=True)
    name = models.CharField(max_length=CHAR_MAX_LENGTH, unique=True)
    description = models.FileField(upload_to='product_description', blank=True)
    price = models.FloatField(default=0)
    sales = models.IntegerField(default=0)
    slug = models.SlugField(blank=True)
    picture = models.ImageField(upload_to='product_images', blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


        
class Cart(models.Model):
    CHAR_MAX_LENGTH = 128
    buyer_name = models.CharField(max_length=CHAR_MAX_LENGTH, default='')
    product_name = models.CharField(max_length=CHAR_MAX_LENGTH, default='')

    def __str__(self):
        return self.buyer_name + self.product_name


class Review(models.Model):
    DESCRIPTION_MAX_LENGTH = 1000
    CHAR_MAX_LENGTH = 128
    buyer_name = models.CharField(max_length=CHAR_MAX_LENGTH, default='')
    product_name = models.CharField(max_length=CHAR_MAX_LENGTH, default='')
    content = models.TextField(default='')

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    CHAR_MAX_LENGTH = 128
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # The additional attributes we wish to include.
    address = models.CharField(max_length=CHAR_MAX_LENGTH, default='', blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    usertype = models.CharField(max_length=CHAR_MAX_LENGTH, default='')

    def __str__(self):
        return self.user.username


