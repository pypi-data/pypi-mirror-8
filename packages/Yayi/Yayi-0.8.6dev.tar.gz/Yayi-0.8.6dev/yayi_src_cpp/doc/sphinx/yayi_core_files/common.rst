Common
======
This module contains relevant structures and functions for manipulating data. These structures are either for coordinate manipulation,
relationship of structures (Graph), color information, etc.

   

Structures
----------

Data types
^^^^^^^^^^
Yayi handles a large amount of data types, where *handling* here mainly means the type of pixels supported for images. A data type is composed of
two fields:

* a :class:`compound type <YayiCommonPython.compound_type>`: this field says what the data is about, if it is :class:`scalar <YayiCommonPython.compound_type.c_scalar>`, 
  :class:`complex <YayiCommonPython.compound_type.c_complex>`, :class:`3 channels <YayiCommonPython.compound_type.c_3>`, 
  :class:`4 channels <YayiCommonPython.compound_type.c_4>`,
* a :class:`scalar type <YayiCommonPython.scalar_type>`: this is the scalar part of any compound data type. Hence *3 channels* data type can be 
  :class:`float <YayiCommonPython.scalar_type.s_float>`, 
  :class:`double <YayiCommonPython.scalar_type.s_double>`, :class:`uint8 <YayiCommonPython.scalar_type.s_ui8>` etc. 


Coordinates
^^^^^^^^^^^
Coordinates in Yayi are tuples of lists. The length of the sequence defines the dimension in with the coordinate is expressed. 
For instance, 2D coordinates and rectangles are defines like this::

  coord1 = (10, 20)
  coord2 = (30, 40)
  rect2D = YayiCommonPython.HyperRectangle(coord1, coord2)
  
The :class:`YayiCommonPython.HyperRectangle` structure is, as its name indicates, a rectangle (or bounding box) in any dimension. It is defined by its two extremal corners.
Some functions are available for manipulating coordinates and collection of coordinates:

* :func:`YayiCommonPython.AreSetOfPointsEqual`



Graphs
^^^^^^
:class:`Graphs <YayiCommonPython.Graph>` are made of vertices and undirected edges (current implementation, may change in the future). The graphs in Yayi cannot 
contain parallel edges. A property can be associated to each vertex and each :class:`Edge <YayiCommonPython.Edge>`. 

Graphs in Yayi are used for manipulating regions in images and their adjacencies. 


Color manipulation
^^^^^^^^^^^^^^^^^^
Yayi can handle different color spaces. The color spaces are encoded in a particular structure: :class:`colorspace <YayiCommonPython.colorspace>`.

* :func:`YayiCommonPython.blackbody_radiation`
* :func:`YayiCommonPython.blackbody_radiation_normalized`
* :class:`YayiCommonPython.colorspace`

The color space transformations are pixel-to-pixel transformations that are available in the :doc:`pixel_processing` module.


Histograms
^^^^^^^^^^
Histograms in Yayi are handled through dictionaries. 

Examples
--------

Coordinates
^^^^^^^^^^^

The following code generates randomly one set of coordinates and creates a second bigger set containing a permutation of the first set. 
Then, sets are tested for equality::
  
  # importing the module containing the utilities
  from Yayi.YAYI import COM as YCOM
  import random
  
  # generates random coordinates
  set1 = [(random.randint(0, 20), random.randint(0, 30)) for i in range(30)]
  
  # generates a random sample
  # we should have len(set(set1) - set(set2)) == 0
  set2 = random.sample(set1, len(set1))
  
  # we add existing points, we still have len(set(set1) - set(set2)) == 0
  set2.extend(random.sample(set1, len(set1)/3))
  
  # testing if the two previous sets contain the same elements
  if(YCOM.AreSetOfPointsEqual(set1, set2)):
    print "The two sets contains the same points"
  set2.append(YCOM.Transpose(set2[-1]))
  if(not YCOM.AreSetOfPointsEqual(set1, set2)):
    print "Sets are different"
    

Graphs
^^^^^^


Reference
---------

.. automodule:: YayiCommonPython
    :members:
    :undoc-members: