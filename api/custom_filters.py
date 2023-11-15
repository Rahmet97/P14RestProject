from django_filters import rest_framework as filters

from .models import Blog


class BlogFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Blog
        fields = ['title', 'description']
