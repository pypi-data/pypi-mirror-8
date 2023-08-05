# django_lazy_admin

Django's automatic admin list screens are awesome! But sometimes you need custom columns to display information that requires some big queries or perhaps some heavy computation. This can slow down displaying the entire list screen. This app is meant to address that need, but converting a custom column in to one that can be dynamically loaded over AJAX on user action.

## Regular custom column

Django allows you to use admin methods to render a column on the change list screen. For example:

```python
class MyAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'custom_column')

    def custom_column(self, obj):
        return foo_takes_time(obj)
    
    custom_column.short_description = 'Custom Title'
```

## Lazy custom column

Lazy custom columns are loaded over AJAX by user action. This is achieved by adding a decorator over any custom list column function you've added in your ModelAdmin class.

```python
from lazy_admin import lazy_admin_column

class MyAdmin(admin.ModelAdmin):
    change_list_template = 'lazy_admin/change_list.html'
    
    list_display = ('name', 'age', 'custom_column')

    @lazy_admin_column
    def custom_column(self, obj):
        return foo_takes_time(obj)
    
    custom_column.short_description = 'Custom Title'
```

> Note the change_list_template of the MyAdmin class. This template loads the javascript necessary to handle the AJAX interaction.

## Install

Ideally, install the package in your virtual environment.

```
pip install django_lazy_admin
```

Now, add the app to your django setting INSTALLED_APPS.

```python
INSTALLED_APPS = (
    '...',
    'lazy_admin'
)
```

And, install the URL handler in your root url conf or in some other url configuration file.

```python
urlpatterns = patterns('',
    '...',
    url(r'^admin/lazy/', include('lazy_admin.urls')),
)
```

And, you're done!

## Configuration

You can turn off all lazy columns by the following in your main django settings.py file.

```python
LAZY_ADMIN_ALLOW = False
```

The column content is rendered using the lazy_admin/lazy_column.html template. You can over-ride this in your own app. Or you can use a parameter to the decorator.

```
@lazy_admin_column(template='my_custom_template.html')
```

## TODO

- Support Model class methods used as custom columns as well with the same decorator.


## Authors

The primary author of this package is Gautam Kachru <gautam@live.in>

## License

BSD 3-clause. See LICENSE file.

