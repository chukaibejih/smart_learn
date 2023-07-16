import django_filters
from .models import Enrollment


class EnrollmentFilter(django_filters.FilterSet):
    enrollment_date = django_filters.DateFromToRangeFilter(
        field_name='enrollment_date')

    class Meta:
        model = Enrollment
        fields = ['enrollment_date']
