Yayi
====


Image processing and mathematical morphology python bindings.


Yayi is a open-source image processing framework which particularly focuses on Mathematical Morphology operators. 
It is released under the very permissive Boost license. 

The core of Yayi is entirely written in C++, mainly using templatized code which enables a high level of 
genericity. It implements some of the main concepts of Mathematical Morphology into an efficient and proven design. 
Yayi aims at providing robust, efficient and flexible algorithms for image analysis, but also reference algorithms 
for Mathematical Morphology.

The python interface provides a simple way for using the main notions and functions of mathematical morphology. 
The export uses the boost.python framework.

The whole project uses `cmake`_ for building. Some bindings with `setup.py` are being developed in order to be able 
to just `pip install yayi`.

Installation
------------
Yayi needs `boost`_, `cmake`_ and a decent C++ compiler to build. You should install those tools in your system, preferably
using your package manager.

.. warning:: as soon as you build and install Yayi, Yayi becomes dependent on the `boost` package. If you upgrade `boost`
   to a new version, then it might break Yayi. As a matter of fact, python package management does not communicate
   with the /native/ package management of your operating system.  
   
.. _boost: http://www.boost.org

.. _cmake: http://www.cmake.org

.. note:: the interface is still a bit clumpsy and is about to change. Your feedbacks are welcome!

.. note:: some of the dependencies are shipped with Yayi directly, but on some platforms (Linux) the dependencies provided
          by the package manager are preferred.

Linux Ubuntu
~~~~~~~~~~~~
Ubuntu is shipped with its own package manager, and it is straightforward to install packages, though you
need administrative privileges.

To install the dependencies of Yayi, just type in a Terminal:

.. code:: shell

  sudo apt-get install boost, cmake, python-numpy, libjpeg8-dev, zlib1g-dev, libpng12-dev, libtiff4-dev
  sudo apt-get install libhdf5-dev


and then

.. code:: shell

  pip install Yayi==0.8.2dev


Then 

.. code:: python

   from Yayi.common import YAYI
   YAYI.IO.readPNG('my/png/file.png")
   
should work.


OSX
~~~
On OSX, a convenient package manager is `brew`_ 

.. _brew: http://brew.sh/

To install the dependencies, just type in a Terminal:

.. code:: shell

  brew install boost
  brew install cmake


and then

.. code:: shell

  pip install numpy
  pip install Yayi==0.8.2dev


Then 

.. code:: python

   from Yayi.common import YAYI
   YAYI.IO.readPNG('my/png/file.png")
   
should work.

.. note:: currently not using the HDF5 extensions.
