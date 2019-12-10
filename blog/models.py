from django.db import models
from unidecode import unidecode
from django.template.defaultfilters import slugify
# from django.utils.text import slugify
from django.urls import reverse

class Source(models.Model):
    name = models.CharField(max_length=100, unique=True)
    link = models.CharField(max_length=100, blank=True)
    # slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name



class Post(models.Model):
    title = models.CharField(max_length = 200)
    post_link = models.CharField(max_length = 200, blank=True)
    slug = models.SlugField(null=False, unique=True, max_length=50)
    short_description = models.TextField()
    description = models.TextField()
    photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_4 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_5 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_6 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_7 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_8 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_9 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_10 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    source = models.ForeignKey(Source, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(unidecode(self.title))[:50]
        return super().save(*args, **kwargs)
