from django_filters import rest_framework as filters, DateFromToRangeFilter

from apps.posts.models import Like


class LikeFilter(filters.FilterSet):
    created = DateFromToRangeFilter()

    class Meta:
        model = Like
        fields = ("created",)
