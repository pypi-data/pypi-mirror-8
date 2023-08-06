Version History
===============

v1.6.1, 2014-12-07
  * Fix issue 6: don't crash if the background color is not present in the palette 
  * Depend on Pillow 2.6, remove dispose workaround

v1.6, 2014-07-13
  * Use correct background color for gifs.
  * Use per-fame delay time for gifs
  * workaround for dispose problem in pillow
  * refactoring of the animation code (old bugs replaced by new)

v1.5, 2014-06-21
  * Support for TinyMux (``--tinymux``) [marando]

v1.4.1, 2014-06-09
  * Support for Python 3.3 and 3.4

v1.4, 2014-06-09
  * Support for NUTS talkers (``--nuts``) [marando]
  * Support for Python 2.6

v1.3, 2014-04-06
  * Support for 16-color terminals (``--shell4``)
  * Slightly smoother animations
  * Only list ``Pillow`` as a dependency. The traditional ``PIL``
    might still work, but it will not be tested against.

v1.2.2, 2014-03-16
  * Make animations appear in the normal text flow
  * Fix problem where animations would sometimes 'jump'
  * Added ``--version`` parameter
  * Leave the last frame of an animation visible when quitting
  * Added lots of docstrings
  * Animation might be slightly smoother on slow terminals

v1.2.1, 2014-03-10
  * Fixed crash when trying to animate pictures that are not animated

v1.2, 2014-03-09
  * Animation support
  * Somewhat prettier results from re-sizing 

V1.1, 2014-03-02
  * Support Pillow [livibetter]
  * Support reading from STDIN 
  * Misc scaling options 

V1.0, 2014-03-01
  * Initial release
