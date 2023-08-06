#ifndef YAYI_IO_HPP__
#define YAYI_IO_HPP__

/*! @file
 *  @brief Global definition for the I/O library
 *
 */


#include <yayiCommon/common_config.hpp>
#include <yayiImageCore/include/yayiImageCore.hpp>



#ifdef YAYI_EXPORT_IO_
  #define YIO_ MODULE_EXPORT
#else
  #define YIO_ MODULE_IMPORT
#endif


namespace yayi
{

  namespace IO
  {

   /*!@defgroup io_grp IO
    * @brief Loading/saving image from/to disk
    *
    * @warning For all file I/O routines, the file names are encoded in the local charset. There is currently no handling of unicode file names.
    * @{
    */

    //!@brief Reads a PNG file
    YIO_ yaRC readPNG (const string_type &filename, IImage*& image);
    //!@brief Writes the image into the provided PNG file
    YIO_ yaRC writePNG(const string_type &filename, const IImage* const & image);

    //!@brief Reads a JPG file
    YIO_ yaRC readJPG (const string_type &filename, IImage*& image);
    //!@brief Writes the image into the provided JPG file
    YIO_ yaRC writeJPG(const string_type &filename, const IImage* const & image);

    /*!@brief Reads a RAW file
     *
     * For this type of file, the dimensions and the type of the image should be provided.
     * @warning the dimension of the image should be exactly the same as the one provided during the save.
     */
    YIO_ yaRC readRAW (const string_type &filename, const s_coordinate<0> &sizes, const type &image_type_, IImage* &out_image);

    /*!@brief Writes the image into the provided RAW file
     *
     * @note Multichannel images are saved in planar format (each channel saved separately), in order to remain compatible with some popular
     * viewers (eg <a href="http://rsbweb.nih.gov/ij/">ImageJ</a>).
     */
    YIO_ yaRC writeRAW(const string_type &filename, const IImage* const & image);

    //!@brief Writes the image into an EPS file (for integration in latex for instance).
    //!@note There is not EPS reading, this format is for export only, and provided for convenience (eg. inclusion of images in Latex).
    YIO_ yaRC writeEPS(const string_type &filename, IImage const * const & image);

    /*!@brief Reads TIFF images.
     *
     * @param filename the full name of the file to read.
     * @param image_index the index of the image to read within the tiff file (for multipage TIFF).
     * @param image the output image.
     * @return yaRC_ok if succeeded, an error code otherwise. If an error occurs, any intermediate allocation of the output image
     * is destroyed and image points to 0.
     *
     * @note The file name is encoded in locale charset.
     * @note The format that are supported are the following:
     *  - tile based or strip based compressed or not
     *  - grey level tiff:
     *    - integers 8, 16, 32, 64 bits (signed or not)
     *    - 32 and 64 bits floating point data types (16 bits unsupported)
     *  - colour level tiff, 3 or 4 channels (no complex), same level of support as for scalar formats.
     *  - compressed or not (legacy compressors included in libtiff 4.x)
     */
    YIO_ yaRC readTIFF(const string_type& filename, int image_index, IImage*& image);



    /*!@brief Write image in TIFF format
     *
     * The function is able to write any supported format of pixel, except the complex ones.
     * @note The file name is encoded in locale charset.
     * @note The compression used is zip based (lossless), with horizontal prediction for types different of 64 bits. 
     * @note The image is saved in tile format. 
     * @note There are no support of multipage TIFF support.
     * @warning Although TIFF is a widely used format, not all TIFF readers are able to properly interpret the file saved by this function.
     *  For instance, <a href="http://rsbweb.nih.gov/ij/">ImageJ</a> is unable to read tiles TIFFs, or TIFF compressed with zip. 
     * 
     *
     */
    YIO_ yaRC writeTIFF(const std::string &filename, const IImage * const & image);

    // Optional HDF5 Support
#ifdef YAYI_IO_HDF5_ENABLED__
    /*!@brief Reads a HDF5 file.
     *
     * An HDF5 file may contain several images of any dimension and any type. See <a href="http://www.hdfgroup.org/HDF5/">HDF5</a> web page for a thorough
     * presentation of the HDF5 format. The format is suitable for storing very large images, and particularly useful for images of dimensions greater or equal than 3.
     * The format is used in the scientific community, often for storing a small/large database of tables and images.
     *
     * @note The image name (within the image file) can be added to the command, in order to read a specific part of the HDF5 file.
     *
     * @param[in]  filename the full path to the file containing the image
     * @param[out] out_image the loaded image (if succeed)
     * @param[in]  image_name the image name to read within the file.
     */
    YIO_ yaRC readHDF5 (const string_type &filename, IImage* &out_image, const std::string &image_name = "yayi_image_1");

    /*!@brief Write an image into a HDF5 file
     *
     * @param[in] filename the full path to the file which will contain the image
     * @param[in] image    the image to save
     * @param[in] image_name the name of the image into which the "image" will be saved
     *
     * See @ref readHDF5 for more details on the format.
     * @see readHDF5
     */
    YIO_ yaRC writeHDF5(const string_type &filename, const IImage* const & image, const std::string &image_name = "yayi_image_1");
#endif


    //! @} //io_grp
  }
}

#endif

