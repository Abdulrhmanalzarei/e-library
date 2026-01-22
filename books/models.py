from django.db import models
from django.utils.text import slugify

class Author(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField(Author, related_name="books")
    categories = models.ManyToManyField(Category, related_name="books", blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    isbn = models.CharField(max_length=20, blank=True, null=True)
    cover = models.ImageField(upload_to="books/covers/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)[:50]
            slug = base
            count = 1
            while Book.objects.filter(slug=slug).exists():
                slug = f"{base}-{count}"
                count += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
