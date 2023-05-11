import django_filters
from .models import Course 

class CourseFilter(django_filters.FilterSet):
    '''Customize filter to allow any Caps'''
    instructor_first_name = django_filters.CharFilter(field_name="instructor__user__first_name", lookup_expr="icontains")
    instructor_last_name = django_filters.CharFilter(field_name="instructor__user__last_name", lookup_expr="icontains")
    
    class Meta:
        model = Course 
        fields = ["instructor_first_name", "instructor_last_name", "difficulty", "is_certified", "reviews", "price", "is_available"]