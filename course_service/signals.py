from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Review, Course
from django.db.models import Avg

@receiver([post_save, post_delete], sender=Review)
def update_course_stats(sender, instance, **kwargs):
    course = instance.course
    reviews = Review.objects.filter(course=course)
    course.reviews = reviews.count()
    # Get the average rating if there are at least 1 rating else return the default rating
    if course.reviews != 0:
        course.average_rating = reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
    else:
        course.average_rating = Course._meta.get_field("average_rating").get_default()
    course.save()
