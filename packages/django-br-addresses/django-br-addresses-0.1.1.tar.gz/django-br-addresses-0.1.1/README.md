# Django BR Locations

## Overview

This app do a reusable model and admin of CRUD cities and address of
Brazil

Image 1

Image 2

It has a two models abstracts in file `mixins.py` that will be used in your custom model if necessary

So you can build a custom City and Address Model extend of others Mixins and register it
in admin.

```
from django_br_address.mixins import CityMixin, AddressMixin

# models.py

class CustomCity(CityMixin, Mixin2, Mixin3)
    pass

# admin.py
from django_br_address.admin import CityAdmin
from customapp.model import CustomCity

admin.site.unregister(CityAdmin)
admin.site.register(CustomCity)
```


## How to install

`pip install django-br-addresses`

## How to use

Put the app in settings installed apps.

```
INSTALLED APPS = [
    'django-br-address'
]
```

### To use in django<1.7

```
SOUTH_MIGRATION_MODULES = {
    'django-br-addresses.br_addresses': 'django-br-addresses.br_addresses.south_migrations',
}

```


## Running tests

Install the requirements in tests directory

`pip install -r requirements.txt`

Go to a tests directory and run the command below

```
python manage.py runstests.py
```



## Todo

1 - Do a geospatial localization of address with latitude and longitude
