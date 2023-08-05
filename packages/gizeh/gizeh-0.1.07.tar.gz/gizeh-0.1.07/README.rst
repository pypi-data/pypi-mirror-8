.. image:: https://raw.githubusercontent.com/Zulko/gizeh/master/logo.jpeg
   :alt: [logo]
   :align: center

Gizeh - Cairo for tourists
===========================

Gizeh is a Python library for vector graphics:
::

    # Let's draw a red circle !
    import gizeh
    surface = gizeh.Surface(width=320, height=260) # in pixels
    circle = gizeh.circle(r=30, xy= [40,40], fill=(1,0,0))
    circle.draw(surface) # draw the circle on the surface
    surface.write_to_png("circle.png") # export the surface as a PNG

You can see examples of Gizeh in action (combined with MoviePy) in `this blog post <http://zulko.github.io/blog/2014/09/20/vector-animations-with-python/>`_.

Gizeh is written on top of the module `cairocffi`, which is a Python binding of the popular C library Cairo. Cairo is powerful, but difficult to learn and use. Gizeh implements a few classes on top of Cairo that make it more intuitive.

Installation
--------------

Gizeh should work on any platform and with python 2 and 3. If you have difficulties installing it, you can ask for help on Github.
Gizeh depends on the Python packages `cairocffi` and `Numpy`. They will both be automatically installed (if they aren't already) during the installation of Gizeh.

**From the source:** Gizeh can be installed by unzipping the source code in some directory and using this command in the same directory:
::

    (sudo) python setup.py install

**Method with pip:** Alternatively, you can install Gizeh directly from the Python Package Index with this command:
::

    (sudo) pip install gizeh

This method may fail if ``ez_setup`` is not installed on your computer. In this case install ``ez_setup`` first, with ::
    
    (sudo) pip install ez_setup

Contribute !
-------------

Gizeh is an open-source software written by Zulko_ and released under the MIT licence. The project is hosted on Github_.
Everyone is welcome to contribute !


User Guide
-------------

This guide, along with the examples in the `gizeh/examples` folder, should give you everything you need to get started. To go further, read the function docstrings.

Surfaces
~~~~~~~~

A Surface is a rectangle of fixed dimensions (in pixels), on which you will draw elements, and that you can save or export as an image:
::

    import gizeh
    
    # initialize surface
    surface = gizeh.Surface(width=320, height=260) # in pixels

    # Now make a shape and draw it on the surface
    circle = gizeh.circle(r=30, xy= [40,40], fill=(1,1,1))
    circle.draw(surface)

    # Now export the surface
    surface.get_npimage() # returns a (width x height x 3) numpy array
    surface.write_to_png("circle.png") # doesn't require scipy, but image is flipped
    


Elements
~~~~~~~~~

Basic elements are circles, rectangles, lines, texts, etc., that you can draw on a surface using `my_element.draw(surface)`. You can specify the properties and coordinates of these elements at creation time:

- `xy` : coordinates of the center of the object. (0,0), which is the defaut, corresponds to the bottom left corner of the final picture.
- `angle` : angle (in radians) of the rotation of the element around its center `xy`.
- `fill` : what will fill the element (default is no fill). Can be a color (R,G,B), a color gradient, an image, etc. See section below.
- `stroke` : What will fill the element's contour. Same rules as for `fill`.
- `stroke_width` : the width (in pixels) of the element's contour. Default is 0 (no stroke).

Examples of elements:
::

    Pi = 3.14
    circ = gizeh.circle(r=30, xy=(50,50), fill=(1,1,1))
    rect = gizeh.rectangle(lx=60.3, ly=45, xy=(60,70), fill=(0,1,0), angle=Pi/8)
    sqr = gizeh.square(l=20, stroke=(1,1,1), stroke_width= 1.5)
    arc = gizeh.arc(r=20, a1=Pi/4, a2=3*Pi/4, fill=(1,1,1))
    text = gizeh.text("Hello world", fontfamily="Impact",  fontsize=40,
                      fill=(1,1,1), xy=(100,100), angle=Pi/12)
    polygon = gizeh.polygon(r=40, n=5, angle=np.pi/4, xy=[40,50], fill=(1,0,1))
    line = gizeh.polyline(points=[(0,0), (20,30), (40,40), (0,10)], stroke_width=3,
                         stroke=(1,0,0), fill=(0,1,0))

Fill and stroke
----------------

When you make a shape, the `fill` and `stroke` parameters can be one of the following:

- A RGB color of the form (r,g,b) where each element is comprised between 0 and 1 (1 is 100%).
- A RGBA colot of the form (r,g,b,a), where `a` is comprised between 0 (totally transparent) and 1 (totally opaque).
- A gizeh.ColorGradient (see the docstring).
- A gizeh.ImagePattern, i.e. an image (see the docstring).
- A numpy array representing a RGB or RGBA image (not implemented yet).
- A PNG image file (not implemented yet).


Transformations
~~~~~~~~~~~~~~~~

Any element can be tranformed (translated, rotated or scaled). All transformations are *outplace*: they do not modify the original element, they create a modified version of it.

Examples:
::

    square_1 = gizeh.square(l=20, xy = [30,35], fill=(1,0,0))
    square_2 = square_1.rotate(Pi/8) # rotation around [0,0] by default
    square_3 = square_2.rotate(Pi/4, center=[10,15]) # rotation around a center
    square_4 = square_1.scale(2) # two times bigger
    square_5 = square1.scale(sx=2, sy=3) # width times 2, height times 3
    square_6 = square_1.scale(2, center=[30,30]) # zoom: scales around a center
    square_7 = square_1.translate(xy=[5,15]) # translation


Groups
~~~~~~~

A Group is a collection of elements which will be transformed and drawn together. The elements can be a basic element (square, circle...) or even groups.

Examples:
::

    square = gizeh.square(l=20, fill=(1,0,0), xy=(40,40))
    circle = gizeh.circle(r=20, fill=(1,2,0), xy=(50,30))
    group_1 = gizeh.Group([square, circle])
    group_2 = group.translate(xy=[30,30]).rotate(Pi/4)
    group_3 = gizeh.Group([circle, group_1])
    
    surface = gizeh.Surface(width=300,height=200)
    group.draw(surface)
    group_1.draw(surface)
    group_2.draw(surface)
    group_3.draw(surface)
    surface.write_to_png("my_masterwork.png")


That's all folks !
~~~~~~~~~~~~~~~~~~~

That's about all there is to know.
To go further, see the examples in the `examples` folder or (wishful thinking) on the Web.

.. _Zulko : https://github.com/Zulko
.. _Github: https://github.com/Zulko/gizeh
