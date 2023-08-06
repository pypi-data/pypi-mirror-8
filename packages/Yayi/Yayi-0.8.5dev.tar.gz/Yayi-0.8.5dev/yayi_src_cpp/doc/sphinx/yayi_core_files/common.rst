Common
======
This module contains some useful structures, classes and functions. 

   

Structures
----------


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
Graphs are made of vertices and undirected edges (current implementation, may change in the future). The graph cannot contain parallel edges. A property can be associated to each vertex and each edge. 

Examples
--------

The following code generates randomly one set of coordinates and creates a second bigger set containing a permutation of the first set. Then, sets are tested for equality::
  
  # importing the module containing the utilities
  import YayiCommonPython as YCOM
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
    
    
Reference
---------

.. automodule:: YayiCommonPython
    :members:
    :undoc-members: