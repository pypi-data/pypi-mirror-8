Renderers to show icons in the input fields for the django-bootstrap3 project from dyve: https://github.com/dyve/django-bootstrap3

Installation
------------

1. Install using pip:

   `` pip install django-bootstrap3``
   `` pip install git+https://github.com/ALibrada/django-bootstrap3-iconfield.git#egg=bootstrap3-iconfield``

   Alternatively, you can install download or clone this repo and call ``pip install -e .``.

2. Add to INSTALLED_APPS in your ``settings.py``:

   ``'bootstrap3',``
   ``'bootstrap3-iconfield'``

3. In your templates, load the ``bootstrap3`` library and use the ``bootstrap_*`` using the layouts icons or icons-horizontal:


Example template for the original layout with icons
----------------

   .. code:: Django

    {% load bootstrap3 %}

    {# Display a form #}

    <form action="/url/to/submit/" method="post" class="form">
        {% csrf_token %}
        {% bootstrap_form form layout="icons"%}
        {% buttons %}
            <button type="submit" class="btn btn-primary">
                {% bootstrap_icon "star" %} Submit
            </button>
        {% endbuttons %}
    </form>

Example template for the horizontal layout with icons
----------------

   .. code:: Django

    {% load bootstrap3 %}

    {# Display a form #}

    <form action="/url/to/submit/" method="post" class="form">
        {% csrf_token %}
        {% bootstrap_form form layout="icons-horizontal"%}
        {% buttons %}
            <button type="submit" class="btn btn-primary">
                {% bootstrap_icon "star" %} Submit
            </button>
        {% endbuttons %}
    </form>


Requirements
------------

- Python 2.6, 2.7, 3.2 or 3.3
- Django >= 1.4
- django-boostrap3 https://github.com/dyve/django-bootstrap3

License
-------

You can use this under Apache 2.0. See `LICENSE
<LICENSE>`_ file for details.

Disclaimer
-------

This is my first django package and I took django-bootstrap3 from dyve as template and
many other small parts of the code from the other people, mostly stackoverflow.
