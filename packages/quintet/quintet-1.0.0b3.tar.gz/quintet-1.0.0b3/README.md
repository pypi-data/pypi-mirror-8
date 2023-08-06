# Quintet
_A Bootstrapped Markdown CMS powered by Django_

[![Travis](http://img.shields.io/travis/quintet-cms/quintet.svg)](https://travis-ci.org/quintet-cms/quintet)
[![Code Health](https://landscape.io/github/quintet-cms/quintet/master/landscape.png)](https://landscape.io/github/quintet-cms/quintet/master)
[![pypi](http://img.shields.io/pypi/v/quintet.svg)](https://pypi.python.org/pypi/quintet/)
![License](http://img.shields.io/pypi/l/quintet.svg)

![Screenshot of edit post screen](http://thegoods.aj7may.com/content/images/2014/Sep/Screen_Shot_2014_09_29_at_11_23_26_PM.png)

## Getting Started

1. `pip install django`
2. `pip install quintet --pre`
3. `django-admin startproject myblog && cd myblog`
4. Add the following to your `settings.py`

        INSTALLED_APPS = (
            ...
            'django.contrib.humanize',
            'django_forms_bootstrap',
            'django_bootstrap_markdown',
            'django_bootstrap_typeahead',
            'django_password_strength',
            'quintet',
            ...
        )

5. `./manage.py migrate`
6. `./manage.py createsuperuser`
7. `./manage.py runserver`
8. Open <http://127.0.0.1:8000/quintet/>
