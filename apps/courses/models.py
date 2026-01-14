from django.db import models
from django.utils.text import slugify
from apps.accounts.models import User


class Course(models.Model):
    LEVEL_CHOICES = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    category = models.CharField(
        max_length=100,
        default="Programming"
    )
    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES,
        default="beginner"
    )
    price = models.DecimalField(max_digits=8, decimal_places=2)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Auto-generate a unique slug from title when missing
        if not self.slug and self.title:
            base = slugify(self.title)[:200]
            slug = base
            counter = 1
            while Course.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
