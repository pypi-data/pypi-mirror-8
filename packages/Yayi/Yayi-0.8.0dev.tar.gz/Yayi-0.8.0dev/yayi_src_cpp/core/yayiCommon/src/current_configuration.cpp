

#include <yayiCommon/include/current_configuration.hpp>
#include <yayiCommon/include/common_string_utilities.hpp>

namespace yayi
{

  extern const std::string yayi_revision;
  extern const std::string yayi_revision_date;

  std::string current_build_version()
  {
    return yayi_revision;
  }

  std::tm current_build_date()
  {
    static const std::tm date = from_string_to_date(yayi_revision_date);
    return date;
  }


  static unsigned int processor_unit = 2;
  unsigned int& NbProcessorUnit() {
    return processor_unit;
  }
  
  
  bool is_big_endian_helper()
  {
    yaUINT16 word = 0x0001;
    yaUINT8 *byte = (yaUINT8 *) &word;
    return (byte[0] == 0);
  }
  const bool is_big_endian = is_big_endian_helper();
  
}

