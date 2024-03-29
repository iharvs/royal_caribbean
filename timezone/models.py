from django.db import models

class TZDBTimezone(models.Model):
    CountryCode = models.CharField(max_length=10)
    CountryName = models.CharField(max_length=100)
    ZoneName = models.CharField(max_length=100, primary_key=True)
    GMTOffset = models.IntegerField(null=True)
    ImportDate = models.DateField(null=True)
    def __str__(self):
        return self.ZoneName

class TZDBZoneDetail(models.Model):
    CountryName = models.CharField(max_length=100)
    CountryCode = models.CharField(max_length=10)
    ZoneName = models.CharField(max_length=100)
    GMTOffset = models.IntegerField()
    DST = models.IntegerField()
    ZoneStart = models.IntegerField()
    ZoneEnd = models.IntegerField()
    ImportDate = models.DateField(null=True)
    def __str__(self):
        return self.ZoneName

class TZDBErrorLog(models.Model):
    ErrorDate = models.DateField()
    ErrorMessage = models.CharField(max_length=255)
    def __str__(self):
        return self.ErrorMessage
