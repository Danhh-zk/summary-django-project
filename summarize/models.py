from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
import os
# Create your models here.

class Submission(models.Model):
    title = models.TextField(max_length=100)
    field = models.CharField(max_length=50)
    paper = models.FileField(upload_to='papers/', null=True, validators=[FileExtensionValidator(['pdf'])])
    summary = models.TextField(max_length=1000, blank=True, editable=False)
    date = models.DateTimeField(default=timezone.now, editable=False)
    
    def __str__(self) -> str:
        return self.title
    
    def delete(self, *args, **kwargs):
        if self.paper:
            if os.path.isfile(self.paper.path):
                os.remove(self.paper.path)
        super().delete(*args, **kwargs)