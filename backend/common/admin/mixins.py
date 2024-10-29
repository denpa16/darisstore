from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.forms import ModelChoiceField


class DeclaredFirstAdminMixin:
    """DeclaredFirstAdminMixin."""

    def get_form(self, request, obj=None, change=False, **kwargs) -> None:
        """Form."""
        form = super().get_form(request, obj, change, **kwargs)
        for field in reversed(form.declared_fields.keys()):
            form.base_fields.move_to_end(field, last=False)
        return form


# noinspection PyProtectedMember, PyUnresolvedReferences
class WrapRelatedAdminMixin:
    """WrapRelatedAdminMixin."""

    def _wrap_related_field(self, name, field, model, request) -> None:
        """Оборачивает виджет внешнего ключа в RelatedFieldWidgetWrapper.

        Для появления кнопок с действиями: добавить, изменить, удалить.
        """
        if isinstance(field.widget, RelatedFieldWidgetWrapper):
            return
        rel = model._meta.get_field(name).remote_field
        rel_admin = self.admin_site._registry.get(model)
        can_change_related = (rel_admin.has_change_permission(request),)
        can_delete_related = (rel_admin.has_delete_permission(request),)
        can_view_related = (rel_admin.has_view_permission(request),)
        field.widget = RelatedFieldWidgetWrapper(
            field.widget,
            rel,
            self.admin_site,
            can_change_related=can_change_related,
            can_delete_related=can_delete_related,
            can_view_related=can_view_related,
        )

    def get_form(self, request, obj=None, change=False, **kwargs) -> None:
        """Добавляем в форму CRUD кнопки для полей выбора внешних ключей."""
        form = super().get_form(request, obj=obj, change=change, **kwargs)
        model_field_names = [field.name for field in self.model._meta.fields]
        for field_name, field in form.base_fields.items():
            if isinstance(field, ModelChoiceField) and field_name in model_field_names:
                self._wrap_related_field(field_name, field, self.model, request)
        return form
