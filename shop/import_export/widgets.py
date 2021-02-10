from import_export import widgets


class CategoryWidget(widgets.ForeignKeyWidget):
    def clean(self, value, row=None, *args, **kwargs):
        val = super(widgets.ForeignKeyWidget, self).clean(value)
        if val:
            obj, created = self.get_queryset(value, row, *args, **kwargs).get_or_create(**{self.field: val})
            return obj
        else:
            return None