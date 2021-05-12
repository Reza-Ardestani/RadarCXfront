from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Coin(models.Model):
    name = models.CharField(max_length=20)
    realtime_price = models.IntegerField()
    moving_average = models.IntegerField()
    volume = models.IntegerField()
    date_updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.name}'


class FavoriteCoins(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    favorite_coin = models.ForeignKey(Coin, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} likes {self.favorite_coin} coin!'


class Condition(models.Model):
    TYPE_CHOICES = (
        ("p", "price"),
        ("v", "volume"),
        ("m", "moving_average")
    )

    OPERATOR_CHOICES = (
        ("g", "greater_than"),
        ("s", "smaller_than"),
    )

    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    coin = models.CharField(max_length=20)
    type = models.CharField(max_length=16, choices=TYPE_CHOICES)
    smaller_or_greater = models.CharField(max_length=16, choices=OPERATOR_CHOICES)
    quantity = models.IntegerField()
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.creator} {self.coin} {self.type} {self.smaller_or_greater} {self.quantity}'