Yayi
====


Image processing and mathematical morphology python bindings.


Yayi is a open-source image processing framework which particularly focuses on Mathematical Morphology operators. 
It is released under the very permissive Boost licence. 

The core of Yayi is entirely written in C++, mainly using templatized code which enables a high level of 
genericity. It implements some of the main concepts of Mathematical Morphology into an efficient and proven design. 
Yayi aims at providing robust, efficient and flexible algorithms for image analysis, but also reference algorithms 
for Mathematical Morphology.

The python interface provides a simple way for using the main notions and functions of mathematical morphology. 
The export uses the boost.python framework.

The whole project uses cmake for building. Some bindings with `setup.py` are being developed in order to be able 
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

  pip install yayi


Then 

.. code:: python

   import Yayi
   
should work.