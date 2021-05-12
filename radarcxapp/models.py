from django.db import models

class Coin(models.Model):
    name = models.CharField(max_length=20)
    realtime_price = models.IntegerField()
    moving_average = models.IntegerField()
    volume = models.IntegerField()


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

    coin = models.CharField(max_length=20)
    type = models.CharField(max_length=16, choices=TYPE_CHOICES)
    smaller_or_greater = models.CharField(max_length=16, choices=OPERATOR_CHOICES)
    quantity = models.IntegerField()
