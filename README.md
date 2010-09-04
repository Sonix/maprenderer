MAP RENDERER
============

Renders a (big) Map of the specified region into a .png file

Usage
-----

    python maprenderer.py *Options*

### Options

* -min *width* *height* - specifies a minimum width and height for the resulting picture. Resulting size will usually be bigger depending on the area to render
* - rect *topleft* *bottomright* - specifies the rectangular area to render. Each has to be a Latitude/Longitude-pair in decimal
* -o *file* - sets the output file


Example: 
    python maprenderer.py -min 1024 1024 -rect 54.196994 12.014923 54.054954 12.194138 

.. renders a map of Rostock with at least 1024x1024 pixels