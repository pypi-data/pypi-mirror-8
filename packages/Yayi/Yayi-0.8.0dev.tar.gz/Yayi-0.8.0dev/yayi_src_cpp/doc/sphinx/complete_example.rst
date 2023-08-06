Examples of use
***************

We describe here some examples of use of the python bindings of Yayi. We hope you will find 
these snippets useful.


.. contents:: This page contains

.. note We suppose Yayi installed! See 

.. glossary::
    CO
    	Color utilities 

Venation network of a leaf image
================================

Description of the input images
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Segmenting the leaf and the background
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
As described in introduction, the images are quite easy to segment. To do that, we simply use the color
information of the leaf against the background. This is easily expressed in the HLS color space, where
the hue of the leaf should be (approximately) between -60 and 180, and 

Here is the code performing this action::

  import yayi.color_utilities as CO
  
  # transforming the image into the HLS l_1 color space
  im_hls = CO.HLS1FromRGB(im_color)
  
  # thresholding the hue component taking care of the circularity of the channel
  t_color_h = CO.ThresholdCircularDomainDegres(MU.colorGetChannel(im_hls, 0), -60, 120 + 60)
  
  # thresholding the saturation component
  t_color_s = MU.MThresh_255(MU.colorGetChannel(im_hls, 2), 10.0/255, 1)
  
  # taking the intersection of these two masks
  immask = MU.AAnd(t_color_h, t_color_s)


Now we the mask of the leaf. 