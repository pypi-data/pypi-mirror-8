
#include <yayiReconstructionPython/reconstruction_python.hpp>
#include <yayiReconstruction/highlevel_minima_maxima.hpp>

using namespace bpy;

void declare_highlevel_minima_maxima() {
  def("HMinima",
      &yayi::hlmm::image_h_minima,
      bpy::args("im_source","SE","variant","im_destination"),
      "Performs the h-minima transformation, it suppresses all minima whose depth is above a given level threshold (variant).");

  def("HMaxima",
      &yayi::hlmm::image_h_maxima,
      bpy::args("im_source","SE","variant","im_destination"),
      "Performs the h-maxima transformation, it suppresses all maxima whose depth is below a given level threshold (variant).");

  def("HConvex",
      &yayi::hlmm::image_h_convex,
      bpy::args("im_source","SE","variant","im_destination"),
      "Performs the h-convex transformation, abs(h-maxima(im_source) - im_source).");

  def("HConcave",
      &yayi::hlmm::image_h_concave,
      bpy::args("im_source","SE","variant","im_destination"),
      "Performs the h-concave transformation, abs(h-minima(im_source) - im_source).");

  def("PseudoDynamicOpening",
      &yayi::hlmm::image_pseudo_dynamic_opening,
      bpy::args("im_source","SE","variant","im_destination"),
      "Performs the PseudoDynamiOpening transformation, similar to h-maxima but restores the dynamic of remaining maxima");

  def("PseudoDynamicClosing",
      &yayi::hlmm::image_pseudo_dynamic_closing,
      bpy::args("im_source","SE","variant","im_destination"),
      "Performs the PseudoDynamiClosing transformation, similar to h-minima but restores the dynamic of remaining minima");

}
