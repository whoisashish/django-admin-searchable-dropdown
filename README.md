# django-admin-searchable-dropdown

A Django admin filter implementation that renders as a searchable select field dropdown.

If you have more than twenty values for a field that you want to filter by in
Django admin, the filtering sidebar gets long, cluttered, sometimes wide and hence, hard to use.

This app contains the `DropdownFilter` class that renders as a drop-down in the
filtering sidebar that can be searched to avoid this problem.

# Example

Here's what it looks like:

![Screenshot of searchable dropdown admin filter](https://raw.githubusercontent.com/mrts/django-admin-list-filter-dropdown/master/docs/list-filter-dropdown.png)


# Usage

Install:

```sh
pip install django-admin-list-filter-dropdown
```

Enable in `settings.py`:

```py
INSTALLED_APPS = (
    ...
    'django_admin_searchable_dropdown',
    ...
)

```

Use in `admin.py`:

```py
from django_admin_searchable_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter

class EntityAdmin(admin.ModelAdmin):
    ...
    list_filter = (
        # for normal fields
        ('any_charfield', DropdownFilter),
        # for choice fields
        ('any_choicefield', ChoiceDropdownFilter),
        # for related fields
        ('any_foreignkey_field', RelatedDropdownFilter),
    )
```

Example of a custom filter that uses the provided template:

```py
class CustomFilter(SimpleListFilter):
    template = 'django_admin_searchable_dropdown/dropdown_filter.html'

    def lookups(self, request, model_admin):
        ...

    def queryset(self, request, queryset):
        ...
```

# Credits

Based on [this StackOverflow question](http://stackoverflow.com/a/20900314/258772) and
[code from FeinCMS](https://github.com/feincms/feincms/blob/master/feincms/templates/admin/filter.html) and
[code from mrts](https://github.com/mrts/django-admin-list-filter-dropdown/blob/8ab1575dcd3cb9b28a80cc07695cec65fa85dfad/django_admin_listfilter_dropdown/templates/django_admin_listfilter_dropdown/dropdown_filter.html).
