from django.db import models

class Currency(models.Model):
    code   = models.CharField("Code",   max_length=3, unique=True)
    name   = models.CharField("Name",   max_length=20, db_index=True)
    symbol = models.CharField("Symbol", max_length=10)

    def __str__(self):
        return f"{self.code} – {self.name}"
