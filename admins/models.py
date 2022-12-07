from django.db import models

# Create your models here.
class FAQ(models.Model):
    question = models.CharField('Qw', max_length=255)
    answer = models.TextField("Answer")

    def __str__(self):
        return self.question