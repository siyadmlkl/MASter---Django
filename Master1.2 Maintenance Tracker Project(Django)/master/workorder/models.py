from django.db import models


class WorkOrder(models.Model):
    area = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    asset = models.CharField(max_length=100, default='unit')
    createdTime = models.DateTimeField(null="True", blank="True")
    createdBy = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    status = models.CharField(max_length=25)
    action = models.CharField(max_length=255)
    closedTime = models.DateTimeField(null="True", blank="True")
    image_file = models.FileField(
        null='True', blank='True', upload_to="")


class Assets(models.Model):
    area = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    asset = models.CharField(max_length=100)


class WoEvents(models.Model):
    wonumber = models.ForeignKey(WorkOrder, on_delete=models.CASCADE)
    editedBy = models.CharField(max_length=100)
    editedTime = models.DateTimeField()
    event = models.CharField(max_length=250, default='')
