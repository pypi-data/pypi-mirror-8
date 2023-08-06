Python modules
**************

.. toctree::
   :maxdepth: 2

   Image treatment <image_utilities>
   Color processing <color_utilities>
   Morphological operators utilities <morpho_utilities>
   Drawing utilities <draw>



Yayi comes with several scripts that should ease its use. The functions contained in these scripts often do nothing but
wrapping corresponding Yayi (C++) functions in a way suitable to scripting. The main difference lies in the fact that, most
often, the functions return a new image containing the desired result, which aleviates the burden of allocating each output.

Hence, technically speaking, these two snippets perform the same action on the input image::

  im1 = YAYI.CORE.GetSameImageOf(im, Ytype(c_scalar, im.DynamicType().s_type))
  YAYI.PIX.CopyOneChannel(im, 0, im1)

and::
  
  #from Yayi.color_utilities import colorGetChannel
  im1 = colorGetChannel(im, 0)
  
The nice thing with these functions is that they can be chained::

  from Yayi.draw import overlay
  from Yayi.color_utilities import colorSplitTo3
  from Yayi.morpho_utilities import MDilate
  im_overlay = overlay(im, MDilate( colorSplitTo3(im)[1], 2) )

.. contents:: This page contains


