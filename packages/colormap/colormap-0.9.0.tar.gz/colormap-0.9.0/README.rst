#############################
COLORMAP documentation
#############################

.. image:: https://badge.fury.io/py/colormap.svg
    :target: https://pypi.python.org/pypi/colormap

.. image:: https://pypip.in/d/colormap/badge.png
    target: https://crate.io/packages/colormap/

.. image:: https://secure.travis-ci.org/cokelaer/colormap.png
    :target: http://travis-ci.org/cokelaer/colormap

.. image:: https://coveralls.io/repos/cokelaer/colormap/badge.png?branch=master 
    :target: https://coveralls.io/r/cokelaer/colormap?branch=master 

.. image:: https://landscape.io/github/cokelaer/colormap/master/landscape.png
    :target: https://landscape.io/github/cokelaer/colormap/master

.. image:: https://badge.waffle.io/cokelaer/colormap.png?label=ready&title=Ready 
    :target: https://waffle.io/cokelaer/colormap


Compatible with Python 2.7, 3.3, 3.4


What is it ?
################

**colormap** package provides simple utilities to convert colors between
RGB, HEX, HLS, HUV and a class to easily build colormaps for matplotlib.


Installation
###################

::

    pip install colormap

Example
##########

Create your own colormap from red to green colors with intermediate color as
whitish (diverging map from red to green)::

    c = Colormap()
    mycmap = c.cmap( {'red':[1,1,0], 'green':[0,1,.39], 'blue':[0,1,0]})
    cmap = c.test_colormap(mycmap)

See user guide for details.


