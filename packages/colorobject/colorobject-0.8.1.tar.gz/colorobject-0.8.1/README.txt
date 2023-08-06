================
colorobject
================

---------------
Highlights
---------------
*colorobjects* are *r, g, b, a* tuples that support easy conversion to other
color types (e.g. HSV, HLS, hexadecimal, or Matplotlib color names) and convenient 
transformation (e.g. adjust color lightness, hue, saturation, or alpha).
Conversions are as convenient as *c = somecolor.hsv*, and transformations as easy as
*somecolor.lightness = c*! And because a *colorobject* is just an extension of
the list type, they can be passed directly to any Matplotlib plotting command.

*colorlists* are lists of *colorobjects* that allow you to easily modify or 
construct colormaps (see module *colormaps*) or cycle through lists of maximally 
distinct colors (see module *discretecolors*). Changing the brightness of a
Matplotlib colormap can be as simple as *cmap_adjust(mycolormap, 'lighten', 0.5)*
and you can even construct a colormap directly from any valid Matplotlib color
name with::
	
	colorlist(color('Aqua', 'name'), color('Gold', 'name')).LinearSegmentedColormap()

Some examples:

	* off-the-shelf Matplotlib colormap ('BuPu')
	* *cmap_lighten()*
	* *cmap_darken()*
	* *cmap_adjust()* used to rotate the hue
	* *cmap_adjust()* used to change the saturation
	* constructing an entirely new colormap using the Matplotlib color names 'Aqua'
	  and 'Gold' as endpoints

.. image:: https://dl.dropboxusercontent.com/u/35392962/colormap_demonstration.jpg
   :width: 683
   :height: 202

Looking for a set of easily distinguishable colors? You could rely on one of the
lists contained in *custom_colorsets*. Access to the color sets is through a 
statement such as::

	colorobject.custom_colorsets.sparse2dense

The included color sets are:

	* *cartercarter_6*: 6 high contrast colors from Carter and Carter (1982)
	* *greenarmytage_26*: 26 colors intended for use against a white background from
	  Green-Armytage (2010)
	* *tatarize_269*: 269 colors from the author of the `godsnotwheregodsnot 
	  <http://godsnotwheregodsnot.blogspot.ru/2013/11/kmeans-color-quantization-seeding.html>`_ 
	  blog

.. image:: https://dl.dropboxusercontent.com/u/35392962/discretecolors_demonstration.jpg
   :width: 683
   :height: 100


----------------
Installation
----------------
*colorobject* has only been tested in Python 2.7

Install through pip::

	$ pip install colorobject

Requires the following non-standard libraries:

     * *matplotlib*

Because preferred installation of matplotlib can vary depending on the operating system, 
matplotlib will not automatically be installed as a dependency. Instead, installation will 
raise an exception if matplotlib cannot be found in the pythonpath. In this case, please 
install matplotlib via your preferred method, most of which are explained `by matplotlib 
<http://matplotlib.org/users/installing.html>`_


-------------------
Bonus!
-------------------
Also included are a set of custom Matplotlib colormaps. These colormaps were designed so
that every color in the colormap would be distinguishable against a white background. Also,
the ordering of the colors from low to high are intended to be as intuitive as possible and
there are no sudden peaks in the lightness or hue. Access to the colormaps is through a
statement such as::

	colorobject.custom_colormaps.sparse2dense

The intended use for these colormaps is:

	* low2high: general
	* cool2hot: temperature or heat
	* deep2shallow: bathymetry maps
	* dirty2clean: environmental condition or degredation
	* sparse2dense: density maps

.. image:: https://dl.dropboxusercontent.com/u/35392962/custom_colormaps.jpg
   :width: 683
   :height: 168


--------------
Changelog
--------------
**0.8.1 (DECEMBER/02/2014)**
	* Moved custom color sets from module *discretecolors* to named tuple *custom_colorsets* in 
	  module *data*. Access is through the statement e.g. 
	  *colorobject.custom_colorsets.cartercarter_6*
	* Added custom color maps with named tuple *custom_colormaps* to module *data*. Access is
	  through the statement e.g. *colorobject.custom_colormaps.sparse2dense*

**0.8.0 (DECEMBER/01/2014)**

	* First release