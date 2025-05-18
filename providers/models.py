from django.db import models

class Provider(models.Model):
    name = models.CharField(max_length=50, unique=True)
    class_path = models.CharField(
        max_length=200,
        help_text="Python path to adapter class"
    )
    is_active = models.BooleanField(default=True)
    priority = models.PositiveIntegerField(default=100)

    class Meta:
        ordering = ["priority"]

    def __str__(self):
        return f"{self.name} (priority={self.priority})"
