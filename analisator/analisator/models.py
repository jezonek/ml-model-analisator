from django.db import models
from django.contrib.auth.models import User
from jsonfield import JSONField


class MLModel(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_on = models.DateTimeField(auto_now=True)
    report = JSONField(null=True, blank=True)
    model_file = models.FileField(upload_to="static/upload/%Y/%m/%d/")
    train_file = models.FileField(upload_to="static/upload/%Y/%m/%d/")
    test_file = models.FileField(upload_to="static/upload/%Y/%m/%d/")

    class Meta:
        ordering = ["-uploaded_on"]

    def __str__(self):
        return self.name
