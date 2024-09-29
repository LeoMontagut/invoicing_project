from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from uuid import uuid4
from django.contrib.auth.models import User


class Client(models.Model):

    PROVINCES = [
        ('Cordoba', 'Cordoba'),
        ('Buenos Aires', 'Buenos Aires'),
        ('La Pampa', 'La Pampa')
    ]

    # Basic fields
    client_name = models.CharField(null=True, blank=True, max_length=200)
    client_address = models.CharField(null=True, blank=True, max_length=200)
    client_province = models.CharField(choices=PROVINCES, blank=True, max_length=20)
    client_phone = models.CharField(null=True, blank=True, max_length=15)

    # Utility fields
    unique_id = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(null=True, blank=True, unique=True, max_length=500)
    date_created = models.DateTimeField(null=True, blank=True)
    last_updated = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.client_name}, {self.unique_id}'

    def get_absolute_url(self):
        return reverse('client-detail', kwargs={
            'slug': self.slug
        })

    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.unique_id is None:
            self.unique_id = str(uuid4()).split('-')[4]
            self.slug = slugify(f'{self.client_name}, {self.unique_id}')

        self.slug = slugify(f'{self.client_name}, {self.unique_id}')
        self.last_updated = timezone.localtime(timezone.now())

        super(Client, self).save(*args, **kwargs)
