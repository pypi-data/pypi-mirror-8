**Django Location Field**

Current version: 1.5.0

Allows users to input locations based on latitude and longitude, using a
Google maps widget.

MIT licensed

**Features**

* The map will automatically update after changing a field based on
* Works with both Spatial and non-Spatial databases
* Works perfectly with formsets

**Compatibility**

* Django 1.6 and 1.7
* Python 2.7 and 3.x

It was only tested with PostGIS but may work with other Spatial Databases.

**Installation**

1. Install through pip (or manually place it on your `PYTHON_PATH`).

    `pip install django-location-field`

2. Create a Spatial Database

For example, PostGIS:

    https://docs.djangoproject.com/en/dev/ref/contrib/gis/install/postgis/

**Configuration**

See the [example postgis](example_postgis/) and [example sqlite](example_sqlite/).

**Basic usage (using Spatial Database)**

    from django.contrib.gis.db import models
    from django.contrib.gis.geos import Point
    from location_field.models import LocationField

    class Place(models.Model):
        city = models.CharField(max_length=255)
        location = LocationField(based_fields=[city], zoom=7, default=Point(1, 1))
        objects = models.GeoManager()

Look that you must put `models.GeoManager()` in your model, or some errors will occur.

**Basic usage (without Spatial Database)**

    from django.db import models
    from location_field.models import PlainLocationField

    class Place(models.Model):
        city = models.CharField(max_length=255)
        location = PlainLocationField(based_fields=[city], zoom=7)

**Screenshot**

![Screenshot](http://img153.imageshack.us/img153/1914/screenshot20101005at161.png)
