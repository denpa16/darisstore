from collections.abc import Generator

from django.contrib.admin import SimpleListFilter, site
from django.db.models import QuerySet
from django_admin_listfilter_dropdown.filters import SimpleDropdownFilter


class ChaindedRelatedDropdownFilter(SimpleDropdownFilter):
    """Фильтр связанных объектов фильтрации админки."""

    lookup = None
    parent_parameters = None
    child_parameters = None
    model = None
    value_field = "id"
    title_field = "name"

    # noinspection PyProtectedMember
    def lookups(self, request, model_admin) -> list:
        """Lookups."""
        related_admin = model_admin.admin_site._registry.get(self.model)
        if not related_admin:
            related_admin = site._registry.get(self.model)
        queryset = related_admin.get_queryset(request)
        if self.parent_parameters:
            for parent_parameter in self.parent_parameters:
                if parent_parameter[0] in request.GET:
                    lookups = {parent_parameter[1]: request.GET[parent_parameter[0]]}
                    queryset = queryset.filter(**lookups)
        return queryset.distinct().values_list(self.value_field, self.title_field)

    # noinspection PyUnusedLocal
    def queryset(self, request, queryset) -> QuerySet:
        """Кверисет."""
        value = self.value()
        lookup = self.lookup
        if not lookup:
            lookup = self.parameter_name
        if value:
            return queryset.filter(**{lookup: self.value()})
        return None

    def choices(self, changelist) -> Generator:
        """Choices."""
        remove_params = list(self.child_parameters) if self.child_parameters else []
        remove_params += [self.parameter_name]
        yield {
            "selected": self.value() is None,
            "query_string": changelist.get_query_string({}, remove_params),
            "display": "All",
        }
        for lookup, title in self.lookup_choices:
            yield {
                "selected": self.value() == str(lookup),
                "query_string": changelist.get_query_string(
                    {self.parameter_name: lookup},
                    self.child_parameters,
                ),
                "display": title,
            }


class ChainedListFilter(SimpleListFilter):
    """Фильтр чьи варианты значений фильтруются на основе другого фильтра."""

    lookup = None
    parent_parameters = None
    child_parameters = None
    model = None
    value_field = "id"
    title_field = "name"

    # noinspection PyProtectedMember
    def lookups(self, request, model_admin) -> list:
        """Lookups."""
        related_admin = model_admin.admin_site._registry.get(self.model)
        if not related_admin:
            related_admin = site._registry.get(self.model)
        queryset = related_admin.get_queryset(request)
        if self.parent_parameters:
            for parent_parameter in self.parent_parameters:
                if parent_parameter[0] in request.GET:
                    lookups = {parent_parameter[1]: request.GET[parent_parameter[0]]}
                    queryset = queryset.filter(**lookups)
        return queryset.distinct().values_list(self.value_field, self.title_field)

    # noinspection PyUnusedLocal
    def queryset(self, request, queryset) -> QuerySet:
        """Кверисет."""
        value = self.value()
        lookup = self.lookup
        if not lookup:
            lookup = self.parameter_name
        if value:
            return queryset.filter(**{lookup: self.value()})
        return None

    def choices(self, changelist) -> Generator:
        """Choices."""
        remove_params = list(self.child_parameters) if self.child_parameters else []
        remove_params += [self.parameter_name]
        yield {
            "selected": self.value() is None,
            "query_string": changelist.get_query_string({}, remove_params),
            "display": "All",
        }
        for lookup, title in self.lookup_choices:
            yield {
                "selected": self.value() == str(lookup),
                "query_string": changelist.get_query_string(
                    {self.parameter_name: lookup},
                    self.child_parameters,
                ),
                "display": title,
            }
