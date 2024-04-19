from django.db import models


class Subscriber(models.Model):
    email = models.EmailField(blank=False, null=False, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email + " " + str(self.is_active)
