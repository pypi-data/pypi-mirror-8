## About Linksets

Linksets was originally built as a Django module to administer navigation menus with multiple levels inside templates, but it can also be used for simpler footer linksets, social media linksets, or anywhere you need an administrable list of links, with or without a hierarchy.

## Installation

You can include linksets directly into your site packages via pip:
```
pip install django-linksets
```

Or install as a library in venv/src by adding this line to your requirements.txt file:

```
-e git+https://github.com/gethee2anunnery/django-linksets.git#egg=django-linksets
```

## Configuration

If you installed linksets via your requirements file, you will need to add the venv/src directory to your project path:

```
VENV_SRC_DIR = os.path.join(APP_DIR, 'venv', 'src')
```

Then add linksets into your installed apps:

```
INSTALLED_APPS = (
    'linksets',
)
```

Then create the database table:
```
python manage.py syncdb
```

## Implementation

At minimum you will need to implement:

* admin.py
* models.py
* utils.py
* templatetags/links.py

Check the template in the example directory for how to implement linksets in your templates.
