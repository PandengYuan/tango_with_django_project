from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class Category(models.Model):
    NAME_MAX_LENGTH = 128
    CHAR_MAX_LENGTH = 128
    # id = models.CharField(max_length=CHAR_MAX_LENGTH, primary_key=True)
    name = models.CharField(max_length=CHAR_MAX_LENGTH, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)
    # img = models.ImageField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Product(models.Model):
    CHAR_MAX_LENGTH = 128
    DESCRIPTION_MAX_LENGTH = 1000
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    id = models.CharField(max_length=CHAR_MAX_LENGTH, primary_key=True)
    name = models.CharField(max_length=CHAR_MAX_LENGTH, unique=True)
    description = models.CharField(max_length=DESCRIPTION_MAX_LENGTH)
    price = models.IntegerField(default=0)
    sales = models.IntegerField(default=0)
    picture = models.ImageField(upload_to='product_images', blank=True)

    def __str__(self):
        return self.name

class Collection(models.Model):
    buyerid = models.ForeignKey(Category, on_delete=models.CASCADE)
    productid = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

        
class Cart(models.Model):
    buyerid = models.ForeignKey(Category, on_delete=models.CASCADE)
    productid = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Review(models.Model):
    DESCRIPTION_MAX_LENGTH = 1000
    buyerid = models.ForeignKey(Category, on_delete=models.CASCADE)
    productid = models.ForeignKey(Product, on_delete=models.CASCADE)
    content = models.CharField(max_length=DESCRIPTION_MAX_LENGTH)

    def __str__(self):
        return self.name


class Order(models.Model):
    CHAR_MAX_LENGTH = 128
    buyerid = models.ForeignKey(Category, on_delete=models.CASCADE)
    productid = models.ForeignKey(Product, on_delete=models.CASCADE)
    orderid = models.CharField(max_length=CHAR_MAX_LENGTH, primary_key=True)

    def __str__(self):
        return self.name

class UploadProduct(models.Model):
    selleriid = models.ForeignKey(Category, on_delete=models.CASCADE)
    productid = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Page(models.Model):
    TITLE_MAX_LENGTH = 128
    URL_MAX_LENGTH = 200
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title


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


