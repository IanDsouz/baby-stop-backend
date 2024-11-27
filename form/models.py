from django.db import models

class Submission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    product = models.CharField(max_length=100)
    date_submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.product}"
