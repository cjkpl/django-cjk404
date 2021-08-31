# Managed 404 Pages with Redirects

![Thank You Page](./readme/404.png)

## Description

Looking for Wagtail package which will give you ability to automatic searching and creation of redirects from within backend panel? If you are disappointed and frustrated by lack of support from the framework itself on this matter, get started with [Cjk404](https://github.com/cjkpl/dj-apps-cjk404). 


### Features

- Automatic "404 Not Found" HTTP Error Detection Following the Non-Existent Page Opening 
- Support for Redirects to [Wagtail Pages](https://docs.wagtail.io/en/stable/reference/pages/index.html)

### How It Works  

- `Regular Expression → Regular Expression` or `Regular Expression → URL`
- `Regular Expression → Wagtail Site`
- `URL → URL`
- `URL → Wagtail Site`

### Repository forked from [wagtail_managed404](https://wagtail-managed404.readthedocs.io/) project...
...which was abandoned in 2018 (and stopped working with Wagtail 2.9 version and higher) and shortly after merged with another (Django) package - [django-regex-redirects](https://github.com/maykinmedia/django-regex-redirects).

Both projects were so similar (one `Model` class and fairly uncomplicated `Middleware`), so the easiest thing was simply to combine them. Below, you can see the classes comparison of those two.

| **Django Regex Redirects**      | **Wagtail Managed 404 (Cjk404)** |
|:---------------------------:|:----------------------------:|
| `class Redirect(models.Model)`                    | `class PageNotFoundEntry(models.Model)`                |
| • `old_path`                    | • `url`                     |
| • `new_path`             | • `redirect_to_url` or `redirect_to_page`                   |
| • `regular_expression`               | -                     |
| • `fallback_redirect`              | -                     |
| • `nr_times_visited`           | • `hits`                     |

**Important:** Thankfully, [django-regex-redirects](https://github.com/maykinmedia/django-regex-redirects) included tests, but which have not been run yet, so may not function properly.


### Dependencies
- wagtail.contrib.modeladmin (https://docs.wagtail.io/en/stable/reference/contrib/modeladmin/index.html)

This package is used for the admin panel itself.

- wagtailfontawesome (https://pypi.org/project/wagtailfontawesome)

The following package is required to render the admin icon.

## Screenshots

#### "All Redirects" in the Backend

!["All Redirects" in the Backend"](./readme/All%20Redirects.jpg)

#### "Edit Redirect" in the Backend 

!["Edit Redirect" in the Backend](./readme/Edit%20Redirect.jpg)

### Usage
To use it in a project, simply add it to the INSTALLED_APPS:

```python
INSTALLED_APPS = [
    'wagtail.contrib.modeladmin',
    'wagtailfontawesome',

    'cjk404'
]
```

Additionally, please use the supplied middleware:

```python
MIDDLEWARE = [
    'cjk404.middleware.PageNotFoundRedirectMiddleware'
]
```

Finally, run the migrations:
```python
./manage.py migrate
```

**Important:** In case of problems with installation, please clear all the cache and restart the server (repeatedly, if necessary).

```python
python3 manage.py runserver 
```

## Authors

- [Grzegorz Król](https://github.com/cjkpl)
- [Filip Woźniak](https://github.com/FilipWozniak)