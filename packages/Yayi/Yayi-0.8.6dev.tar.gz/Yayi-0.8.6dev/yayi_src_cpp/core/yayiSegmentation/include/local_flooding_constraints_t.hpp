#ifndef YAYI_SEGMENTATION_LOCAL_FLOODING_CONSTRAINTS_HPP__
#define YAYI_SEGMENTATION_LOCAL_FLOODING_CONSTRAINTS_HPP__

namespace yayi 
{
  namespace sgt
  {
/*!
 * @addtogroup seg_details_grp
 *
 *@{
 */     
    //! Dummy empty structure. Only two specialization are defined
    template <class t_gradient, class t_external_modifier, class SE>
    struct s_constraint_function_area;

    //! Area constraint functor for ImageSE<UINT8>
    template <class t_gradient, class t_external_modifier>
    struct s_constraint_function_area<t_gradient, t_external_modifier, ImageSE<UINT8> >
    {
    public:
      typedef yaF_double result_type;
      typedef ImageSE<UINT8> SE;
      
      // magic magic, yeah yeah yeah
      enum e_easy_update {easy_update = true};


    public:

      s_constraint_function_area(const SE& im) : ui16_count(0), d_factor(0.)
      {
        // compute the area of the image SE:
        typename SE::const_iterator it = im.begin(), ite = im.end();
        for(; it != ite; ++it)
        {
          if(*it != DataTraits<typename SE::value_type>::default_value::background()) ui16_count ++;
        }

        d_factor = 2. / static_cast<result_type>(ui16_count);
        ui16_count = 0;
      }

      void reset()
      {
        ui16_count = 0;
      }
      
      yaRC center(const offset_t off)
      {
        // toujours la meme surface, donc pas de problème ici
        return yaRC_ok;
      }
      
      void push_new_point(const t_gradient /* point_initial_value */, const offset_t offset_neighbor)
      {
        ui16_count++;
      }
      
      result_type operator()(const t_gradient center_initial_value, const t_external_modifier center_alpha_value) const
      {
        result_type res2 = ui16_count;
        res2 *= d_factor;
        res2 -= 1;
        res2 *= -center_alpha_value;
        res2 += static_cast<result_type>(center_initial_value);
        return res2;
      }
      result_type update(const t_gradient /*center_initial_value*/, const t_external_modifier center_alpha_value) const
      {
        return -center_alpha_value * d_factor;
      }

    private:
      result_type d_factor;
      yaUINT16    ui16_count;
    };
    
    
    
    //! Area constraint functor for map_se
    template <class t_gradient, class t_external_modifier, class SE_t, class t_map_image>
    struct s_constraint_function_area<t_gradient, t_external_modifier, map_se<t_map_image, SE_t> >
    {
    public:
      typedef yaF_double result_type;
      typedef SE_t SE;
      typedef map_se<t_map_image, SE_t> t_map_se;
      
      // magic magic, yeah yeah yeah
      enum e_easy_update {easy_update = true};

    private:
      typedef std::map<typename t_map_se::map_image_type::value_type, result_type> map_factors_type;


    public:

      s_constraint_function_area(const t_map_se& map) : ui16_count(0), map_factors(), d_factor_current(0), map_se_internal_ref(map)
      {

        for(typename t_map_se::se_association_type::const_iterator it_ = map_se_internal_ref.m_se_association.begin(), ite_ = map_se_internal_ref.m_se_association.end();
          it_ != ite_;
          ++it_)
        {
          // compute the area of the image SE:
          typename SE::const_iterator it = (it_->second).begin(), ite = (it_->second).end();
          for(; it != ite; ++it)
          {
            if(*it != typename SE::value_type(0)) ui16_count ++;
          }

          //std::cout << "area " << ui16_count << std::endl;
          map_factors[it_->first] = 2. / static_cast<result_type>(ui16_count);
          ui16_count = 0;					
        }
      }

      void reset()
      {
        ui16_count = 0;
        d_factor_current = 0.;
      }
      yaRC center(const offset_t off)
      {
        d_factor_current = map_factors[map_se_internal_ref.MapImage().pixel(off)];
        return yaRC_ok;
      }
      void push_new_point(const t_gradient /* point_initial_value */, const offset_t /*o*/)
      {
        ui16_count++;
      }
      result_type operator()(const t_gradient center_initial_value, const t_external_modifier center_alpha_value) const
      {
        result_type res2 = ui16_count;
        res2 *= d_factor_current;
        res2 -= 1;
        res2 *= -center_alpha_value;
        res2 += static_cast<result_type>(center_initial_value);
        return res2;
      }
      result_type update(const t_gradient /*center_initial_value*/, const t_external_modifier center_alpha_value) const
      {
        return -center_alpha_value * d_factor_current;
      }

    private:
      map_factors_type		map_factors;
      result_type         d_factor_current;
      yaUINT16            ui16_count;
      const t_map_se			&map_se_internal_ref;	// bouououou pas boooooo
    };





    
    //! Mean constraint functor
    template <class t_gradient, class t_external_modifier, class SE>
    struct s_constraint_function_mean
    {
    public:
      typedef yaF_double result_type;

      // magic magic, yeah yeah yeah
      enum e_easy_update {easy_update = false};

      s_constraint_function_mean(const SE&):d_acc(0.), ui16_count(0){}

      void reset()
      {
        ui16_count = 0;
        d_acc = 0.;
      }
      yaRC center(const offset_t off)
      {
        return yaRC_ok;
      }
      
      void push_new_point(const t_gradient point_initial_value, const offset_t offset_neighbor)
      {
        ui16_count++;
        d_acc += point_initial_value;
      }
      
      result_type operator()(const t_gradient center_initial_value, const t_external_modifier /*center_alpha_value*/) const
      {
        if(ui16_count == 0) return center_initial_value;
        return d_acc / ui16_count;
      }
      result_type update(const t_gradient /*center_initial_value*/, const t_external_modifier /*center_alpha_value*/) const
      {
        throw yaException("s_constraint_function_mean::update : should never be called, check your function");
      }

    private:
      result_type d_acc;
      yaUINT16 ui16_count;
    };

//! @} doxygroup: seg_details_grp
      
  }
}

#endif /* YAYI_SEGMENTATION_LOCAL_FLOODING_CONSTRAINTS_HPP__ */
