django-template-media
=======================

This module allows template writers to manipulate form media in templates.
This allows multiple forms on a page to share scripts with out including them twice.

All of the media included in the page using these tools
are collected into a single 'global'[1]_ ``Media`` instance for that page.
All operations are performed on this 'global'[1]_ ``Media`` instance.

Installing
==========

Install this package, using pip::

    $ pip install django-template-media

Add it to your ``INSTALLED_APPS`` and ``TEMPLATE_CONTEXT_PROCESSORS``::

    INSTALLED_APPS += (
        'django_template_media',
    )

    TEMPLATE_CONTEXT_PROCESSORS += (
        'django_template_media.context_processors.template_media',
    )

Load the template tags in your templates by loading the ``media_tags`` library::

    {% load media_tags %}

Using
=====

The tools are designed to work with the template heirarchy in a sane manner.
The examples will assume a ``site.html`` base template that defines a block named ``media``,
and two ``{% print_media %}`` tags to print the accumulated media files::

    <!doctype html>
    <html>
        <head>
            <title>Example site</title>

            {# Define the media for the page. This block is not printed #}
            {% load media_tags %}
            {% block media %}{% media %}
                {% add_css "screen" "css/bootstrap.css" %}
                {% add_css "screen" "css/site.css" %}
                {% add_css "print" "css/print.css" %}

                {% add_js "js/jquery.js" %}
            {% media %}{% endblock %}

            {# print out CSS media in the <head> #}
            {% print_media "css" %}

        </head>
        <body>

            {% block body %}

            {# print out JS media at the end of the <body> #}
            {% print_media "js" %}

        </body>
    </html>

The ``media`` block is used by child templates to add media to the site media.
The block does not have to be named ``media``,
it just has to be named the same thing on all templates.
The block must appear *before* any calls to ``{% print_media %}``

Printing the media
------------------

The ``{% print_media %}`` tag prints all of the media accumulated on the page so far.
A sensible place to put this is in your base template.

Calling this tag with no arguments will print out all of the accumulated media.

You can print out just the ``css`` or ``js`` by supplying a second argument::

    {% print_media "css" %}

    {% print_media "js" %}

Building media in the template
------------------------------

If you want to construct an ad-hoc media instance,
for site-wide media or fancy pages,
you can use the ``{% media %}`` block.
The ``Media()`` instance generated will be added to the current page media.
Just as in ``Media`` classes on forms, the same file can be named multiple times —
only the first instance will be used.
You can safely name all dependencies of the current page,
without worrying about including the dependency multiple times::

    {% extends "site.html" %}

    {% load media_tags %}
    {% block media %}
        {% media %}

            {% add_js "js/jquery.js" %}
            {% add_js "js/jquery.lib.js" %}
            {% add_js "js/bootstrap.js" %}
            {% add_js "js/bootstrap.lib.js" %}

            {% add_css "screen" "css/bootstrap.css" %}
            {% add_css "screen" "css/widget.css" %}

            {% if user.is_anonymous %}
                {% add_media login_form.media %}
            {% endif %}

        {% endmedia %}

        {# This is called **after** adding all the media #}
        {{ block.super }}
    {% endblock %}

The three possible tags in the ``{% media %}`` block are as follows:

``{% add_js path %}``
    Add the JavaScript file ``path`` to the media.
    Multiple files can be specified in the one tag,
    or just place them one after another as a series of tags.

``{% add_css media_type path %}``
    Add the CSS file ``path`` to the media, with ``media_type``.
    Multiple files can be specified in the one tag,
    or just place them one after another as a series of tags.

``{% add_media media %}``
    Adds the named form media to the current media.
    Multiple media instances can be added at once by naming them all.
    or just place them one after another as a series of tags.

Adding media from forms
-----------------------

If you just want to add a single JavaScript file or CSS file,
or a single form media instance,
you do not need to wrap everything in a ``{% media %}`` block::

    {% extends 'site.html' %}

    {% load media_tags %}

    {% block body %}
        <form action='.' method='post'>
            {% csrf_token %}
            {{ form }}
            <input type="submit">
        </form>
    {% endblock %}

    {% block media %}
        {% add_media form.media %}
        {{ block.super }}
    {% endblock %}

The ``{% add_media %}`` tag accepts multiple media instances,
so if you have multiple forms, you can add the media for all of them at once::

    {% add_media form_1.media form_2.media %}

Working with template hierarchies
---------------------------------

In sub-templates, the call to ``{{ block.super }}``
*must* be placed *after* all calls that modify the media.
As the media is printed out in an ancestor's ``{% block media %}``,
the sub-template must add all of the media it needs
before calling ``{{ block.super }}``.

``{% add_js %}``, ``{% add_css %}`` and ``{% add_media %}`` tags outside of
``{% media %}`` blocks always *prepend* new media to the current page media.
This is because templates are rendered from the child to the parent,
and parent media should precede child media.
Thus, if you have multiple ``{% add_media %}`` or ``{% media %}`` tags in once page,
the media will be printed out in reverse order to its appearance on the page.
As such, you are encouraged to have only one
``{% add_media %}`` or ``{% media %}`` block per template,
to prevent confusion.

In a ``{% media %}`` block, calls to ``{% add_media %}``, ``{% add_js %}`` and
``{% add_css %}`` append media to the current ad-hoc media instance.

------------------------

.. [1]
   The 'global' ``Media`` instance is stored in the currently rendering template context.
   It is only global to the whole page that is currently being constructed,
   not across all templates.
