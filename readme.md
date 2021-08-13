# Managed 404 pages with redirects

## forked from wagtail_managed404
... which was abandoned in 2018 and stopped working with Wagtail 2.9+
Original page: https://wagtail-managed404.readthedocs.io/


## Requirements
```
wagtailfontawesome
```

## Usage
To use cjk404 in a project, simply add it to the INSTALLED_APPS:

INSTALLED_APPS = [
    ...
    
    # if not installed:
    'wagtail.contrib.modeladmin',
    'wagtailfontawesome',

    # 404 app:
    'cjk404',
wagtailfontawesome is required to render the admin icon. 

wagtail.contrib.modeladmin is used for the admin panel itself.

And make sure to use the supplied middleware:

MIDDLEWARE = [
    ...

    'cjk404.middleware.PageNotFoundRedirectMiddleware',
]
Run the migrations:

./manage.py migrate