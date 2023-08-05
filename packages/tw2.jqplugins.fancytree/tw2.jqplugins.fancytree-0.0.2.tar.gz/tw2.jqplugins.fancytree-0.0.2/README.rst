tw2.jqplugins.fancytree
=========================

:Author: Robert Sudwarts <robert.sudwarts@gmail.com>

.. comment: split here

.. _toscawidgets2 (tw2): http://toscawidgets.org/documentation/tw2.core/
.. _fancytree: https://github.com/mar10/fancytree/
.. _fancytree_demo: http://wwwendt.de/tech/fancytree/demo/
.. _fancytree_source: https://github.com/mar10/fancytree/

tw2.jqplugins.fancytree is a `toscawidgets2 (tw2)`_ wrapper for `fancytree`_.

Fancytree is the renamed/updated version of DynaTree and this tw2 widget
draws heavily on the work of Ralph Bean's wrapper for the earlier version.
`(tw2.jqplugins.dynatree) <https://github.com/toscawidgets/tw2.jqplugins.dynatree>`_


Live Demo
---------
[not yet available]
Peep the `live demonstration <http://tw2-demos.threebean.org/module?module=tw2.jqplugins.fancytree>`_.

Links
-----
[to be assigned]
Get the `source from github <http://github.com/toscawidgets/tw2.jqplugins.fancytree>`_.

`PyPI page <http://pypi.python.org/pypi/tw2.jqplugins.fancytree>`_
and `bugs <http://github.com/toscawidgets/tw2.jqplugins.fancytree/issues/>`_

Description
-----------

`toscawidgets2 (tw2)`_ aims to be a practical and useful widgets framework
that helps people build interactive websites with compelling features, faster
and easier. Widgets are re-usable web components that can include a template,
server-side code and JavaScripts/CSS resources. The library aims to be:
flexible, reliable, documented, performant, and as simple as possible.

`fancytree`_ is a jQuery plugin that allows to dynamically create html
tree view controls using JavaScript.

This module, tw2.jqplugins.fancytree, provides `toscawidgets2 (tw2)`_ access
to `fancytree`_ widgets.

Sampling tw2.fancytree in the WidgetBrowser
---------------------------------------------

The best way to scope out ``tw2.fancytree`` is to load its widgets in the
``tw2.devtools`` WidgetBrowser.  To see the source code that configures them,
check out ``tw2.fancytree/tw2/fancytree/samples.py``

To give it a try you'll need git, python, and `virtualenvwrapper
<http://pypi.python.org/pypi/virtualenvwrapper>`_.  Run::

    $ git clone git://github.com/toscawidgets/tw2.fancytree.git
    $ cd tw2.fancytree
    $ mkvirtualenv tw2.fancytree
    (tw2.fancytree) $ pip install tw2.devtools
    (tw2.fancytree) $ python setup.py develop
    (tw2.fancytree) $ paster tw2.browser
        or
    (tw2.fancytree) $ gearbox tw2.browser

And then browse to http://localhost:8000/ (possibly :8001) to check it out.
