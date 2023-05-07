from django.db import models

# Create your models here.

class zi_document(models.Model):

    zi_document = models.CharField(max_length=45)


class zi_sync_master(models.Model):


    zi_document = models.ForeignKey(zi_document)
    sync_stamp = models.DateTimeField()
    zi_org = models.CharField(max_length=45, unique=True)

