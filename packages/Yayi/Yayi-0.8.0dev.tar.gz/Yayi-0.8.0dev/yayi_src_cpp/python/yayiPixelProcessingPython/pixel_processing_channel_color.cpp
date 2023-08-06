#include <yayiPixelProcessingPython/pixelprocessing_python.hpp>


#include <yayiPixelProcessing/image_channels_process.hpp>
#include <yayiPixelProcessing/image_color_process.hpp>


using namespace bpy;

void declare_channel_color() {

  def("CopyOneChannelIntoAnother",
    &yayi::copy_one_channel_to_another,
    args("im_source", "channel_input", "channel_output", "im_destination"),
    "Copy the channel channel_input of the first image into the channel channel_output of the second image");

  def("CopyOneChannel",
    &yayi::copy_one_channel,
    args("im_source", "channel_input", "im_destination"),
    "Copy the channel channel_input of the first image into the second (scalar) image");
    
  def("CopyIntoChannel",
    &yayi::copy_to_channel,
    args("im_source", "channel_output", "im_destination"),
    "Copy the input image (im_source) into the specified channel (channel_output) of the output image (im_destination)");

  def("CopySplitChannels",
    &yayi::copy_split_channels,
    args("im_source", "channel1_out", "channel2_out", "channel3_out"),
    "Copy each channel of the input image into the output images");

  def("CopyComposeChannels",
    &yayi::copy_compose_channels,
    args("im_source1", "im_source2", "im_source3", "im_out"),
    "Copy each image pixel into a channel of the output image (in the same order as provided)");


  def("ExtractModulusArgument",
    &yayi::extract_modulus_argument,
    args("imin", "im_modulus", "im_argument"),
    "Extracts the polar (modulus and argument) information from a complex image");
  def("ComposeFromModulusArgument",
    &yayi::compose_from_modulus_argument,
    args("im_modulus", "im_argument", "imout"),
    "Fills a complex image from its polar (modulus and argument) representation");




  def("color_RGB_to_HLS_l1",
    &yayi::color_RGB_to_HLS_l1,
    args("im_source", "im_destination"),
    "Transforms a color image in RGB colour space to a colour image in HLS (l1) colour space");
  def("color_HLS_l1_to_RGB",
    &yayi::color_HLS_l1_to_RGB,
    args("im_source", "im_destination"),
    "Transforms a color image in HLS (l1) colour space to a colour image in RGB colour space");

  def("color_RGB_to_L601",
    &yayi::color_RGB_to_L601,
    args("im_source", "im_destination"),
    "Transforms a color image in RGB into a luminosity image, following the Rec601 definition");
  def("color_RGB_to_L709",
    &yayi::color_RGB_to_L709,
    args("im_source", "im_destination"),
    "Transforms a color image in RGB into a luminosity image, following the Rec709 definition");

  def("color_RGB_to_YUV",
    &yayi::color_RGB_to_YUV,
    args("im_source", "im_destination"),
    "Transforms a color image in RGB colour space to a colour image in YUV colour space");
  def("color_YUV_to_RGB",
    &yayi::color_YUV_to_RGB,
    args("im_source", "im_destination"),
    "Transforms a color image in YUV colour space to a colour image in RGB colour space");





  def("color_CIERGB_to_XYZ_refWE",
    &yayi::color_CIERGB_to_XYZ_refWE,
    args("im_source", "im_destination"),
    "Transforms a color image in RGB colour space to a colour image in XYZ colour space, assuming "
    "the RGB space is CIE-RGB (reference white E, CIE rgb primaries, gamma 2.2)");
  def("color_XYZ_to_CIERGB_refWE",
    &yayi::color_XYZ_to_CIERGB_refWE,
    args("im_source", "im_destination"),
    "Transforms a color image in XYZ colour space to a colour image in RGB colour space, assuming "
    "the RGB space is CIE-RGB (reference white E, CIE rgb primaries, gamma 2.2)");

  def("color_AdobeRGB_to_XYZ_refWD65",
    &yayi::color_AdobeRGB_to_XYZ_refWD65,
    args("im_source", "im_destination"),
    "Transforms a color image in RGB colour space to a colour image in XYZ colour space, assuming "
    "the RGB space is AdobeRGB (reference white D65, AdobeRGB rgb primaries, gamma 2.2)");
  def("color_XYZ_to_AdobeRGB_refWD65",
    &yayi::color_XYZ_to_AdobeRGB_refWD65,
    args("im_source", "im_destination"),
    "Transforms a color image in XYZ colour space to a colour image in RGB colour space, assuming "
    "the RGB space is AdobeRGB (reference white D65, AdobeRGB rgb primaries, gamma 2.2)");

  def("color_sRGB_to_XYZ_refWD65",
    &yayi::color_sRGB_to_XYZ_refWD65,
    args("im_source", "im_destination"),
    "Transforms a color image in RGB colour space to a colour image in XYZ colour space, assuming "
    "the RGB space is sRGB (reference white D65, CIE rgb primaries, gamma 2.4, specific linearising)");
  def("color_XYZ_to_sRGB_refWD65",
    &yayi::color_XYZ_to_sRGB_refWD65,
    args("im_source", "im_destination"),
    "Transforms a color image in XYZ colour space to a colour image in RGB colour space, assuming "
    "the RGB space is sRGB (reference white D65, CIE rgb primaries, gamma 2.4, specific linearising)");



  def("color_XYZ_to_LAB_refWE",
    &yayi::color_XYZ_to_LAB_refWE,
    args("im_source", "im_destination"),
    "Transforms a color image in XYZ colour space to a colour image in LAB colour space, using 'E' as reference white.");
  def("color_LAB_to_XYZ_refWE",
    &yayi::color_LAB_to_XYZ_refWE,
    args("im_source", "im_destination"),
    "Transforms a color image in LAB colour space to a colour image in XYZ colour space, using 'E' as reference white.");

  def("color_XYZ_to_LAB_refWA",
    &yayi::color_XYZ_to_LAB_refWA,
    args("im_source", "im_destination"),
    "Transforms a color image in XYZ colour space to a colour image in LAB colour space, using 'A' as reference white.");
  def("color_LAB_to_XYZ_refWA",
    &yayi::color_LAB_to_XYZ_refWA,
    args("im_source", "im_destination"),
    "Transforms a color image in LAB colour space to a colour image in XYZ colour space, using 'A' as reference white.");

  def("color_XYZ_to_LAB_refWD65",
    &yayi::color_XYZ_to_LAB_refWD65,
    args("im_source", "im_destination"),
    "Transforms a color image in XYZ colour space to a colour image in LAB colour space, using 'D65' as reference white.");
  def("color_LAB_to_XYZ_refWD65",
    &yayi::color_LAB_to_XYZ_refWD65,
    args("im_source", "im_destination"),
    "Transforms a color image in LAB colour space to a colour image in XYZ colour space, using 'D65' as reference white.");

  def("color_XYZ_to_LAB_refWD75",
    &yayi::color_XYZ_to_LAB_refWD75,
    args("im_source", "im_destination"),
    "Transforms a color image in XYZ colour space to a colour image in LAB colour space, using 'D75' as reference white.");
  def("color_LAB_to_XYZ_refWD75",
    &yayi::color_LAB_to_XYZ_refWD75,
    args("im_source", "im_destination"),
    "Transforms a color image in LAB colour space to a colour image in XYZ colour space, using 'D75' as reference white.");

}

