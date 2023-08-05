Layers
======
The first step in creating a map service with django-wms is to setup at least one WmsLayer sublcass. The WmsLayer class represents the `LAYER <http://mapserver.org/mapfile/layer.html>`_ directive from a mapserver map file. Each layer that will be offered as a service end point will be a subclass of WmsLayer.

Layer attributes
----------------

Spatial field
^^^^^^^^^^^^^
The main component of a WmsLayer is a django model that has at least one spatial field, which has to specified when sublclassing. For example
::

    # In myapp.wmslayers

    from wms.layers import WmsLayer
    from myapp.models import MySpatialModel

    class MyLayer(WmsLayer):
        model = MySpatialModel

The WmsLayer class auto-detects the first spatial field it can find in the model specified, for models with several spatial fields, the name of the spatial field can be specified explicitly using the ``geo_field_name`` attribute of the class.

Layer name
^^^^^^^^^^
By default, the spatial field name will be used as the layer's name. For a custom layer name, set the ``name`` attribute of the class.

Where clause
^^^^^^^^^^^^
This attribute can be used to preselect or filter the data from the model table that is shown on the layer. It can be used analogue to the where clause in a SQL select query such as ``SELECT FROM ... WHERE``. An example is ``where='quality>50'``.

Class item
^^^^^^^^^^
The ``class_item`` attribute can be used to specify a column of the specified model as a selector for coloring the map (analogue to the CLASSITEM directive in mapserver layers). To adopt coloring of the map according to the specified class_item field, the ``cartograpy`` attribute has to be specified, as described below.

Cartography
^^^^^^^^^^^
The cartography of a layer is defined as an array of dictionaries, where each dictionary has a *name*, a *expression* and a *color*. The name will be the name used in the legend when requested, the expression is a class expression for the ``class_item`` attribute that needs to be specified for the WmsLayer subclass (see above). The expression is SQL like, but not the same. The syntax is defined through the `MapServer Expressions <http://mapserver.org/mapfile/expressions.html>`_. Finally, the color used for this category can be specified as RGB with white spaces as separators (``255 0 0``) or as hexadecimal color (``#FF0000``). ::

    mycartograpy = [
        {
            'name': 'Category A',
            'expression': '1',
            'color': '0 0 255'
        },
        {
            'name': 'Category B',
            'expression': '2',
            'color': '255 0 0'
        }
    ]

    class MySpatialModel(models.Model):
        quality = models.FloatField()
        geom = models.PolygonField()

    class MyLayer(WmsLayer):
        model = MySpatialModel
        class_item = 'quality'
        where = 'quality > 0'
        cartograpy = mycartography

Vector layers
-------------
Supported spatial vector data types are Points, Lines, Polygons and MultiPolygons. Any of those field types are automatically detected in models or can be specifically set as explained above.

For points and polygons a set of predefined symbols can be used to render them (*circle*, *square*, *triangle*, *cross* and *diagonal*), for polygon a hatch fill symbology is available as well (*hatch*). To use those symbols, add the symbol attribute to the cartography array. For example ::

    mycartograpy = [
        {
            'name': 'Category A',
            'expression': '1',
            'color': '0 0 255',
            'symbol': 'hatch'
        }
    ]

Custom symbols can be added to display data, see `this tutorial <http://mapserver.org/mapfile/symbology/construction.html>`_ for guidance on symbol definitions. After creating custom mapscript symbols, the symbols can be added by subclassing the WmsSymbolSet class and setting an array of symbols in the ``custom_symbols`` attribute. When creating the WmsMap subclass, the custom symbol set needs to be specified as well. Below is a simple example ::

        import mapscript
        from wms.symbols import WmsSymbolSet

        symb = mapscript.symbolObj('v-line')
        symb.type = mapscript.MS_SYMBOL_VECTOR
        symb.filled = mapscript.MS_FALSE
        line = mapscript.lineObj()
        for pnt in [(0,0), (5, 10), (10, 0)]:
            line.add(mapscript.pointObj(pnt[0], pnt[1]))
        symb.setPoints(line)
        symb.sizex = 50
        symb.sizey = 50

        class MyCustomSymbols(WmsSymbolSet):
            custom_symbols = [symb]

        class MyWmsMap(maps.WmsMap):
            symbolset_class = MyCustomSymbols


Raster layers
-------------
Raster layers are supported if the `django-raster <https://pypi.python.org/pypi/django-raster/>`_ package is installed. The django-raster package allows loading raster files into django, which can then be served through map services with this package.

After uploading a rasterfile to the RasterLayer model, that specific raster layer can be filtered for using the rasterlayer_id or the rasterfile name. Below is an example for a layer using raster data from the RasterTile table, which is generated by the django-raster package through the RasterTile model. The cartography can be equal to the definition in the previous example above. ::
    
    class MyRasterLayer(WmsLayer):
        model = RasterTile
        where="filename=\\\'myrasterfile.tif\\\'"
        nodata = '0'
        cartography = mycartograpy
