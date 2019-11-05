from django.db import models
from gdstorage.storage import GoogleDriveStorage
import httplib2shim


httplib2shim.patch()


gd_storage = GoogleDriveStorage()


class Client(models.Model):

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    telephone = models.CharField(max_length=20)
    active = models.BooleanField(default=False)
    photo = models.FileField(blank=True, upload_to='image', storage=gd_storage)

    def __str__(self):
        return self.last_name


class Visit(models.Model):
    client = models.ForeignKey(Client, related_name='visit', on_delete=models.CASCADE)
    date_visit = models.DateField(blank=True)
    manicure = models.BooleanField(default=False)
    pedicure = models.BooleanField(default=False)
    manicure_correction = models.BooleanField(default=False)
    pedicure_correction = models.BooleanField(default=False)
    pay = models.DecimalField(decimal_places=2, max_digits=6, default=0)


class ImageUrls(models.Model):
    visit = models.ForeignKey(Visit, related_name='image', on_delete=models.CASCADE, blank=True)
    client = models.ForeignKey(Client, related_name='image', on_delete=models.CASCADE, blank=True)
    main_image = models.FileField(blank=True, upload_to='image', storage=gd_storage)
