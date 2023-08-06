**************************
collective.z3cform.widgets
**************************

.. contents:: Table of Contents

Life, the Universe, and Everything
----------------------------------

A widget package for Dexterity projects.

.. Warning::
    This package is no longer being actively maintained.
    Take a look at `plone.app.widgets`_ for an alternative set of widgets.

collective.z3cform.widgets provides the following widgets:

**EnhancedTextLinesFieldWidget**
    This widget is an ajaxified version of the TextLinesFieldWidget that will
    allow creation, sort, update and deletion of text lines; degrades to
    <textarea> if JavaScript is not enabled.

    .. image:: https://github.com/collective/collective.z3cform.widgets/raw/master/enhancedtextlines.png
        :align: center
        :height: 143px
        :width: 600px

    This widget uses the `jQuery TaskPlease`_ plugin.

**TokenInputFieldWidget**
    TokenInputFieldWidget allows your users to select multiple items from
    portal Subjects list , using autocompletion as they type to find each
    item. You may have seen a similar type of text entry when filling in the
    recipients field sending messages on `Facebook`_. This widget will degrade
    to <textarea> if JavaScript is not enabled.

    .. image:: https://github.com/collective/collective.z3cform.widgets/raw/master/tokeninput.png
        :align: center
        :height: 110px
        :width: 600px

    This widget uses the `jQuery Tokeninput`_ plugin.

    If you install collective.z3cform.widgets in a Plone site it will replace
    every ICategorization subjects field's widget of any Dexterity-based
    content type with this one.

**MultiContentSearchFieldWidget**
    A widget to add a dynamic list of objects. This works as a widget for
    related items field so it must be used like this::

        relatedItems = RelationList(
            title=_(u'label_related_items', default=u'Related Items'),
            default=[],
            value_type=RelationChoice(title=u"Related",
                          source=ObjPathSourceBinder(portal_type='Document')),
            required=False,
            )
        form.widget(relatedItems=MultiContentSearchFieldWidget)

    The parameters passed to the ObjPathSourceBinder class are used to filter
    the search of elements to relate to. If no parameters are passed, a tree
    structure is shown in the widget.

**SimpleRichTextWidget**
    A lightweight and unbloated Rich Text Editor (RTE / WYSIWYG). These
    parameters can be configured::

        'iframe_height': height in pixels,
        'format_block': 'true' or 'false',
        'bold': 'true' or 'false',
        'italic': 'true' or 'false',
        'unordered_list': 'true' or 'false',
        'link': 'true' or 'false',
        'image': 'true' or 'false',
        'allow_disable': 'true' or 'false'

    This widget uses the `jQuery RTE`_ plugin.

Mostly Harmless
---------------

.. image:: https://secure.travis-ci.org/collective/collective.z3cform.widgets.png?branch=master
    :alt: Travis CI badge
    :target: http://travis-ci.org/collective/collective.z3cform.widgets

.. image:: https://coveralls.io/repos/collective/collective.z3cform.widgets/badge.png?branch=master
    :alt: Coveralls badge
    :target: https://coveralls.io/r/collective/collective.z3cform.widgets

.. image:: https://pypip.in/d/collective.z3cform.widgets/badge.png
    :alt: Downloads
    :target: https://pypi.python.org/pypi/collective.z3cform.widgets

Got an idea? Found a bug? Let us know by `opening a support ticket`_.

Don't Panic
-----------

Installation
^^^^^^^^^^^^

To enable this product in a buildout-based installation:

1. Edit your buildout.cfg and add ``collective.z3cform.widgets`` to the list
   of eggs to install::

    [buildout]
    ...
    eggs =
        collective.z3cform.widgets

After updating the configuration you need to run ''bin/buildout'', which will
take care of updating your system.

Go to the 'Site Setup' page in a Plone site and click on the 'Add-ons' link.

Check the box next to ``collective.z3cform.widgets`` and click the 'Activate'
button.

Note: You may have to empty your browser cache and save your resource
registries in order to see the effects of the product installation.

New fields
^^^^^^^^^^

**EnhancedTextLinesFieldWidget**
    To use this widget we must use a List field or a Tuple field with the
    value_type as an schema.TextLine() like this::

        from collective.z3cform.widgets.enhancedtextlines import EnhancedTextLinesFieldWidget

        form.widget(options = EnhancedTextLinesFieldWidget)
        options = schema.Tuple(
            title=_(u"Options"),
            value_type=schema.TextLine(),
            missing_value=(),
            )

**TokenInputFieldWidget**
    To use this Widget we must use a List field or a Tuple field with the
    value_type as a schema.TextLine() like this::

        from collective.z3cform.widgets.token_input_widget import TokenInputFieldWidget

        form.widget(subjects=TokenInputFieldWidget)
        subjects = schema.List(
            title=_(u"Categories"),
            value_type=schema.TextLine(),
            default=[],
            )

**MultiContentSearchFieldWidget**
    The parameters passed to the ObjPathSourceBinder class are used to filter
    the search of elements to relate to.. if none parameter are passed, a tree
    structure is shown in the widget::

        from collective.z3cform.widgets.multicontent_search_widget import MultiContentSearchFieldWidget

        form.widget(relatedItems=MultiContentSearchFieldWidget)
        relatedItems = RelationList(
            title=_(u"Related Items"),
            default=[],
            value_type=RelationChoice(title=u"Related",
                source=ObjPathSourceBinder(portal_type='Document')),
            )

**SimpleRichTextWidget**
    TBA

Override existing fields
^^^^^^^^^^^^^^^^^^^^^^^^

TBA

Future widgets
--------------

The following widgets will be available in this package in the near future:

- widget to select an option from a list; this widget will degrade to <select>
  if JavaScript is not enabled.

- widget to select multiple options from a list; this widget will degrade to
  <select> if JavaScript is not enabled.

This widgets will probably use the `Chosen`_ plugin.

Browsers supported
------------------

All modern browsers should be supported (Mozilla Firefox 3.0+, Google Chrome
7.0+, Apple Safari 4.0+, Opera 10.0+ and Microsoft Internet Explorer 9.0+).

See also
--------

Not entirely unlike
-------------------

`collective.z3cform.datagridfield`_
    Version of DataGridField for use with Dexterity / z3c.form.

`plone.app.widgets`_
    A revamp of Plone widgets, it does this by overriding the widgets of some
    of the fields in Plone.

.. _`jQuery TaskPlease`: https://github.com/Quimera/tasksplease
.. _`jQuery Tokeninput`: http://loopj.com/jquery-tokeninput/
.. _`Chosen`: http://harvesthq.github.com/chosen/
.. _`Facebook`: http://www.facebook.com/
.. _`opening a support ticket`: https://github.com/collective/collective.z3cform.widgets/issues
.. _`eea.tags`: https://github.com/collective/eea.tags
.. _`jQuery RTE`: http://code.google.com/p/rte-light
.. _`collective.z3cform.datagridfield`: http://pypi.python.org/pypi/collective.z3cform.datagridfield
.. _`plone.app.widgets`: https://github.com/plone/plone.app.widgets
