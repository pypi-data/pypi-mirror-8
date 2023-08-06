
doscmd-screen
==============================================================================
 -- Screen positioning and colors in the dos shell (and unix too)

Installation
------------
::

   pip install doscmd-screen

Changes in version 1.0 include support for non-dos platforms, a visual 
test script, and zero-based indexing of screen positions. Since the last
one is a backwards incompatible change I have upped the major version 
number. I don't forsee any further backwards incompatible changes in 
this module.


Documentation
-------------

The documentation lives at http://doscmd-screen.readthedocs.org/


Usage
-----

Straight forward positioning and terminal colors in the terminal::

    import screen
    scr = Screen()
    scr.centerxy(scr.center, scr.middle, '((.))')

    scr.writexy(scr.left, scr.bottom, 
                'left bottom', 
		color='black', on='red')

Works for both Windows..

.. image:: screenshot-dos.png


..and unix-like terminals:

.. image:: screenshot-linux.png



