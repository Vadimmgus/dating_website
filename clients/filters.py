from clients.models import User
from clients.utils import SearchFilterSet
import django_filters
from django.contrib.gis.geos import Point, GEOSGeometry


class UserFilter(SearchFilterSet):
    """
    Фильтр пользователей
    """
    distance = django_filters.NumberFilter(method='filter_distance')

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'gender',
            'distance',
        )

    def filter_queryset(self, queryset):
        qs = super().filter_queryset(queryset)  # type: User
        return qs

    def filter_distance(self, qs, name, value):
        if not value:
            return qs
        pnt = GEOSGeometry(f'SRID=4326;POINT({str(self.request.user.longitude)} {str(self.request.user.latitude)})')
        ids = []
        users = User.objects.exclude(pk=self.request.user.pk).exclude(longitude__isnull=True).exclude(latitude__isnull=True).all()
        for item in users:
            pnt2 = GEOSGeometry(f'SRID=4326;POINT({str(item.longitude)} {str(item.latitude)})')
            if pnt.distance(pnt2) < value:
                ids.append(item.id)
        return qs.filter(pk__in=ids)
