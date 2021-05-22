from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Coin(models.Model):
    name = models.CharField(max_length=20)
    realtime_price = models.FloatField()
    moving_average = models.FloatField()
    volume = models.FloatField()
    date_updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.name}'


class FavoriteCoins(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    favorite_coin = models.ForeignKey(Coin, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} likes {self.favorite_coin} coin!'


class UserToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=40)

    def __str__(self):
        return f'{self.user} {self.token}'


class Condition(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    coin = models.CharField(max_length=20)
    type = models.CharField(max_length=16)
    smaller_or_greater = models.CharField(max_length=1)
    quantity = models.FloatField()
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.creator} -> {self.name}'
