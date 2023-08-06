Installation
============

1. Add ``cmstemplates`` to ``INSTALLED_APPS``
2. Append ``cmstemplates.loaders.Loader`` to
   the end of ``TEMPLATE_LOADERS`` setting
3. Configure your file-based templates directory::

    ZONE_TEMPLATES_DIR = os.path.join(BASE_DIR, 'zone_templates')

4. Create directory ``zone_templates`` near ``settings.py`` file
5. Run ``./manage.py migrate cmstemplates``
6. Go to admin and create new zone template with name *test-zone*
7. Add this zone to your template with built-in django ``include`` tag::

    {% include "test-zone" %}

Using codemirror widget
=======================

Add to your settings::

    ZONE_TEMPLATE_USE_CODEMIRROR = True

Install codemirror widget::

1. source env/bin/activate
2. pip install django-codemirror-widget
3. cd project_name/static/vendor
4. wget http://codemirror.net/codemirror.zip
5. unzip codemirror.zip
6. mv codemirror-4.2 codemirror
7. Add to settings::

    CODEMIRROR_PATH = 'vendor/codemirror'
    CODEMIRROR_THEME = 'default'
    CODEMIRROR_CONFIG = {'lineNumbers': True}


Final settings should look like this::

    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
        'django.template.loaders.eggs.Loader',
        'cmstemplates.loaders.Loader',
    )

    # cmstemplates
    ZONE_TEMPLATES_DIR = os.path.join(BASE_DIR, 'zone_templates')
    ZONE_TEMPLATE_USE_CODEMIRROR = True

    # codemirror
    CODEMIRROR_PATH = 'vendor/codemirror'
    CODEMIRROR_THEME = 'default'
    CODEMIRROR_CONFIG = {'lineNumbers': True}
