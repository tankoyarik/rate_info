import django.db.models as models


class Rate(models.Model):
    base = models.CharField(max_length=10)
    target = models.CharField(max_length=10)
    price = models.FloatField(default=0.0)
    refreshed = models.DateTimeField(auto_now_add=True)


class Account(models.Model):
    username = models.CharField(max_length=200, unique=True)
    saved_rates = models.ManyToManyField(Rate)

class Ivan(models.Model):
    pass


