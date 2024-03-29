import django_filters
from .models import Announcement

class PriceModelFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    sub_category_id = django_filters.NumberFilter(field_name='sub_category_id')

    class Meta:
        model = Announcement
        fields = ['min_price', 'max_price', 'sub_category_id']
