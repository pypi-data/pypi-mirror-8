Vector Tile Tools
=================
A set of classes for managing tiles of geospatial vector data

![Build Status](https://travis-ci.org/SkyTruth/vectortile.svg)


Installation and Unittests
--------------------------
Install via pip:

    pip install vectortile

Source:
    
    $ git clone https://github.com/SkyTruth/vectortile.git
    $ cd vectortile
    $ pip install -r requirements.txt
    $ nosetests
    $ python setup.py install


TypedMatrix
-----------
TypedMatrix is a binary coded format optimized for delivering large amounts of
tabular data from a web server to a javascript client without the need for
parsing in javascript on the client side.

The vectortile.TypedMatrix module provides functions to read and write
typed-matrix formatted strings.


### Format Details ###
A TypedMatrix is a packed 2 dimensional array of typed values suitable for
typecasting to a set of javascript arrays.  Currently two fundamental data
types are supported:

- Int32
- Float32

Special handling is provided for converting datetime values to Float32.  The
format includes a header containing a json object, which can contain arbitrary
content.  The header must contain at least:

- length: indicated the number of rows in the data section
- cols: an array of column definitions.  The length of this array indicates the number of columns in each row

For example, a TypedMatrix with 2 rows and 3 columns:

    {
        'length': 2,
        'cols': [
            {
                'type': 'Float32',
                'name': 'float'
            },
            {
                'type': 'Int32',
                'name': 'int'
            },
            {
                'type': 'Float32',
                'name': 'timestamp'
            }
        ]
    }


### Usage Examples ###

    >>> from vectortile import TypedMatrix
    >>> from datetime import datetime
    >>> from pprint import pprint

    # Create two rows of 3 columns each: int, float and datetime
    >>> data = [{'int':1, 'float':1.0, 'timestamp': datetime(2014,1,1)}]
    >>> data.append ({'int':2, 'float':2.0, 'timestamp':datetime(2014,1,2)})
    >>> t_str = TypedMatrix.pack(data)

    # Typedmatrix is now coded as a binary string, packed row-wise
    >>> t_str
    'tmtx\x01\x00\x00\x00r\x89\x00\x00\x00{"length": 2, "cols": [{"type": "Float32", "name": "float"}, {"type": "Int32", "name": "int"}, {"type": "Float32", "name": "timestamp"}]}\x00\x00\x80?\x01\x00\x00\x00\x8d\xa5\xa1S\x00\x00\x00@\x02\x00\x00\x00 \xa8\xa1S'
    
    >>> header, data = TypedMatrix.unpack(t_str)
    >>> pprint(header)
    {
        'cols': [
            {
                'name': 'float',
                'type': 'Float32'
            },
            {
                'name': 'int',
                'type': 'Int32'
            },
            {
                'name': 'timestamp',
                'type': 'Float32'
            }
        ],
        'length': 2
    }
    
    >>> pprint(data)
    [
        {
            'float': 1.0,
            'int': 1,
            'timestamp': 1388534431744.0
        },
        {
            'float': 2.0,
            'int': 2,
            'timestamp': 1388620808192.0
        }
    ]

    # Pack data column-wise
    >>> TypedMatrix.pack(data,orientation='columnwise')
    'tmtx\x01\x00\x00\x00c\x89\x00\x00\x00{"length": 2, "cols": [{"type": "Float32", "name": "float"}, {"type": "Int32", "name": "int"}, {"type": "Float32", "name": "timestamp"}]}\x00\x00\x80?\x00\x00\x00@\x01\x00\x00\x00\x02\x00\x00\x00\x8d\xa5\xa1S \xa8\xa1S'
    
    >>> header, data = TypedMatrix.unpack(t_str)
    >>> pprint(header)
    {
        'cols': [
            {
                'name': 'float',
                'type': 'Float32'
            },
            {
                'name': 'int',
                'type': 'Int32'
            },
            {
                'name': 'timestamp',
                'type': 'Float32'
            }
        ],
        'length': 2
    }
    
    >>> pprint(data)
    [
        {
            'float': 1.0,
            'int': 1,
            'timestamp': 1388534431744.0
        },
        {
            'float': 2.0,
            'int': 2,
            'timestamp': 1388620808192.0
        }
    ]


### Javascript Example ###
See [data-visualization-tools](https://github.com/SkyTruth/data-visualization-tools)
