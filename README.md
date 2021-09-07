[![PyPI version](https://d25lcipzij17d.cloudfront.net/badge.svg?id=py&r=r&type=6e&v=1.2&x2=0)](https://pypi.org/project/django-admin-searchable-dropdown/1.2/)

Django Admin Searchable Dropdown
================================
A Django admin filter implementation that renders as a searchable select field dropdown.


Overview:
---------

If you have more than twenty values for a field that you want to filter by in
Django admin, the filtering sidebar gets long, cluttered, sometimes wide and hence, hard to use.

This app contains the `AutocompleteFilter` class that renders as a drop-down in the
filtering sidebar that can be searched to avoid this problem. 

Requirements:
-------------

Requires Django version >= 2.0

Features:
-------------

* Custom search view/endpoint ([more details](#functionality-to-provide-a-custom-view-for-search))
* `list_filter` Filter Factory support ([more details](#shortcut-for-creating-filters))
* Custom widget text ([more details](#customizing-widget-text))
* Support for [Grappelli](https://grappelliproject.com/)


Installation:
-------------

You can install it via pip.  To get the latest version clone this repo.

```shell script
pip install django-admin-searchable-dropdown
```

Add `admin_searchable_dropdown` to your `INSTALLED_APPS` inside settings.py of your project.


Usage:
------

Let's say you have following models:
```python
from django.db import models

class CarCompany(models.Model):
    name = models.CharField(max_length=128)

class CarModel(models.Model):
    name = models.CharField(max_length=64)
    company = models.ForeignKey(CarCompany, on_delete=models.CASCADE)
```

And you would like to filter results in `CarModelAdmin` on the basis of `company`.  You need to define `search fields` in `CarCompany` and then define filter like this:

```python
from django.contrib import admin
from admin_searchable_dropdown.filters import AutocompleteFilter


class CarCompanyFilter(AutocompleteFilter):
    title = 'Company' # display title
    field_name = 'company' # name of the foreign key field


class CarCompanyAdmin(admin.ModelAdmin):
    search_fields = ['name'] # this is required for django's autocomplete functionality
    # ...


class CarModelAdmin(admin.ModelAdmin):
    list_filter = [CarCompanyFilter]
    # ...
```

After following these steps you may see the filter as:

![](https://raw.githubusercontent.com/whoisashish/django-admin-searchable-dropdown/main/admin_searchable_dropdown/media/UnFiltered.PNG)

![](https://raw.githubusercontent.com/whoisashish/django-admin-searchable-dropdown/main/admin_searchable_dropdown/media/Filtered.PNG)


Functionality to provide a custom view for search:
--------------------------------------------------

You can also register your custom view instead of using Django admin's `search_results` to control the results in the autocomplete. For this you will need to create your custom view and register the URL in your admin class as shown below:

In your `views.py`:

```python
from admin_searchable_dropdown.views import AutocompleteJsonView


class CustomSearchView(AutocompleteJsonView):
    def get_queryset(self):
        """
           your custom logic goes here.
        """
        queryset = CarCompany.objects.all().order_by('name')
        return queryset
```

After this, register this view in your admin class:

```python
from django.contrib import admin
from django.urls import path


class CarModelAdmin(admin.ModelAdmin):
    list_filter = [CarCompanyFilter]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('custom_search/', self.admin_site.admin_view(CustomSearchView.as_view(model_admin=self)),
                 name='custom_search'),
        ]
        return custom_urls + urls
```

Finally, just tell the filter class to use this new view:

```python
from django.shortcuts import reverse
from admin_searchable_dropdown.filters import AutocompleteFilter


class CarCompanyFilter(AutocompleteFilter):
    title = 'Company'
    field_name = 'company'

    def get_autocomplete_url(self, request, model_admin):
        return reverse('admin:custom_search')
```


Shortcut for creating filters:
------------------------------

It's also possible to use the `AutocompleteFilterFactory` shortcut to create
filters on the fly, as shown below. Nested relations are supported too, with
no need to specify the model.

```
An autocomplete widget filter with a customizable title. Use like this:
        AutocompleteFilterFactory('My title', 'field_name')
        AutocompleteFilterFactory('My title', 'fourth__third__second__first')
    Be sure to include distinct in the model admin get_queryset() if the second form is used.
    Assumes: parameter_name == f'fourth__third__second__{field_name}'
        * title: The title for the filter.
        * base_parameter_name: The field to use for the filter.
        * viewname: The name of the custom AutocompleteJsonView URL to use, if any.
        * use_pk_exact: Whether to use '__pk__exact' in the parameter name when possible.
        * label_by: How to generate the static label for the widget - a callable, the name
          of a model callable, or the name of a model field.
```

Example:

```python
from django.contrib import admin
from admin_searchable_dropdown.filters import AutocompleteFilterFactory


class AlbumAdmin(admin.ModelAdmin):
    list_filter = [
        AutocompleteFilterFactory('Company', 'company', 'admin:custom_search', True)
    ]

    def get_urls(self):
        """As above..."""
```


Customizing widget text
-----------------------

You can customize the text displayed in the filter widget, to use something
other than `str(obj)`. This needs to be configured for both the dropdown
endpoint and the widget itself.

In your `views.py`, override `display_text`:

```python
from admin_searchable_dropdown.views import AutocompleteJsonView


class CustomSearchView(AutocompleteJsonView):

    @staticmethod
    def display_text(obj):
        return obj.my_str_method()

    def get_queryset(self):
        """As above..."""
```

Then use either of two options to customize the text.

Option one is to specify the form_field in an AutocompleteFilter in your
`admin.py`:

```python
from django import forms
from django.contrib import admin
from django.shortcuts import reverse
from admin_searchable_dropdown.filters import AutocompleteFilter


class FuelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.my_str_method()


class CarCompanyFilter(AutocompleteFilter):
    title = 'Company'
    field_name = 'company'
    form_field = FuelChoiceField

    def get_autocomplete_url(self, request, model_admin):
        return reverse('admin:custom_search')


class CarModelAdmin(admin.ModelAdmin):
    list_filter = [CarCompanyFilter]

    def get_urls(self):
        """As above..."""
```

Option two is to use an AutocompleteFilterFactory in your `admin.py`
add a `label_by` argument:

```python
from django.contrib import admin
from admin_searchable_dropdown.filters import AutocompleteFilterFactory


class CarModelAdmin(admin.ModelAdmin):
    list_filter = [
        AutocompleteFilterFactory('Company', 'company', 'admin:custom_search', True, label_by='my_str_method')
    ]

    def get_urls(self):
        """As above..."""
```


Contributing:
------------

Based on [this StackOverflow question, and the comments that went unresolved in the selected answer](http://stackoverflow.com/a/20900314/258772) and
[code from FeinCMS](https://github.com/feincms/feincms/blob/master/feincms/templates/admin/filter.html) and
[code from mrts](https://github.com/mrts/django-admin-list-filter-dropdown/blob/8ab1575dcd3cb9b28a80cc07695cec65fa85dfad/django_admin_listfilter_dropdown/templates/django_admin_listfilter_dropdown/dropdown_filter.html).

To Contribute, please fork the project, make a pull-request, and clearly mention the problems or improvements your PR is addressing.


License:
--------

Django Admin Searchable Dropdown is an Open Source project licensed under the terms of the MIT LICENSE.
