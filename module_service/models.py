from shortuuid.django_fields import ShortUUIDField 
from django.db import models


class Tag(models.Model):
    id = ShortUUIDField(primary_key=True, length=6, max_length=6, editable=False)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

class TagModule(models.Model):
    id = ShortUUIDField(primary_key=True, length=6, max_length=6, editable=False)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    module = models.ForeignKey('Module', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.tag.name} - {self.module.name}"
    

class Module(models.Model):
    id = ShortUUIDField(primary_key=True, length=6, max_length=6, editable=False)
    name = models.CharField(max_length=200)
    course_id = models.UUIDField()
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='thumbnails/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    tags = models.ManyToManyField(Tag, through='TagModule')

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['course_id']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['name']
