from shortuuid.django_fields import ShortUUIDField 
from django.db import models
from course_service.models import Course


class Tag(models.Model):
    id = ShortUUIDField(primary_key=True, length=6, max_length=6, editable=False)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

class Module(models.Model):
    id = ShortUUIDField(primary_key=True, length=6, max_length=6, editable=False)
    name = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course')
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='module_service/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    tags = models.ManyToManyField(Tag, through='TagModule')

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['id']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['name']


class TagModule(models.Model):
    id = ShortUUIDField(primary_key=True, length=6, max_length=6, editable=False)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    module = models.ForeignKey('Module', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.tag.name} - {self.module.name}"
