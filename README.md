

# Face Recognition and Emotion Detector Device
1. Orange PI 1
1. Python 3.10.0 + Django 3.2.9


# Project's file explanation

## Django

1. ### `manage.py`
Django commands handler<br>
Run `py manage.py [cmds]` instead of `py -m django [cmds]` or `django-admin [cmds]`

1. ### `COURSE`
|file name          |description|
|---                |---        |
|`__init__.py__`    |defining this module as a package                                              |
|`asgi.py`          |--for deployment purposes                                                      |
|`settings.py`      |settings of whole project (e.g. used apps [django.authentication, VITAZ...])   |
|`urls.py`          |project's url handler (admin, VITAZ...)                                        |
|`wsgi.py`          |--for deployment purposes                                                      |

1. ### `VITAZ`
|file name          |description|
|---                |---        |
|F `migrations`     |generating DB tables                           |
|F `templates`      |actually views (html...)                       |
|`__init__.py__`    |defining this module as a package              |
|`admin.py`         |admin interface                                |
|`apps.py`          |actually app config                            |
|`models.py`        |models're used for pulling data from DBs       |
|`tests.py`         |unit tests                                     |
|`urls.py`          |APP's url handler (home page, profile page...) |
|`views.py`         |return responses (Http, html...)               |

```
Copyright 2021, Evula A. S., All rights reserved.
```