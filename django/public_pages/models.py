from django.db import models

class HotJar(models.Model):
    hotjar_script = models.CharField(max_length=2200)