#ifndef YAYI_VISCOUS_SEGMENTATION_HPP__
#define YAYI_VISCOUS_SEGMENTATION_HPP__

/*!@file
 * This file defines the viscous watershed as defined in my PhD thesis
 * @author Raffi Enficiaud
 */

#include <Yayi/core/yayiSegmentation/yayiSegmentation.hpp>
#include <Yayi/core/yayiPixelProcessing/include/image_constant_T.hpp>
#include <Yayi/core/yayiCommon/common_priority_queues.hpp>
#include <Yayi/core/yayiPixelProcessing/include/image_copy_T.hpp>
#include <Yayi/core/yayiStructuringElement/include/yayiRuntimeStructuringElement_hexagon_t.hpp>
#include <Yayi/core/yayiStructuringElement/include/yayiRuntimeNeighborhood_t.hpp>
#include <Yayi/core/yayiStructuringElement/include/yayiNeighborhoodStrategy_t.hpp>
#include <Yayi/core/yayiCommon/common_labels.hpp>
namespace yayi 
{
  namespace sgt
  {
/*!
 * @addtogroup seg_details_grp
 *
 *@{
 */


			//! Utility structure for choosing the points of the same label as the center one
			//! Only strongly labelled points are counted
			template <class t_value>
      struct s_filter_point_same_label_done
			{

				/*! Main filter : points are strongly labelled and of the same label
				 * @param value_center label of the center point
				 * @param value_neighbor label of the neighbor point
				 * @param label_neighbor state of the neighbor point
				 */
				bool operator()(
					const t_value value_center, const Label /*label_center*/,
					const t_value value_neighbor, const Label label_neighbor) const throw()
				{
					return (value_neighbor == value_center) && (label_neighbor == labelDone);
				}

				/*! Update filter : points are of the same temporary label and in the queued state
				 * @param value_center label of the center point
				 * @param value_neighbor label of the neighbor point
				 * @param label_neighbor state of the neighbor point
				 */
				bool neighbor_need_update(
					const t_value value_center, const Label /*label_center*/,
					const t_value value_neighbor, const Label label_neighbor) const throw()
				{
					return (value_neighbor == value_center) && (label_neighbor == labelQueued /*|| label_neighbor == labelQueued2*/);
				}
			};





			//! Utility structure for choosing the points of the same label as the center one and only 
			//! in the front
			template <class t_value>
				struct s_filter_point_same_label_and_front
			{
				bool operator()(
					const t_value value_center, const Label /*label_center*/,
					const t_value value_neighbor, const Label label_neighbor) const
				{
					return value_neighbor == value_center;
				}
				bool neighbor_need_update(const t_value value_center, const Label /*label_center*/,
					const t_value value_neighbor, const Label label_neighbor) const
				{
					return value_neighbor == value_center && label_neighbor == labelQueued;
				}
			};


















			/*!
				* @brief Computes the flooding with an area constrained "viscous" fluid starting from a label image
				*
				* This function returns the result of the watershed using a viscous fluid. To do so, we suppose that
				* modifiying the priority of a point, while inserting it in the priority queue and with respect to
				* the local configuration, we obtain what we expect.
				* We modifie the priority through a function counting the number of points belonging to the same label
				* of the point. First, the ratio of same minus different label points, with the size of the ball used 
				* to compute it, is computed. Then a scale is given to the strenght of this ratio through the image imAlpha 
				* (local strenght).
				* 
				*
				* @param imin the gradient image
				* @param imLabels the constrained labels
				* @param op_constraint operator contraint
				* @param nl the structuring element representing the chosen connexity
				* @param constraint_SE the ball choosen for constraint
				* @param imout the output image of labels
				*
				*/

      template <class t_im_gradient, class image_labels_t, class se_t, class ball_type, class constraint_op_t>
        yaRC viscous_watershed_t(
          const t_im_gradient& imin,
          const image_labels_t& imLabels,
          const constraint_op_t& op_constraint,
          const se_t	&nl,
          const ball_type &constraint_SE,
          image_labels_t& imout)
      {

        // some runtime checks
        if(!are_same_geometry(imin, imout) || !are_same_geometry(imin, imLabels) || !are_same_geometry(imin, imAlpha))
        {
          DEBUG_INFO("Some images have incompatible offsets");
          return yaRC_E_bad_size;
        }



        // functors à passer en paramètre
        typedef s_filter_point_same_label_done<typename image_labels_t::pixel_type> filter_operator;
        typedef s_constraint_function_area<
          typename t_im_gradient::pixel_type, 
          typename t_im_alpha::pixel_type, 
          ball_type> constraint_operator;
        typedef typename constraint_operator::result_type key_type;


        typedef typename s_get_same_image_of_t<label_image_pixel_t, t_im_alpha>::type work_image_type;
        typedef typename s_get_same_image_of_t<key_type, t_im_alpha>::type work_priority_image_type;

        typedef std::vector< std::pair<offset, typename work_image_type::pixel_type> >	t_first_pass_queue;
        typedef std::vector< std::pair<std::pair<offset, offset>, typename work_image_type::pixel_type> > t_first_pass_discovered;
        typedef priority_queue_t<key_type, offset> t_priority_queue_type;



        // work image
        work_image_type work; 
        yaRC res = work.set_same(imin);
        if(res != yaRC_ok)
        {
          DEBUG_INFO("error in set_same");
          return res;
        }
        
        // priority image; this version of the flooding allows the modification of the priority during the flooding process
        work_priority_image_type work_priority; 
        res = work_priority.set_same(imin);
        if(res != yaRC_ok)
        {
          DEBUG_INFO("error in set_same");
          return res;
        }
                
        // constant values
        typename im_label_t::pixel_type const lpeVal(0);
        typename im_label_t::pixel_type const label_value_background(0);

        // for debugging purposes
  #ifdef __WATERSHED_VISQUEUX_FILE_OUT__
        if(t_ImDimension(work) > 2)
        {
          throw errors::yaException("t_ImViscousWatershed_v2 : Cannot trace : image of dimension > 2");
        }

        // raffi: cette ligne foirera la compil de toute manière si on fait le con
        Image<yaUINT8> imtemp;
        res = imtemp.set_same(work)
        int	i_file = 0;
        yaUINT32 nb_pixels_between_each_trace = (UINT32)(t_SizePixel(work) * 0.1 / 100), i_counter = 0;
        work.ColorInfo() = ciMonoSpectral;
  #endif


        // quelques calculs sur la boule
        filter_operator op_filter;
        constraint_operator op_constraint(constraint_SE);
        
        // do not forget this line
        res = copy_image_t(imLabels, imout);
        if(res != yaRC_ok)
        {
          DEBUG_INFO("error in copy_image_t(imLabels, imout)");
          return res;
        }

        res = constant_image_t(work, static_cast<label_image_pixel_t>(e_lab_candidate));
        if(res != yaRC_ok)
        {
          DEBUG_INFO("error in constant_image_t");
          return res;
        }

        res = constant_image_t(work_priority, 0.);
        if(res != yaRC_ok)
        {
          DEBUG_INFO("error in constant_image_t (work_priority)");
          return res;
        }



        // constraint neighborhood
        typedef se::s_runtime_neighborhood<image_labels_t const, se_t>  imlabel_neighborhood_t;        
        imlabel_neighborhood_t neighb_constraint(imout, constraint_SE);

        // neighbor graph for propagating (NeighborList)
        typedef se::s_runtime_neighborhood<image_labels_t const, se_t>   imlabel_neighborhood_t;
        imlabel_neighborhood_t neighb(imout,nl.remove_center());

        typedef Neighborhood<NeighborList, work_image_type > t_work_neigh;
        t_work_neigh work_neighb(work, nl);
        typename t_work_neigh::iterator	wit, wend;


        // queues
        t_priority_queue_type			priority_queue;
        t_first_pass_queue				temporary_queue_pfp;
        t_first_pass_discovered   temporary_queue_pfp2;
        std::vector<offset>       temporary_queue1, temporary_queue2, temporary_queue_watershed;

        int cleaning_inc = 0;

        // init part
        for(typename t_im_label::iterator out_it(imout.begin_block()), out_it_end(imout.end_block());
            out_it != out_it_end; 
            ++out_it) 
        {
          const t_label label_center = *out_it;

          // background points are neutral
          if(label_center == label_value_background)
            continue;

          const offset offset_center = out_it.Offset();


          // neighborhood test : we use the neighborhood to determine wheather the point is watershed or not
          bool b_is_watershed = false;
          temporary_queue1.clear();

          res = neighb_out.center(out_it);
          YAYI_ASSERT(res == yaRC_ok, "Error in setcenter");
          
          for(typename t_imlabel_neigh::const_iterator nit(neighb_out.begin_const()), nend(neighb_out.end_const()); nit != nend; ++nit)
          {
            const offset off = nit.Offset();
            
            /* on teste les voisins, pas le point en cours */
            if(off == offset_center) 
              continue;

            const t_label label_neighbor = *nit;

            // we don't handle the case neighbor = watershed point because imOut is updated during this pass 
            if(label_neighbor != label_value_background)
            {
              if(label_neighbor != label_center)
              {
                b_is_watershed = true;
                break;
              }
            }
            else
              temporary_queue1.push_back(off);
          }


          
          if(b_is_watershed)
          {
            // the point belongs to the watershed, we don't push it into the queue
            // but mark imout and imwork accordingly
            work.pixel(offset_center) = e_lab_watershed;
            imout.pixel(offset_center) = lpeVal;
          }
          else
          {

            // the point does not belong to the watershed: we process its neighbors
            work.pixel(offset_center) = e_lab_processed;
            
            // already done in the copy_image_t
            //imout.pixel(offset_center) = label_center;
            assert(imout.pixel(offset_center) == label_center);


            while(!temporary_queue1.empty())
            {
              const offset off = temporary_queue1.front();
              temporary_queue1.pop_front();
              if(work.pixel(off) == e_lab_candidate)
              {
                work.pixel(off) = e_lab_queued;
                temporary_queue_pfp.push_back(typename t_first_pass_queue::value_type(off, label_center));
              }
            }
          }
        } // for all points of imout



        for(typename t_first_pass_queue::const_iterator it = temporary_queue_pfp.begin(), it_e = temporary_queue_pfp.end();
            it != it_e;
            ++it)
        {
          const offset off = it->first;
          imout.pixel(off) = it->second;
          assert(work.pixel(off) == e_lab_queued);
        }
        
        for(typename t_first_pass_queue::const_iterator it = temporary_queue_pfp.begin(), it_e = temporary_queue_pfp.end();
          it != it_e;
          ++it)
        {
          const offset offset_center	= it->first;
          const t_label label_center  = it->second;
          const Label w_label         = work.pixel(offset_center);
          assert(work.pixel(offset_center) == e_lab_queued);


          // iterators init
          if(neighSEOut.center(offset_center) != yaRC_ok)
            YAYI_THROW("Error during the call of neighSEOut.setCenter (1)");
          t_it_label_ball			it_ball(neighSEOut.begin());
          const t_it_label_ball	it_ball_end(neighSEOut.end());
          
          // priority modifier init for the center point
          op_constraint.reset();
          if(op_constraint.center(offset_center) != yaRC)
            YAYI_THROW("Error during the call of op_constraint.center (1)");

          // parse of the points inside the ball
          for( ; it_ball!= it_ball_end; ++it_ball)
          {
            const offset_t offset_neighbor	= it_ball.Offset();
            const t_label label_neighbor	= imout.pixel(offset_neighbor);
            const Label w_neighbor			= work.pixel(offset_neighbor);

            // filtering points of interest
            if(op_filter(label_center, w_label, label_neighbor, w_neighbor))
            {
              // en esperant que le compilo comprendra ce qu'on souhaite faire
              op_constraint.push_new_point(imin.pixel(offset_neighbor), offset_neighbor);
            }
          }

          // get the result of the modification
          const key_type result = op_constraint(imin.pixel(offset_center), imAlpha.pixel(offset_center));
          
          //double res = imin.pixel(offset_center) - imAlpha.pixel(offset_center) * static_cast<double>(2 * sum_X - area)/static_cast<double>(area);
          priority_queue.push(result, offset_center);
          work_priority.pixel(offset_center) = result;
        }






        // process the queue
        while(!priority_queue.empty())
        {
          // priority order
          typename t_priority_queue_type::iterator it_plateau = priority_queue.top_plateau_begin();
          const typename t_priority_queue_type::iterator it_plateau_end = priority_queue.top_plateau_end();

          const key_type current_priority = it_plateau.key();
          temporary_queue2.clear();
          temporary_queue_pfp.clear();

          for(;it_plateau != it_plateau_end; ++it_plateau)
          {
            bool b_is_watershed = false, b_is_labeled = false;
            const offset_t offset_center = it_plateau.data();

            if(work_priority.pixel(offset_center) != current_priority)
              continue;

  #if 1
            t_label label_center = lpeVal;
  #else
            t_label label_center;
  #endif

            // thick watershed condition
            if(work.pixel(offset_center) == labelQueued2)
            {
              b_is_watershed = true;
            }
            else
            {
              // priority has been updated already
              // Raffi: revoir la condition


              //if(work.pixel(offset_center) != labelQueued)
              //	continue;
              
              temporary_queue1.clear();
              temporary_queue2.clear();
              work_neighb.setCenter(offset_center);
              wit = work_neighb.begin();
              wend= work_neighb.end();

              for(; wit != wend; ++wit)
              {
                const offset off = wit.Offset();

                // discard the center point
                if(off == offset_center) continue;
        
                const Label state_neighbor = *wit;
        
                if(state_neighbor == labelCandidate)
                {
                  temporary_queue1.push_back(off);
                }								
                
                else if(state_neighbor == labelDone)
                {
                  if(b_is_labeled)
                  {
                    // has alredy a 'done' neighbor
                    assert(label_center != lpeVal);
                    const t_label label_neighbor = imout.pixel(off);
                    
                    if((label_neighbor != label_center) && (label_neighbor != label_value_background))
                    {
                      assert(imout.pixel(off) != 0);
                      // no further computing, the point is watershed
                      b_is_watershed = true;
                      break;
                    }
                  }
                  else
                  {
                    label_center = imout.pixel(off);
                    b_is_labeled = true;
                  }
                }
                
                else if(state_neighbor == labelQueued || state_neighbor == labelQueued2)
                {
                  // the neighbor is also in the queue, we should further process this point
                  temporary_queue2.push_back(off);
                }
                else
                  //assert(state_neighbor == labelWatershed);
                  if(state_neighbor != labelWatershed)
                    YAYI_THROW("Unknown configuration");

              } // for all neighbors


              if(!b_is_watershed)
              {

                for(std::deque<offset_t>::const_iterator it = temporary_queue2.begin(), ite = temporary_queue2.end();
                  it != ite;
                  ++ it)
                {

                  const offset off = *it;

                  // if the neighbor's temporary label is different and the priorities matches, we have a thick watershed line
                  const t_label weak_label = imout.pixel(off);
                  assert(weak_label != label_value_background);
                  
                  // a priori, weak_label ne doit pas être à 0

                  // ajout de la condition b_is_labeled
                  if(weak_label != imout.pixel(offset_center))
                  {

                    // priorité + ou - alpha par rapport à la priorité courante: on suppose alors que les points appartiennent
                    // au même niveau.
                    
                    if(current_priority >= imin.pixel(off) - imAlpha.pixel(off))
                    {
                      // no further computing, the point is watershed
                      // do not forget b_is_labeled
                      b_is_labeled = b_is_watershed = true;
                                            
                      // the weak neighbor is flagged as 'watershed to be'
                      work.pixel(off) = labelQueued2;
                      temporary_queue_watershed.push_back(off);
                      
                      // not break there, wer should parse all the queued neighbors 
                      //break;
                    }
                  }
                }
              }




            } // if(work.pixel(offset_center) != labelQueued2)


            
            if(b_is_watershed)
            {
              // the point is watershed, we discard the neighbors and mark it accordingly
              // temporary_queue1.clear(); -> already done before the parsing of each neighborhood
              if(b_is_labeled)
                temporary_queue_watershed.push_back(offset_center);
            }
            else if(label_center != label_value_background) // which means b_is_labeled
            {
              // the point is not watershed, we wait before inserting the neighbors into the queue
              // label is strong now
              
              // important: we cannot modify work at this point. It will be later used for the modification
              // of priorities
              assert(label_center != label_value_background);
              temporary_queue_pfp.push_back(typename t_first_pass_queue::value_type(offset_center, label_center));

              // the discovered neighbors : they are put inside another queue, for later insertion into the HQ
              while(!temporary_queue1.empty())
              {
                const offset off = temporary_queue1.front();
                temporary_queue1.pop_front();

                // we cannot push the points into the main queue nor can we change work
                // since it will be used for the computation of new priorities
                temporary_queue_pfp2.push_back(std::make_pair(std::make_pair(off, offset_center), label_center));

              }

            } // if/else watershd point

            
          } // end of the current plateau


          // update the watershed points
          for(std::deque<offset_t>::const_iterator it = temporary_queue_watershed.begin(), ite = temporary_queue_watershed.end();
            it != ite;
            ++it)
          {
            const offset_t offset_center = *it;
            imout.pixel(offset_center) = lpeVal;
            work.pixel(offset_center) = labelWatershed;
          }




          // update of the whole front (formely queued points)
          // these points become strongly labelled, their offset are pushed into temporary_queue2
          temporary_queue2.clear();
          for(typename t_first_pass_queue::const_iterator it = temporary_queue_pfp.begin(), it_e = temporary_queue_pfp.end();
            it != it_e;
            ++it)
          {
            const offset_t offset_center = it->first;
            const t_label label_center = it->second;

            if(work.pixel(offset_center) == labelQueued)
            {
              work.pixel(offset_center)		= labelDone;
              //imout.pixel(offset_center)	= label_center;
              temporary_queue2.push_back(offset_center);
              
              // test intended for removal
              if(imout.pixel(offset_center)	!= label_center)
              {
                YAYI_THROW("imout.pixel(offset_center)	!= label_center");
              }



  #ifdef __WATERSHED_VISQUEUX_FILE_OUT__
              // trace sur le nombre de points ajoutés
              i_counter += 1;
              if(i_counter % nb_pixels_between_each_trace == 0)
              {
                std::cout << '.';
                t_ImCompareOp_sss(work, operationCompare_Equal<Label, Label>(), labelDone, 255, 0, imtemp);
                t_ImCompareOp_ssi(work, operationCompare_Equal<Label, Label>(), labelQueued, 50, imtemp, imtemp);
                t_ImCompareOp_ssi(work, operationCompare_Equal<Label, Label>(), labelQueued2, 100, imtemp, imtemp);
                pngFileWrite(
                  &imtemp, 
                  filesystem::joinPaths(root_path, string("trace_viscous_watershed_") + AnyToStringFormatted(i_file++, 5, '0') + string(".png")));
              }
  #endif
            }

          }


          std::cout << "U";
          // update the priority of the points that where in the queued before our action, which means ONLY points of queued state
          // the updated points are pushed into temporary_queue1
          temporary_queue1.clear();
          for(std::deque<offset_t>::const_iterator it = temporary_queue2.begin(), it_e = temporary_queue2.end();
            it != it_e;
            ++it)
          {
            const offset_t offset_center	= *it;
            //const t_label label_center		= it->second; /* also equal to imout.pixel(offset_center) due to the previous update */

            const t_label label_center = imout.pixel(offset_center);


            // now we look for the queued points (the queued ones BEFORE we parsed the plateau)

            // centers the ball
            if(neighSEOut.setCenter(offset_center) != yaRC_ok)
              YAYI_THROW("Error during the call of neighSEOut.setCenter (2)");
            t_it_label_ball			it_ball(neighSEOut.begin());
            const t_it_label_ball	it_ball_end(neighSEOut.end());


            // init the priority modifier
            op_constraint.reset();
            if(op_constraint.center(offset_center) != yaRC_ok)
              YAYI_THROW("Error during the call of op_constraint.center (2)");


            for( ; it_ball!= it_ball_end; ++it_ball)
            {
              const offset offset_neighbor  = it_ball.Offset();
              const t_label label_neighbor  = imout.pixel(offset_neighbor);
              const Label w_neighbor        = work.pixel(offset_neighbor);


              if(op_filter.neighbor_need_update(label_center, labelDone, label_neighbor, w_neighbor))
              {

                if(constraint_operator::easy_update)
                  work_priority.pixel(offset_neighbor) += op_constraint.update(
                    imin.pixel(offset_neighbor), 
                    imAlpha.pixel(offset_neighbor));


                // to avoid more than one update
                if(std::find(temporary_queue1.begin(), temporary_queue1.end(), offset_neighbor) == temporary_queue1.end())
                {
                  temporary_queue1.push_back(offset_neighbor);
                }

              }
            }
          }


          // now the points of temporary_queue1 need to be updated
          // for the easy update, they were already updated during the search, so the only thing needed here
          // is to push their updated priority into the queue, from the priority image
          if(constraint_operator::easy_update)
          {
            for(std::deque<offset>::const_iterator it(temporary_queue1.begin()), ite(temporary_queue1.end()); it != ite; ++it)
            {
              const offset offset_neighbor = *it;
              priority_queue.push_buffered(work_priority.pixel(offset_neighbor), offset_neighbor);
            }
            temporary_queue1.clear();
          }

          // discovered points
          // their priority should be computed properly
          // the list of points is augmented with the points having a change in their local configuration
          // for the case !constraint_operator::easy_update
          for(typename t_first_pass_discovered::const_iterator it = temporary_queue_pfp2.begin(), it_e = temporary_queue_pfp2.end();
            it != it_e;
            ++it)
          {

            const offset_t offset_source = (it->first).second;
            if(work.pixel(offset_source) != labelDone)
              continue;

            const offset_t off = (it->first).first;
            
            // because points can be pushed more than once
            if(work.pixel(off) != labelCandidate)
              continue;

            const t_label label_center = it->second; // weak temporary label
            work.pixel(off) = labelQueued;
            imout.pixel(off)= label_center;

            // planified for update
            temporary_queue1.push_back(off);
          }


          // update of the points that need to be:
          // 1 - easy_update: the list of points contains only the discovered points
          // 2 - not easy_update : the list of points contains the discovered points along with the points having a change in their neighborhood
          for(std::deque<offset_t>::const_iterator it = temporary_queue1.begin(), it_e = temporary_queue1.end();
            it != it_e;
            ++it)
          {
            const offset_t offset_center	= *it;
            const t_label label_center		= imout.pixel(offset_center);
            assert(work.pixel(offset_center) == labelQueued);

            // iterators init
            if(neighSEOut.center(offset_center) != yaRC_ok)
              YAYI_THROW("Error during the call of neighSEOut.setCenter (1)");
            t_it_label_ball			it_ball(neighSEOut.begin());
            const t_it_label_ball	it_ball_end(neighSEOut.end());
            
            // priority modifier init for the center point
            op_constraint.reset();
            if(op_constraint.center(offset_center) != yaRC_ok)
              YAYI_THROW("Error during the call of op_constraint.center (1)");

            // parse of the points inside the ball
            for( ; it_ball!= it_ball_end; ++it_ball)
            {
              const offset_t offset_neighbor	= it_ball.Offset();
              const t_label label_neighbor	= imout.pixel(offset_neighbor);
              const Label w_neighbor			= work.pixel(offset_neighbor);

              // filtering points of interest
              if(op_filter(label_center, labelQueued, label_neighbor, w_neighbor))
              {
                // en esperant que le compilo comprendra ce qu'on souhaite faire
                op_constraint.push_new_point(imin.pixel(offset_neighbor), offset_neighbor);
              }
            }

            // get the result of the modification
            const key_type res = op_constraint(imin.pixel(offset_center), imAlpha.pixel(offset_center));
            
            //double res = imin.pixel(offset_center) - imAlpha.pixel(offset_center) * static_cast<double>(2 * sum_X - area)/static_cast<double>(area);
            priority_queue.push_buffered(res, offset_center);
            work_priority.pixel(offset_center) = res;

          }

          










  #if 0

          for(typename t_first_pass_queue::const_iterator it = temporary_queue_pfp2.begin(), it_e = temporary_queue_pfp2.end();
            it != it_e;
            ++it)
          {
            const offset_t offset_center	= it->first;
            const t_label label_center		= it->second; // weak temporary label





            // compute the ball
            if(neighSEOut.center(offset_center) != yaRC_ok)
              YAYI_THROW("Error during the call of neighSEOut.setCenter (3)");
            t_it_label_ball			it_ball(neighSEOut.begin());
            const t_it_label_ball	it_ball_end(neighSEOut.end());
            
            // init the priority modifier
            op_constraint.reset();
            if(op_constraint.center(offset_center) != yaRC_ok)
              YAYI_THROW("Error during the call of op_constraint.center (3)");

            for( ; it_ball!= it_ball_end; ++it_ball)
            {
              const offset_t offset_neighbor	= it_ball.Offset();
              const t_label label_neighbor	= imout.pixel(offset_neighbor);
              const Label w_neighbor			= work.pixel(offset_neighbor);

              // discard the center
              if(offset_neighbor == offset_center)
              {
                assert(w_neighbor != labelDone);
                continue;
              }


              // only done points sucker (là c'est parce que j'écoute Cypress Hill ...)
              if(op_filter(label_center, labelDone, label_neighbor, w_neighbor))
              {
                op_constraint.push_new_point(imin.pixel(offset_neighbor), offset_neighbor);
              }

              /*if(w_neighbor == labelDone)
              {
                if(label_neighbor == label_center)
                {
                  op_constraint.push_new_point(imin.pixel(offset_neighbor), offset_neighbor);
                }
              }*/

            }

            //double res = imin.pixel(offset_center) - imAlpha.pixel(offset_center) * (2 * sum_X - area)/static_cast<double>(area);
            const key_type res = op_constraint(imin.pixel(offset_center), imAlpha.pixel(offset_center));
            priority_queue.push_buffered(res, offset_center);
            assert(work_priority.pixel(offset_center) == 0.);
            work_priority.pixel(offset_center) = res;
          }





  #if 0


          //std::cout << "(15) : size = " << priority_queue.size();


          // inserting new points with modified priority
          // adjusting queued points priority with the new constraint
          temporary_queue1.clear();
          int toto = 0;
          while(!temporary_queue2.empty())
          {
            const offset_t offset_center = temporary_queue2.front();
            temporary_queue2.pop_front();

            // label provisoire (wait_for_first_pass) du centre : ce sont les points e_Queued
            const t_label label_center = imout.pixel(offset_center);

            // compute the ball
            neighSEOut.setCenter(offset_center);
            t_it_label_ball it_ball(neighSEOut.begin());
            const t_it_label_ball it_ball_end(neighSEOut.end());
            op_constraint.reset();

            const Label w_center = work.pixel(offset_center);

            UINT16 sum_X = 0;
            for( ; it_ball!= it_ball_end; ++it_ball)
            {
              const offset_t offset_neighbor = it_ball.Offset();
              const t_label label_neighbor = imout.pixel(offset_neighbor);
              const Label w_neighbor = work.pixel(offset_neighbor);


  #if 0

              // we compute the constraint on the center point
              if(op_filter(label_center, w_center, label_neighbor, w_neighbor))
              {
                // en esperant que le compilo comprendra ce qu'on souhaite faire
                op_constraint.push_new_point(imin.pixel(offset_neighbor), offset_neighbor);
              }

              // the easy update should not depend on the local configuration
              if(op_filter.neighbor_need_update(label_center, w_center, label_neighbor, w_neighbor))
              {
                if(constraint_operator::easy_update)
                {
                  work_priority.pixel(offset_neighbor) += op_constraint.update(
                    imin.pixel(offset_neighbor), 
                    imAlpha.pixel(offset_neighbor));
                }

                // pushing points that need updade, but not twice
                if(std::find(temporary_queue1.begin(), temporary_queue1.end(), offset_neighbor) == temporary_queue1.end())
                {
                  temporary_queue1.push_back(offset_neighbor);
                }
              }
  #else

              if(offset_neighbor == offset_center)
                continue;


              if(w_neighbor == labelQueued)
              {
                if(label_neighbor == label_center)
                {
                  work_priority.pixel(offset_neighbor) -= (imAlpha.pixel(offset_neighbor) * 2.)/static_cast<double>(area);
                  //sum_X ++;
                  if(std::find(temporary_queue1.begin(), 
                      temporary_queue1.end(), 
                      offset_neighbor) == temporary_queue1.end())
                  {
                    temporary_queue1.push_back(offset_neighbor);
                  }
                }
                
              }
              else if(w_neighbor == labelDone && label_neighbor == label_center)
              {
                sum_X ++;
              }

  #endif
            } // for the ball

            //const key_type res = op_constraint(imin.pixel(offset_center), imAlpha.pixel(offset_center));
            double result = imin.pixel(offset_center) - imAlpha.pixel(offset_center) * (2 * sum_X - area)/static_cast<double>(area);
            priority_queue.push_buffered(result, offset_center);
            work_priority.pixel(offset_center) = result;
          }


          // adjusting neighbors
          while(!temporary_queue1.empty())
          {
            const offset_t offset_center = temporary_queue1.front();
            temporary_queue1.pop_front();


  #if 0
            // non easy update: means we should update completely the neighbors
            // without this time cycling on neighbor's neighbors update :)
            // the code below should be correctly discarded by the compiler for the appropriate cases
            if(!constraint_operator::easy_update)
            {
              const t_label label_center = imout.pixel(offset_center);
              neighSEOut.setCenter(offset_center);
              t_it_label_ball it_ball(neighSEOut.begin());
              const t_it_label_ball it_ball_end(neighSEOut.end());
              op_constraint.reset();
              const Label w_center = work.pixel(offset_center);
              for( ; it_ball!= it_ball_end; ++it_ball)
              {
                const offset_t offset_neighbor = it_ball.Offset();
                const t_label label_neighbor = imout.pixel(offset_neighbor);
                const Label w_neighbor = work.pixel(offset_neighbor);

                // we compute the constraint on the center point
                if(op_filter(label_center, w_center, label_neighbor, w_neighbor))
                {
                  // en esperant que le compilo comprendra ce qu'on souhaite faire
                  op_constraint.push_new_point(imin.pixel(offset_neighbor), offset_neighbor);
                }


              } // for the ball

              const key_type res = op_constraint(imin.pixel(offset_center), imAlpha.pixel(offset_center));
              priority_queue.push_buffered(res, offset_center);
              work_priority.pixel(offset_center) = res;

            } // not easy update
            else
            {
              // this case: updated points can be present several time inside the queue
              priority_queue.push_buffered(work_priority.pixel(offset_center), offset_center);
            }
  #else
            priority_queue.push_buffered(work_priority.pixel(offset_center), offset_center);
  #endif


          }
  #endif


  #endif


          // ok this is the end of the plateau, we can continue to the next
          priority_queue.top_plateau_pop();

          if(++cleaning_inc == 200)
          {
            cleaning_inc = 0;
            t_priority_queue_type priority_queue_temp;

            typename work_image_type::iterator w_it = work.begin();
            const typename work_image_type::iterator w_ite = work.end();
            for(; w_it != w_ite; ++w_it)
            {
              const offset off = w_it.Offset();
              const Label lab = *w_it;
              if(lab == labelQueued || lab == labelQueued2)
                priority_queue_temp.push(work_priority.pixel(off), off);
            }

            std::cout << 'x';
            priority_queue.swap(priority_queue_temp);
          }






        } // while !priority_queue.empty()
        
  #if 0
        std::cout << "end image...";
        t_ImCompareOp_sss(work, operationCompare_Equal<Label, Label>(), labelDone, 255, 0, imtemp);
        t_ImCompareOp_ssi(work, operationCompare_Equal<Label, Label>(), labelQueued, 50, imtemp, imtemp);
        t_ImCompareOp_ssi(work, operationCompare_Equal<Label, Label>(), labelQueued2, 100, imtemp, imtemp);
        pngFileWrite(
          &imtemp, 
          filesystem::joinPaths(root_path, string("trace_viscous_watershed_") + AnyToStringFormatted(i_file++, 5, '0') + string(".png")));
  #endif
        return yayi::yaRC_ok;
      }

      template <class t_im_gradient, class t_im_label, class ball_type>
        yaRC t_ImViscousWatershed_v2_constant_alpha(
          const t_im_gradient& imin,
          const t_im_label& imLabels,
          const float alpha,
          const selement::NeighborList	&nl,
          const ball_type &constraint_SE,
          t_im_label& imout)
      {

        typedef typename t_im_label::value_type		t_label;
        typedef float    t_alpha;


        // functors à passer en paramètre
        typedef s_filter_point_same_label_done<t_label>							              filter_operator;
        typedef s_constraint_function_area<typename t_im_gradient::pixel_type, t_alpha, ball_type>		    constraint_operator;
        typedef typename constraint_operator::result_type						              key_type;


        typedef typename s_from_type_to_type<t_im_gradient,Label>::image_type		    work_image_type;
        typedef typename s_from_type_to_type<t_im_gradient,key_type>::image_type	    work_priority_image_type;

        typedef std::deque< std::pair<offset_t, t_label> >						            t_first_pass_queue;
        typedef std::deque< std::pair<std::pair<offset_t, offset_t>, t_label> >   t_first_pass_discovered;
        typedef common_priority_queue<key_type, offset_t >						            t_priority_queue_type;




        if(		!t_CheckOffsetCompatible(imin, imout) 
          ||	!t_CheckOffsetCompatible(imin, imLabels))
          return yayi::yaRC_E_bad_size;			

        yaRC res;

        // work image
        work_image_type work; work.set_same(imin);
        
        // priority image; this version of the flooding allows the modification of the priority during the flooding process
        work_priority_image_type work_priority; work_priority.set_same(imin);
        
        // constant values
        const t_label lpeVal = DataTraits<t_label>::default_value::background();
        const t_label label_value_background = DataTraits<t_label>::default_value::background();

        // for debugging purposes
  #ifdef __WATERSHED_VISQUEUX_FILE_OUT__
        if(t_ImDimension(work) > 2)
        {
          YAYI_THROW("t_ImViscousWatershed_v2 : Cannot trace : image of dimension > 2");
        }

        // raffi: cette ligne foirera la compil de toute manière si on fait le con
        Image<UINT8> imtemp = work.template t_getSame<UINT8>();
        int	i_file = 0;
        UINT32 nb_pixels_between_each_trace = (UINT32)(t_SizePixel(work) * 0.1 / 100), i_counter = 0;
        work.ColorInfo() = ciMonoSpectral;
  #endif


        std::cout << "t_ImViscousWatershed_v2: initialising images" << std::endl;

        // quelques calculs sur la boule
        //const yaF_double size_boule = dummy;
        filter_operator op_filter;
        constraint_operator op_constraint(constraint_SE);
        

        // do not forget this line: very important indeed
        res = copy_image_t(imLabels, imout);
        if(res != yaRC_ok)
        {
          DEBUG_INFO("t_ImViscousWatershed_v2: error in copy_image_t(imLabels, imout)");
          return res;
        }

        res = t_ImSetConstant(work, labelCandidate);
        if(res != yaRC_ok)
        {
          DEBUG_INFO("t_ImViscousWatershed_v2: error in t_ImSetConstant : work");
          return res;
        }
        res = t_ImBorderSetConstant(work, labelWatershed);

        res = t_ImSetConstant(work_priority, 0.);
        if(res != yaRC_ok)
        {
          DEBUG_INFO("t_ImViscousWatershed_v2: error in t_ImSetConstant : work_priority");
          return res;
        }



        // constraint neighborhood
        typedef Neighborhood<ball_type, t_im_label>				t_im_label_type_ball_neigh;
        typedef typename t_im_label_type_ball_neigh::iterator	t_it_label_ball;
        t_im_label_type_ball_neigh neighSEOut(imout, constraint_SE);

        // neighbor graph for propagating (NeighborList)
        typedef Neighborhood<NeighborList, t_im_label> t_imlabel_neigh;
        t_imlabel_neigh neighb_out(imout,nl);

        typedef Neighborhood<NeighborList, work_image_type > t_work_neigh;
        t_work_neigh work_neighb(work, nl);
        typename t_work_neigh::iterator	wit, wend;


        // queues
        t_priority_queue_type			priority_queue;
        t_first_pass_queue				temporary_queue_pfp;
        t_first_pass_discovered			temporary_queue_pfp2;
        std::deque<offset_t>			temporary_queue1, temporary_queue2, temporary_queue_watershed;

        int cleaning_inc = 0;

        // init part

        typename t_im_label::iterator out_it = imout.begin();
        const typename t_im_label::iterator out_it_end = imout.end();

        std::cout << "Init queue" << std::endl;
        for(;out_it != out_it_end; ++out_it) 
        {
          const t_label label_center = *out_it;

          // background points are neutral
          if(label_center == label_value_background)
            continue;

          const offset_t offset_center = out_it.Offset();


          // neighborhood test : we use the neighborhood to determine wheather the point is watershed or not
          bool b_is_watershed = false;
          temporary_queue1.clear();

          if(neighb_out.setCenter(out_it) != yaRC_ok)
            YAYI_THROW("neighb_out.setCenter failed");
          typename t_imlabel_neigh::const_iterator		nit(neighb_out.begin_const());
          const typename t_imlabel_neigh::const_iterator	nend(neighb_out.end_const());
          for( ; nit != nend; ++nit)
          {
            const offset_t offset = nit.Offset();
            
            /* on teste les voisins, pas le point en cours */
            if(offset == offset_center) 
              continue;

            const t_label label_neighbor = *nit;

            // we don't handle the case neighbor = watershed point because imOut is updated during this pass 
            if(label_neighbor != label_value_background)
            {
              if(label_neighbor != label_center)
              {
                b_is_watershed = true;
                break;
              }
            }
            else
              temporary_queue1.push_back(offset);
          }


          
          if(b_is_watershed)
          {
            // the point belongs to the watershed, we don't push it into the queue
            // but mark imout and imwork accordingly
            work.pixel(offset_center) = labelWatershed;
            imout.pixel(offset_center) = lpeVal;
          }
          else
          {

            // the point does not belong to the watershed: we process its neighbors
            work.pixel(offset_center) = labelDone;
            
            // already done in the copy_image_t
            //imout.pixel(offset_center) = label_center;
            assert(imout.pixel(offset_center) == label_center);


            while(!temporary_queue1.empty())
            {
              const offset_t offset = temporary_queue1.front();
              temporary_queue1.pop_front();
              if(work.pixel(offset) == labelCandidate)
              {
                work.pixel(offset) = labelQueued;
                temporary_queue_pfp.push_back(typename t_first_pass_queue::value_type(offset, label_center));
              }
            }
          }
        } // for all points of imout



        for(typename t_first_pass_queue::const_iterator it = temporary_queue_pfp.begin(), it_e = temporary_queue_pfp.end();
          it != it_e;
          ++it)
        {
          const offset_t offset = it->first;
          imout.pixel(offset) = it->second;
          assert(work.pixel(offset) == labelQueued);
        }
        
        for(typename t_first_pass_queue::const_iterator it = temporary_queue_pfp.begin(), it_e = temporary_queue_pfp.end();
          it != it_e;
          ++it)
        {
          const offset_t offset_center	= it->first;
          const t_label label_center		= it->second;
          const Label w_label				= work.pixel(offset_center);
          assert(work.pixel(offset_center) == labelQueued);


          // iterators init
          if(neighSEOut.setCenter(offset_center) != yaRC_ok)
            YAYI_THROW("Error during the call of neighSEOut.setCenter (1)");
          t_it_label_ball			it_ball(neighSEOut.begin());
          const t_it_label_ball	it_ball_end(neighSEOut.end());
          
          // priority modifier init for the center point
          op_constraint.reset();
          if(op_constraint.center(offset_center) != yaRC_ok)
            YAYI_THROW("Error during the call of op_constraint.center (1)");

          // parse of the points inside the ball
          for( ; it_ball!= it_ball_end; ++it_ball)
          {
            const offset_t offset_neighbor	= it_ball.Offset();
            const t_label label_neighbor	= imout.pixel(offset_neighbor);
            const Label w_neighbor			= work.pixel(offset_neighbor);

            // filtering points of interest
            if(op_filter(label_center, w_label, label_neighbor, w_neighbor))
            {
              // en esperant que le compilo comprendra ce qu'on souhaite faire
              op_constraint.push_new_point(imin.pixel(offset_neighbor), offset_neighbor);
            }
          }

          // get the result of the modification
          const key_type res = op_constraint(imin.pixel(offset_center), alpha/*imAlpha.pixel(offset_center)*/);
          
          //double res = imin.pixel(offset_center) - imAlpha.pixel(offset_center) * static_cast<double>(2 * sum_X - area)/static_cast<double>(area);
          priority_queue.push(res, offset_center);
          work_priority.pixel(offset_center) = res;
        }






        // process the queue
        while(!priority_queue.empty())
        {
          std::cout << "I : ";

          // priority order
          typename t_priority_queue_type::iterator it_plateau = priority_queue.top_plateau_begin();
          const typename t_priority_queue_type::iterator it_plateau_end = priority_queue.top_plateau_end();

          const key_type current_priority = it_plateau.key();
          temporary_queue2.clear();
          temporary_queue_pfp.clear();

          std::cout << "Current priority : " << current_priority << std::endl;

          for(;it_plateau != it_plateau_end; ++it_plateau)
          {
            bool b_is_watershed = false, b_is_labeled = false;
            const offset_t offset_center = it_plateau.data();

            if(work_priority.pixel(offset_center) != current_priority)
              continue;

  #if 1
            t_label label_center = lpeVal;
  #else
            t_label label_center;
  #endif

            // thick watershed condition
            if(work.pixel(offset_center) == labelQueued2)
            {
              b_is_watershed = true;
            }
            else
            {
              // priority has been updated already
              // Raffi: revoir la condition


              //if(work.pixel(offset_center) != labelQueued)
              //	continue;
              
              temporary_queue1.clear();
              temporary_queue2.clear();
              work_neighb.setCenter(offset_center);
              wit = work_neighb.begin();
              wend= work_neighb.end();

              for(; wit != wend; ++wit)
              {
                const offset_t offset = wit.Offset();

                // discard the center point
                if(offset == offset_center) continue;
        
                const Label state_neighbor = *wit;
        
                if(state_neighbor == labelCandidate)
                {
                  temporary_queue1.push_back(offset);
                }								
                
                else if(state_neighbor == labelDone)
                {
                  if(b_is_labeled)
                  {
                    // has alredy a 'done' neighbor
                    assert(label_center != lpeVal);
                    const t_label label_neighbor = imout.pixel(offset);
                    
                    if((label_neighbor != label_center) && (label_neighbor != label_value_background))
                    {
                      assert(imout.pixel(offset) != 0);
                      // no further computing, the point is watershed
                      b_is_watershed = true;
                      break;
                    }
                  }
                  else
                  {
                    label_center = imout.pixel(offset);
                    b_is_labeled = true;
                  }
                }
                
                else if(state_neighbor == labelQueued || state_neighbor == labelQueued2)
                {
                  // the neighbor is also in the queue, we should further process this point
                  temporary_queue2.push_back(offset);
                }
                else
                  //assert(state_neighbor == labelWatershed);
                  if(state_neighbor != labelWatershed)
                    YAYI_THROW("Unknown configuration");

              } // for all neighbors


              if(!b_is_watershed)
              {

                for(std::deque<offset_t>::const_iterator it = temporary_queue2.begin(), ite = temporary_queue2.end();
                  it != ite;
                  ++ it)
                {

                  const offset_t offset = *it;

                  // if the neighbor's temporary label is different and the priorities matches, we have a thick watershed line
                  const t_label weak_label = imout.pixel(offset);
                  assert(weak_label != label_value_background);
                  
                  // a priori, weak_label ne doit pas être à 0

                  // ajout de la condition b_is_labeled
                  if(weak_label != imout.pixel(offset_center))
                  {

                    // priorité + ou - alpha par rapport à la priorité courante: on suppose alors que les points appartiennent
                    // au même niveau.
                    
                    if(current_priority >= imin.pixel(offset) - alpha/*imAlpha.pixel(offset)*/)
                    {
                      // no further computing, the point is watershed
                      // do not forget b_is_labeled
                      b_is_labeled = b_is_watershed = true;
                                            
                      // the weak neighbor is flagged as 'watershed to be'
                      work.pixel(offset) = labelQueued2;
                      temporary_queue_watershed.push_back(offset);
                      
                      // not break there, wer should parse all the queued neighbors 
                      //break;
                    }
                  }
                }
              }




            } // if(work.pixel(offset_center) != labelQueued2)


            
            if(b_is_watershed)
            {
              // the point is watershed, we discard the neighbors and mark it accordingly
              // temporary_queue1.clear(); -> already done before the parsing of each neighborhood
              if(b_is_labeled)
                temporary_queue_watershed.push_back(offset_center);
            }
            else if(label_center != label_value_background) // which means b_is_labeled
            {
              // the point is not watershed, we wait before inserting the neighbors into the queue
              // label is strong now
              
              // important: we cannot modify work at this point. It will be later used for the modification
              // of priorities
              assert(label_center != label_value_background);
              temporary_queue_pfp.push_back(typename t_first_pass_queue::value_type(offset_center, label_center));

              // the discovered neighbors : they are put inside another queue, for later insertion into the HQ
              while(!temporary_queue1.empty())
              {
                const offset_t offset = temporary_queue1.front();
                temporary_queue1.pop_front();

                // we cannot push the points into the main queue nor can we change work
                // since it will be used for the computation of new priorities
                temporary_queue_pfp2.push_back(std::make_pair(std::make_pair(offset, offset_center), label_center));

              }

            } // if/else watershd point

            
          } // end of the current plateau


          // update the watershed points
          for(std::deque<offset_t>::const_iterator it = temporary_queue_watershed.begin(), ite = temporary_queue_watershed.end();
            it != ite;
            ++it)
          {
            const offset_t offset_center = *it;
            imout.pixel(offset_center) = lpeVal;
            work.pixel(offset_center) = labelWatershed;
          }




          // update of the whole front (formely queued points)
          // these points become strongly labelled, their offset are pushed into temporary_queue2
          temporary_queue2.clear();
          for(typename t_first_pass_queue::const_iterator it = temporary_queue_pfp.begin(), it_e = temporary_queue_pfp.end();
            it != it_e;
            ++it)
          {
            const offset_t offset_center = it->first;
            const t_label label_center = it->second;

            if(work.pixel(offset_center) == labelQueued)
            {
              work.pixel(offset_center)		= labelDone;
              //imout.pixel(offset_center)	= label_center;
              temporary_queue2.push_back(offset_center);
              
              // test intended for removal
              if(imout.pixel(offset_center)	!= label_center)
              {
                YAYI_THROW("imout.pixel(offset_center)	!= label_center");
              }



  #ifdef __WATERSHED_VISQUEUX_FILE_OUT__
              // trace sur le nombre de points ajoutés
              i_counter += 1;
              if(i_counter % nb_pixels_between_each_trace == 0)
              {
                std::cout << '.';
                t_ImCompareOp_sss(work, operationCompare_Equal<Label, Label>(), labelDone, 255, 0, imtemp);
                t_ImCompareOp_ssi(work, operationCompare_Equal<Label, Label>(), labelQueued, 50, imtemp, imtemp);
                t_ImCompareOp_ssi(work, operationCompare_Equal<Label, Label>(), labelQueued2, 100, imtemp, imtemp);
                pngFileWrite(
                  &imtemp, 
                  filesystem::joinPaths(root_path, string("trace_viscous_watershed_") + AnyToStringFormatted(i_file++, 5, '0') + string(".png")));
              }
  #endif
            }

          }


          std::cout << "U";
          // update the priority of the points that where in the queued before our action, which means ONLY points of queued state
          // the updated points are pushed into temporary_queue1
          temporary_queue1.clear();
          for(std::deque<offset_t>::const_iterator it = temporary_queue2.begin(), it_e = temporary_queue2.end();
            it != it_e;
            ++it)
          {
            const offset_t offset_center	= *it;
            //const t_label label_center		= it->second; /* also equal to imout.pixel(offset_center) due to the previous update */

            const t_label label_center = imout.pixel(offset_center);


            // now we look for the queued points (the queued ones BEFORE we parsed the plateau)

            // centers the ball
            if(neighSEOut.setCenter(offset_center) != yaRC_ok)
              YAYI_THROW("Error during the call of neighSEOut.setCenter (2)");
            t_it_label_ball			it_ball(neighSEOut.begin());
            const t_it_label_ball	it_ball_end(neighSEOut.end());


            // init the priority modifier
            op_constraint.reset();
            if(op_constraint.center(offset_center) != yaRC_ok)
              YAYI_THROW("Error during the call of op_constraint.center (2)");


            for( ; it_ball!= it_ball_end; ++it_ball)
            {
              const offset_t offset_neighbor	= it_ball.Offset();
              const t_label label_neighbor	= imout.pixel(offset_neighbor);
              const Label w_neighbor			= work.pixel(offset_neighbor);


              if(op_filter.neighbor_need_update(label_center, labelDone, label_neighbor, w_neighbor))
              {

                if(constraint_operator::easy_update)
                  work_priority.pixel(offset_neighbor) += op_constraint.update(
                    imin.pixel(offset_neighbor), 
                    alpha/*imAlpha.pixel(offset_neighbor)*/);


                // to avoid more than one update
                if(std::find(temporary_queue1.begin(), temporary_queue1.end(), offset_neighbor) == temporary_queue1.end())
                {
                  temporary_queue1.push_back(offset_neighbor);
                }

              }
            }
          }


          // now the points of temporary_queue1 need to be updated
          // for the easy update, they were already updated during the search, so the only thing needed here
          // is to push their updated priority into the queue, from the priority image
          if(constraint_operator::easy_update)
          {
            for(std::deque<offset_t>::const_iterator it = temporary_queue1.begin(), ite = temporary_queue1.end(); it != ite; ++it)
            {
              const offset_t offset_neighbor = *it;
              priority_queue.push_buffered(work_priority.pixel(offset_neighbor), offset_neighbor);
            }
            temporary_queue1.clear();
          }

          // discovered points
          // their priority should be computed properly
          // the list of points is augmented with the points having a change in their local configuration
          // for the case !constraint_operator::easy_update
          for(typename t_first_pass_discovered::const_iterator it = temporary_queue_pfp2.begin(), it_e = temporary_queue_pfp2.end();
            it != it_e;
            ++it)
          {

            const offset_t offset_source		= (it->first).second;
            if(work.pixel(offset_source) != labelDone)
              continue;

            const offset_t offset				= (it->first).first;
            
            // because points can be pushed more than once
            if(work.pixel(offset) != labelCandidate)
              continue;

            const t_label label_center			= it->second; // weak temporary label
            work.pixel(offset)		= labelQueued;
            imout.pixel(offset)		= label_center;

            // planified for update
            temporary_queue1.push_back(offset);
          }


          // update of the points that need to be:
          // 1 - easy_update: the list of points contains only the discovered points
          // 2 - not easy_update : the list of points contains the discovered points along with the points having a change in their neighborhood
          for(std::deque<offset_t>::const_iterator it = temporary_queue1.begin(), it_e = temporary_queue1.end();
            it != it_e;
            ++it)
          {
            const offset_t offset_center	= *it;
            const t_label label_center		= imout.pixel(offset_center);
            assert(work.pixel(offset_center) == labelQueued);

            // iterators init
            if(neighSEOut.setCenter(offset_center) != yaRC_ok)
              YAYI_THROW("Error during the call of neighSEOut.setCenter (1)");
            t_it_label_ball			it_ball(neighSEOut.begin());
            const t_it_label_ball	it_ball_end(neighSEOut.end());
            
            // priority modifier init for the center point
            op_constraint.reset();
            if(op_constraint.center(offset_center) != yaRC_ok)
              YAYI_THROW("Error during the call of op_constraint.center (1)");

            // parse of the points inside the ball
            for( ; it_ball!= it_ball_end; ++it_ball)
            {
              const offset_t offset_neighbor	= it_ball.Offset();
              const t_label label_neighbor	= imout.pixel(offset_neighbor);
              const Label w_neighbor			= work.pixel(offset_neighbor);

              // filtering points of interest
              if(op_filter(label_center, labelQueued, label_neighbor, w_neighbor))
              {
                // en esperant que le compilo comprendra ce qu'on souhaite faire
                op_constraint.push_new_point(imin.pixel(offset_neighbor), offset_neighbor);
              }
            }

            // get the result of the modification
            const key_type res = op_constraint(imin.pixel(offset_center), alpha/*imAlpha.pixel(offset_center)*/);
            
            //double res = imin.pixel(offset_center) - imAlpha.pixel(offset_center) * static_cast<double>(2 * sum_X - area)/static_cast<double>(area);
            priority_queue.push_buffered(res, offset_center);
            work_priority.pixel(offset_center) = res;

          }

          










  #if 0

          for(typename t_first_pass_queue::const_iterator it = temporary_queue_pfp2.begin(), it_e = temporary_queue_pfp2.end();
            it != it_e;
            ++it)
          {
            const offset_t offset_center	= it->first;
            const t_label label_center		= it->second; // weak temporary label





            // compute the ball
            if(neighSEOut.setCenter(offset_center) != yaRC_ok)
              YAYI_THROW("Error during the call of neighSEOut.setCenter (3)");
            t_it_label_ball			it_ball(neighSEOut.begin());
            const t_it_label_ball	it_ball_end(neighSEOut.end());
            
            // init the priority modifier
            op_constraint.reset();
            if(op_constraint.center(offset_center) != yaRC_ok)
              YAYI_THROW("Error during the call of op_constraint.center (3)");

            for( ; it_ball!= it_ball_end; ++it_ball)
            {
              const offset_t offset_neighbor	= it_ball.Offset();
              const t_label label_neighbor	= imout.pixel(offset_neighbor);
              const Label w_neighbor			= work.pixel(offset_neighbor);

              // discard the center
              if(offset_neighbor == offset_center)
              {
                assert(w_neighbor != labelDone);
                continue;
              }


              // only done points sucker (là c'est parce que j'écoute Cypress Hill ...)
              if(op_filter(label_center, labelDone, label_neighbor, w_neighbor))
              {
                op_constraint.push_new_point(imin.pixel(offset_neighbor), offset_neighbor);
              }

              /*if(w_neighbor == labelDone)
              {
                if(label_neighbor == label_center)
                {
                  op_constraint.push_new_point(imin.pixel(offset_neighbor), offset_neighbor);
                }
              }*/

            }

            //double res = imin.pixel(offset_center) - imAlpha.pixel(offset_center) * (2 * sum_X - area)/static_cast<double>(area);
            const key_type res = op_constraint(imin.pixel(offset_center), imAlpha.pixel(offset_center));
            priority_queue.push_buffered(res, offset_center);
            assert(work_priority.pixel(offset_center) == 0.);
            work_priority.pixel(offset_center) = res;
          }





  #if 0


          //std::cout << "(15) : size = " << priority_queue.size();


          // inserting new points with modified priority
          // adjusting queued points priority with the new constraint
          temporary_queue1.clear();
          int toto = 0;
          while(!temporary_queue2.empty())
          {
            const offset_t offset_center = temporary_queue2.front();
            temporary_queue2.pop_front();

            // label provisoire (wait_for_first_pass) du centre : ce sont les points e_Queued
            const t_label label_center = imout.pixel(offset_center);

            // compute the ball
            neighSEOut.setCenter(offset_center);
            t_it_label_ball it_ball(neighSEOut.begin());
            const t_it_label_ball it_ball_end(neighSEOut.end());
            op_constraint.reset();

            const Label w_center = work.pixel(offset_center);

            UINT16 sum_X = 0;
            for( ; it_ball!= it_ball_end; ++it_ball)
            {
              const offset_t offset_neighbor = it_ball.Offset();
              const t_label label_neighbor = imout.pixel(offset_neighbor);
              const Label w_neighbor = work.pixel(offset_neighbor);


  #if 0

              // we compute the constraint on the center point
              if(op_filter(label_center, w_center, label_neighbor, w_neighbor))
              {
                // en esperant que le compilo comprendra ce qu'on souhaite faire
                op_constraint.push_new_point(imin.pixel(offset_neighbor), offset_neighbor);
              }

              // the easy update should not depend on the local configuration
              if(op_filter.neighbor_need_update(label_center, w_center, label_neighbor, w_neighbor))
              {
                if(constraint_operator::easy_update)
                {
                  work_priority.pixel(offset_neighbor) += op_constraint.update(
                    imin.pixel(offset_neighbor), 
                    imAlpha.pixel(offset_neighbor));
                }

                // pushing points that need updade, but not twice
                if(std::find(temporary_queue1.begin(), temporary_queue1.end(), offset_neighbor) == temporary_queue1.end())
                {
                  temporary_queue1.push_back(offset_neighbor);
                }
              }
  #else

              if(offset_neighbor == offset_center)
                continue;


              if(w_neighbor == labelQueued)
              {
                if(label_neighbor == label_center)
                {
                  work_priority.pixel(offset_neighbor) -= (imAlpha.pixel(offset_neighbor) * 2.)/static_cast<double>(area);
                  //sum_X ++;
                  if(std::find(temporary_queue1.begin(), 
                      temporary_queue1.end(), 
                      offset_neighbor) == temporary_queue1.end())
                  {
                    temporary_queue1.push_back(offset_neighbor);
                  }
                }
                
              }
              else if(w_neighbor == labelDone)
              {
                if(label_neighbor == label_center) sum_X ++;
              }

  #endif
            } // for the ball

            //const key_type res = op_constraint(imin.pixel(offset_center), imAlpha.pixel(offset_center));
            double res = imin.pixel(offset_center) - imAlpha.pixel(offset_center) * (2 * sum_X - area)/static_cast<double>(area);
            priority_queue.push_buffered(res, offset_center);
            work_priority.pixel(offset_center) = res;
          }


          // adjusting neighbors
          while(!temporary_queue1.empty())
          {
            const offset_t offset_center = temporary_queue1.front();
            temporary_queue1.pop_front();


  #if 0
            // non easy update: means we should update completely the neighbors
            // without this time cycling on neighbor's neighbors update :)
            // the code below should be correctly discarded by the compiler for the appropriate cases
            if(!constraint_operator::easy_update)
            {
              const t_label label_center = imout.pixel(offset_center);
              neighSEOut.setCenter(offset_center);
              t_it_label_ball it_ball(neighSEOut.begin());
              const t_it_label_ball it_ball_end(neighSEOut.end());
              op_constraint.reset();
              const Label w_center = work.pixel(offset_center);
              for( ; it_ball!= it_ball_end; ++it_ball)
              {
                const offset_t offset_neighbor = it_ball.Offset();
                const t_label label_neighbor = imout.pixel(offset_neighbor);
                const Label w_neighbor = work.pixel(offset_neighbor);

                // we compute the constraint on the center point
                if(op_filter(label_center, w_center, label_neighbor, w_neighbor))
                {
                  // en esperant que le compilo comprendra ce qu'on souhaite faire
                  op_constraint.push_new_point(imin.pixel(offset_neighbor), offset_neighbor);
                }


              } // for the ball

              const key_type res = op_constraint(imin.pixel(offset_center), imAlpha.pixel(offset_center));
              priority_queue.push_buffered(res, offset_center);
              work_priority.pixel(offset_center) = res;

            } // not easy update
            else
            {
              // this case: updated points can be present several time inside the queue
              priority_queue.push_buffered(work_priority.pixel(offset_center), offset_center);
            }
  #else
            priority_queue.push_buffered(work_priority.pixel(offset_center), offset_center);
  #endif


          }
  #endif


  #endif
          std::cout << "P";

          // ok this is the end of the plateau, we can continue to the next
          priority_queue.top_plateau_pop();


          cleaning_inc ++;
          if(cleaning_inc == 200)
          {
            cleaning_inc = 0;
            t_priority_queue_type priority_queue_temp;

            typename work_image_type::iterator w_it = work.begin();
            const typename work_image_type::iterator w_ite = work.end();
            for(; w_it != w_ite; ++w_it)
            {
              const offset_t offset = w_it.Offset();
              const Label lab = *w_it;
              if(lab == labelQueued || lab == labelQueued2)
                priority_queue_temp.push(work_priority.pixel(offset), offset);
            }

            std::cout << 'x';
            priority_queue.swap(priority_queue_temp);
          }






        } // while !priority_queue.empty()
        
  #if 0
        std::cout << "end image...";
        t_ImCompareOp_sss(work, operationCompare_Equal<Label, Label>(), labelDone, 255, 0, imtemp);
        t_ImCompareOp_ssi(work, operationCompare_Equal<Label, Label>(), labelQueued, 50, imtemp, imtemp);
        t_ImCompareOp_ssi(work, operationCompare_Equal<Label, Label>(), labelQueued2, 100, imtemp, imtemp);
        pngFileWrite(
          &imtemp, 
          filesystem::joinPaths(root_path, string("trace_viscous_watershed_") + AnyToStringFormatted(i_file++, 5, '0') + string(".png")));
  #endif
        return yayi::yaRC_ok;
      }







      //! viscous watershed for balls defined by images
      template <class t_im_gradient, class t_im_label, class t_im_alpha>
        yaRC t_ImViscousWatershed_v2(
          const t_im_gradient& imin,
          const t_im_label& imLabels,
          const t_im_alpha& imAlpha,
          const selement::NeighborList &nl,
          const Image<UINT8> &ballSEIm,
          t_im_label& imout)
      {
        typedef Image<UINT8> t_im_ball_se;

        // Boules et voisinages de grande taille (Images voisinage)
        // Warning: reduce the ball to the real dimension of the image (unless it won't iterate)
        typedef ImageSE<typename t_im_ball_se::value_type, t_im_ball_se::dimension>	ball_type;

        // this works because 1/2 = 0 (so, the center is not outside the image)
        const typename t_im_ball_se::coordinate_system center_point = ballSEIm.Size() / 2;
        ball_type ball_se(ballSEIm, center_point, selement::SEBorderTypeClip);


        return t_ImViscousWatershed_v2(imin, imLabels, imAlpha, nl, ball_se, imout);
      }



      //! viscous watershed for balls defined by images
      template <class t_im_gradient, class t_im_label>
        yaRC t_ImViscousWatershed_v2_constant_alpha(
          const t_im_gradient& imin,
          const t_im_label& imLabels,
          const float alpha,
          const selement::NeighborList &nl,
          const Image<UINT8> &ballSEIm,
          t_im_label& imout)
      {
        typedef Image<UINT8> t_im_ball_se;

        // Boules et voisinages de grande taille (Images voisinage)
        // Warning: reduce the ball to the real dimension of the image (unless it won't iterate)
        typedef ImageSE<typename t_im_ball_se::value_type, t_im_ball_se::dimension>	ball_type;

        // this works because 1/2 = 0 (so, the center is not outside the image)
        const typename t_im_ball_se::coordinate_system center_point = ballSEIm.Size() / 2;
        ball_type ball_se(ballSEIm, center_point, selement::SEBorderTypeClip);


        return t_ImViscousWatershed_v2_constant_alpha(imin, imLabels, alpha, nl, ball_se, imout);
      }














      class IGloballyConstraintModifier
      {
      public:

        virtual ~IGloballyConstraintModifier(){};

        //! Initialize the class
        virtual yaRC initialize(const std::deque<offset_t> &offset_list_init) = 0;

        //! 
        virtual yaRC priority_modifier(const offset_t position, yaF_double &priority) = 0;

        virtual yaRC new_point(const offset_t position) = 0;
        virtual yaRC new_points(const std::deque<offset_t>) = 0;

        virtual yaRC update() = 0;

      };


      typedef enum e_global_modification_type
      {
        gmt_color_hue,
        gmt_color_weighted_hue,
        gmt_barycentric,
        gmt_nothing
      } global_modification_type;

      class IGloballyConstraintModifierFactory
      {
        typedef IGloballyConstraintModifier* concrete_constraint_type;
        virtual IGloballyConstraintModifier* create(global_modification_type, CVariant label) = 0;
        virtual ~IGloballyConstraintModifierFactory(){};


      };

      
      
      
      struct op_diff_hue_minus_one_exp : public std::unary_function<yaF_double, yaF_double>
      {
        yaF_double operator()(yaF_double hue_diff) const
        {
          hue_diff = std::exp(hue_diff);
          hue_diff-= 1;
          return hue_diff;
        }
      };

      template <class t_label_type, class hue_image_type, class operator_diff_hue = op_diff_hue_minus_one_exp>
        struct s_hue_constraint /*: public IGloballyConstraintModifier*/
      {
      public:

        typedef yaF_double result_type;


        s_hue_constraint():hue_image(0), d_average_arg(0), ui32_nb_element(0), d_accu_real(0.),d_accu_imag(0.)
        {}
        
        s_hue_constraint(const hue_image_type& im) : 
          hue_image(const_cast<hue_image_type*>(&im)),
          d_average_arg(0), ui32_nb_element(0), d_accu_real(0.),d_accu_imag(0.)
        {}

        s_hue_constraint(const s_hue_constraint& hue_const) : 
          hue_image(const_cast<hue_image_type*>(hue_const.hue_image)),
          d_average_arg(hue_const.d_average_arg), ui32_nb_element(hue_const.ui32_nb_element), 
          d_accu_real(hue_const.d_accu_real), d_accu_imag(hue_const.d_accu_imag)
        {}
        
        ~s_hue_constraint()
        {}

        //! Called each time a point is strongly labelled into a region
        //! The internal distribution is updated accordingly
        yaRC new_point(const offset_t off)
        {
          ui32_nb_element ++;
          const yaF_double hue = hue_image->pixel(off);
          d_accu_real += cos(hue);
          d_accu_imag += sin(hue);
          return yaRC_ok;
        }

        //! Called each time a point is strongly labelled into a region
        //! The internal distribution is updated accordingly
        yaRC new_points(const std::deque<offset_t> l_off)
        {
          for(std::deque<offset_t>::const_iterator it = l_off.begin(), ite = l_off.end();
            it != ite;
            ++it)
          {
            new_point(*it);
          }
          return yaRC_ok;
        }

        //! Called once the region has been updated
        yaRC update()
        {
          d_average_arg = std::arg(std::complex<yaF_double>(d_accu_real / ui32_nb_element, d_accu_imag / ui32_nb_element));
          if(d_average_arg < 0) d_average_arg += 2*MPI;
          return yaRC_ok;
        }

        //! Called each time a new point should be inserted into the priority queu
        //! the priority is modified according to a metric with an internal distribution
        yaF_double priority_modifier(const offset_t offset_point) const
        {
          double d_delta_H = d_average_arg, dummy;
          d_delta_H-= hue_image->pixel(offset_point);
          if(d_delta_H < 0.) 
            d_delta_H = -d_delta_H;

          d_delta_H/= 2.*static_cast<double>(MPI);
          d_delta_H = std::modf( d_delta_H, &dummy );
          d_delta_H*= 2.;
          if(d_delta_H > 1.)
          {
            d_delta_H = 2.-d_delta_H;
          }
          operator_diff_hue op;
          return op(d_delta_H);
        }

        yaRC initialize(const std::deque<offset_t> &offset_list_init)
        {

          yaRC res = new_points(offset_list_init);
          if(res != yaRC_ok)
            return res;


          /*typename hue_image_type::coordinate_system coord;
          t_GetCoordsFromOffset(*hue_image, *offset_list_init.begin(), coord);
          std::cout << "First position init is : " << coord << std::endl;*/

          res = update();
          /*std::cout << "internal values are updated to : \n\td_average_arg : " << d_average_arg 
            << "\n\td_average_arg (degres): " << 360.*d_average_arg / (2 * MPI)
            << "\n\tui32_nb_element : " << ui32_nb_element
            << "\n\td_accu_real" << d_accu_real
            << "\n\td_accu_imag" << d_accu_imag << std::endl;*/

          return res;
        }


      private:
        hue_image_type *hue_image;
        yaF_double d_average_arg;
        UINT32 ui32_nb_element;
        yaF_double d_accu_real, d_accu_imag;



      };

      template <class t_label_type, class weighted_hue_image_type, class operator_diff_hue = op_diff_hue_minus_one_exp>
        struct s_weighted_hue_constraint /*: public IGloballyConstraintModifier*/
      {
      public:

        typedef yaF_double result_type;


        s_weighted_hue_constraint(): 
          w_hue_image(0), 
          d_average_arg(0), d_accu_saturation(0.), d_accu_real(0.),d_accu_imag(0.)
        {}
        s_weighted_hue_constraint(const weighted_hue_image_type& im) : 
          w_hue_image(const_cast<weighted_hue_image_type*>(&im)), 
          d_average_arg(0), d_accu_saturation(0.), d_accu_real(0.),d_accu_imag(0.)
        {
        }
        s_weighted_hue_constraint(const s_weighted_hue_constraint& w_hue_const) : 
          w_hue_image(const_cast<weighted_hue_image_type*>(w_hue_const.hue_image)),
          d_average_arg(w_hue_const.d_average_arg), d_accu_saturation(w_hue_const.d_accu_saturation), 
          d_accu_real(w_hue_const.d_accu_saturation),d_accu_imag(w_hue_const.d_accu_saturation)
        {
        }

        ~s_weighted_hue_constraint()
        {
        }

        //! Called each time a point is strongly labelled into a region
        //! The internal distribution is updated accordingly
        yaRC new_point(const offset off)
        {
          const typename weighted_hue_image_type::value_type w_hue = w_hue_image->pixel(off);
          const yaF_double d_sat = w_hue.channel3;
          d_accu_saturation += d_sat;
          d_accu_real += d_sat*cos(w_hue.channel1);
          d_accu_imag += d_sat*sin(w_hue.channel1);
          return yaRC_ok;
        }

        //! Called each time a point is strongly labelled into a region
        //! The internal distribution is updated accordingly
        yaRC new_points(const std::deque<offset_t> l_off)
        {
          for(std::deque<offset_t>::const_iterator it = l_off.begin(), ite = l_off.end();
            it != ite;
            ++it)
          {
            new_point(*it);
          }
          return yaRC_ok;
        }

        //! Called once the region has been updated
        yaRC update()
        {
          if(d_accu_saturation == 0) 
            d_average_arg = 0.;
          else
          {
            d_average_arg = std::arg(std::complex<yaF_double>(d_accu_real / d_accu_saturation, d_accu_imag / d_accu_saturation));
            if(d_average_arg < 0) d_average_arg += 2*MPI;
          }
          return yaRC_ok;
        }

        //! Called each time a new point should be inserted into the priority queu
        //! the priority is modified according to a metric with an internal distribution
        yaF_double priority_modifier(const offset_t offset_point) const
        {
          double d_delta_H = d_average_arg, dummy;
          d_delta_H -= (w_hue_image->pixel(offset_point)).channel1;
          if(d_delta_H < 0.) 
            d_delta_H = -d_delta_H;

          d_delta_H/= 2.*static_cast<double>(MPI);
          d_delta_H = std::modf( d_delta_H, &dummy );
          d_delta_H*= 2.;
          if(d_delta_H > 1.)
          {
            d_delta_H = 2.-d_delta_H;
          }
          operator_diff_hue op;
          return op(d_delta_H);
        }

        yaRC initialize(const std::deque<offset> &offset_list_init)
        {
          yaRC res = new_points(offset_list_init);
          if(res != yaRC_ok)
            return res;

          return update();
        }


      private:
        weighted_hue_image_type *w_hue_image;
        yaF_double d_average_arg;
        yaF_double d_accu_real, d_accu_imag, d_accu_saturation;
      };


      //! Simple factory class for constraint on hue homogeneity
      template <class t_label_type, class hue_image_type>
        struct s_hue_constraint_factory /*: public IGloballyConstraintModifierFactory*/
      {
        //! Constraint type returned by the factory class
        typedef s_hue_constraint<t_label_type, hue_image_type>	constraint_type;
        typedef boost::shared_ptr< constraint_type>					concrete_constraint_type;


        //! The class should be initialized with an external hue image, on which the priority
        //! modification will be computed
        s_hue_constraint_factory(const hue_image_type& im) : hue_image(&im){}


        //! Factory function. Returns always the same type of modifier
        concrete_constraint_type create(global_modification_type, CVariant ) const
        {
          return concrete_constraint_type(new constraint_type(*hue_image)); 
        }

      private:
        const hue_image_type *hue_image;
      };




      //! Simple factory class for constraint on hue homogeneity, with saturation weighting factor
      template <class t_label_type, class weighted_hue_image_type>
        struct s_weighted_hue_constraint_factory /*: public IGloballyConstraintModifierFactory*/
      {
        //! Constraint type returned by the factory class
        typedef s_weighted_hue_constraint<t_label_type, weighted_hue_image_type>	constraint_type;
        typedef boost::shared_ptr<constraint_type>									concrete_constraint_type;


        //! The class should be initialized with an external hue image, on which the priority
        //! modification will be computed
        s_weighted_hue_constraint_factory(const weighted_hue_image_type& im) : w_hue_image(&im){}


        //! Factory function. Returns always the same type of modifier
        concrete_constraint_type create(global_modification_type, CVariant ) const
        {
          return concrete_constraint_type(new constraint_type(*w_hue_image)); 
        }

      private:
        const weighted_hue_image_type *w_hue_image;
      };


      //! Utility class for testing purposes
      template <class t_label_type>
        struct s_predicate_find_first_offset
      {
        const offset_t off_to_find;
        s_predicate_find_first_offset(const offset_t & off) : off_to_find(off){}
        bool operator()(const std::pair<std::pair<offset_t, offset_t>, t_label_type> &val) const
        {
          return val.first.first == off_to_find;
        }

      };


      template <class image>
        struct s_remove_if_from_image
      {
        const image& im;
        const typename image::value_type value;
        s_remove_if_from_image(const image& _im, const typename image::value_type _value) : im(_im), value(_value){}

        bool operator()(const offset_t off) const throw()
        {
          return im.pixel(off) == value;
        }
      };

      template <class image_type, class priority_type, bool b_need_cleaning = true>
        struct s_priority_queue_cleaning_helper
      {

        s_priority_queue_cleaning_helper(const image_type& im_work, const UINT16 steps) 
          : work_priority(), cleaning_inc(0), cleaning_inc_step(steps)
        {
          work_priority = im_work.template t_getSameImage<work_priority_image_type>();
          if(t_ImSetConstant(work_priority, DataTraits<priority_type>::default_value::background()) != yaRC_ok)
            YAYI_THROW("s_priority_queue_cleaning_helper:constructor : error during the call of t_ImSetConstant");
        }

        void insert_point(const offset_t off, const priority_type& prior)
        {
          work_priority.pixel(off) = prior;
        }

        bool need_update(const offset_t& off, const priority_type& prior) const
        {
          return work_priority.pixel(off) != prior;
        }

        bool is_priority_accurate(const offset_t& off, const priority_type& prior) const
        {
          return work_priority.pixel(off) == prior;
        }


        template <class priority_queue_type>
          void clean_priority_queue(
          const typename s_from_type_to_type<image_type,Label>::image_type &work,
          priority_queue_type& queue)
        {
          typedef typename s_from_type_to_type<
            image_type,
            Label>::image_type work_image_type;
          
          cleaning_inc++;
          if(cleaning_inc < cleaning_inc_step)
            return;

          cleaning_inc = 0;
          priority_queue_type priority_queue_temp;

          for(typename work_image_type::const_iterator w_it = work.begin(), w_ite = work.end(); 
            w_it != w_ite; 
            ++w_it)
          {
            const offset_t offset = w_it.Offset();
            const Label lab = *w_it;
            if(lab == labelQueued || lab == labelQueued2)
              priority_queue_temp.push(work_priority.pixel(offset), offset);
          }

          queue.swap(priority_queue_temp);
        }


      private:
        typedef typename s_from_type_to_type<
          image_type,
          priority_type>::image_type work_priority_image_type;
        work_priority_image_type work_priority;
        UINT16 cleaning_inc;
        const UINT16 cleaning_inc_step;
      };


      // same signature as above, but does nothing
      template <class image_type, class priority_type>
        struct s_priority_queue_cleaning_helper<image_type, priority_type, false>
      {

        s_priority_queue_cleaning_helper(const image_type& , const UINT16 ) throw()
        {}

        void insert_point(const offset_t& , const priority_type& ) const throw()
        {}

        bool need_update(const offset_t& , const priority_type& ) const throw()
        {
          return false;
        }

        bool is_priority_accurate(const offset_t& off, const priority_type& prior) const throw()
        {
          return true;
        }

        template <class priority_queue_type>
          void clean_priority_queue(
          const typename s_from_type_to_type<image_type,Label>::image_type &work,
          priority_queue_type& queue) const throw()
        {}
      };


      //! Pareil que "Héhéhé", sans l'update lors de l'ajout de points. Je sens que ca va aller, mais vraiment vachement plus vite
      template <class t_im_gradient, class t_im_label, class t_im_alpha, class constraint_factory_type, bool b_update>
        yaRC t_ImGloballyConstrainedWatershedNoUpdate(
          const t_im_gradient& imin,
          const t_im_label& imLabels,
          const t_im_alpha& imAlpha,
          const selement::NeighborList	&nl,
          const constraint_factory_type &constraint_factory,
          t_im_label& imout)
      {

        // general value types
        typedef typename t_im_label::value_type		t_label;
        typedef typename t_im_alpha::value_type		t_alpha;


        // the contraint operator type
        typedef typename constraint_factory_type::constraint_type				contraint_operator_type;
        typedef typename contraint_operator_type::result_type					key_type;
        typedef typename constraint_factory_type::concrete_constraint_type		concrete_constraint_type;
        typedef std::map<typename t_im_label::value_type, concrete_constraint_type>		constraint_map_type;

        // work and priority images
        typedef typename s_from_type_to_type<t_im_alpha,Label>::image_type		work_image_type;

        // list of offset of different kinds
        typedef std::deque< offset_t >											off_queue_type;
        typedef std::set< offset_t >											off_set_type;
        typedef std::map< t_label, off_set_type >								map_front_list_type;
        typedef std::map< t_label, off_queue_type >								map_region_list_type;
        typedef std::deque< std::pair<offset_t, t_label> >						t_first_pass_queue;
        typedef std::deque< std::pair<std::pair<offset_t, offset_t>, t_label> > t_first_pass_discovered;
        typedef common_priority_queue<key_type, offset_t >						t_priority_queue_type;




        if(		!t_CheckOffsetCompatible(imin, imout) 
          ||	!t_CheckOffsetCompatible(imin, imLabels)
          ||	!t_CheckOffsetCompatible(imin, imAlpha))
          return yayi::yaRC_E_bad_size;			

        yaRC res;
        

        // work image
        work_image_type work = imin.template t_getSame<Label>();
        
        // priority image; this version of the flooding allows the modification of the priority during the flooding process
        //work_priority_image_type work_priority = imin.template t_getSame<key_type>();

        s_priority_queue_cleaning_helper<work_image_type, key_type, b_update>		priority_queue_cleaning_operator(work, 2000);
        
        // constant values
        const t_label lpeVal = DataTraits<t_label>::default_value::background();
        const t_label label_value_background = DataTraits<t_label>::default_value::background();

        // for debugging purposes
  #ifdef __WATERSHED_VISQUEUX_FILE_OUT__
        if(t_ImDimension(work) > 2)
        {
          YAYI_THROW("t_ImGloballyConstrainedWatershedNoUpdate : Cannot trace : image of dimension > 2");
        }

        // raffi: cette ligne foirera la compil de toute manière si on fait le con
        Image<UINT8> imtemp = work.template t_getSame<UINT8>();
        int	i_file = 0;
        UINT32 nb_pixels_between_each_trace = (UINT32)(t_SizePixel(work) * 1. / 100), i_counter = 0;
        work.ColorInfo() = ciMonoSpectral;
  #endif


        // Compute the histogram for the label image
        std::map<t_label, UINT32> histogram;
        res = stats::t_measHistogram(imLabels, histogram);
        if(res != yaRC_ok)
        {
          DEBUG_INFO("t_ImGloballyConstrainedWatershedNoUpdate: error in t_measHistogram(imLabels, histogram)");
          return res;
        }


        // create constraint modifiers
        map_front_list_type		map_front_list;
        map_region_list_type	map_region_list;
        constraint_map_type		map_constraint;
        for(typename std::map<t_label, UINT32>::const_iterator it = histogram.begin(), ite = histogram.end();
          it != ite;
          ++it)
        {
          if(it->first == label_value_background) continue;
          map_constraint[it->first] = constraint_factory.create(gmt_color_weighted_hue /* dummy gmt */, it->first /* dummy label */);
        }


        // I do not think i'll keep these lines...
        t_ImBorderSetConstant(imout, label_value_background);
        t_ImBorderSetConstant(work, labelWatershed);
        //t_ImBorderSetConstant(work_priority, 0.);
        


        // do not forget this line: very important indeed
        res = copy_image_t(imLabels, imout);
        if(res != yaRC_ok)
        {
          DEBUG_INFO("t_ImGloballyConstrainedWatershedNoUpdate: error in copy_image_t(imLabels, imout)");
          return res;
        }

        res = t_ImSetConstant(work, labelCandidate);
        if(res != yaRC_ok)
        {
          DEBUG_INFO("t_ImGloballyConstrainedWatershedNoUpdate: error in t_ImSetConstant : work");
          return res;
        }


        // neighbor graph for propagating (NeighborList)
        typedef Neighborhood<NeighborList, t_im_label> t_imlabel_neigh;
        t_imlabel_neigh neighb_out(imout,nl);

        typedef Neighborhood<NeighborList, work_image_type > t_work_neigh;
        t_work_neigh work_neighb(work, nl);
        typename t_work_neigh::iterator	wit, wend;


        // queues
        t_priority_queue_type			priority_queue;
        t_first_pass_queue				temporary_queue_pfp;
        t_first_pass_discovered			temporary_queue_pfp2;
        std::deque<offset_t>			temporary_queue1, temporary_queue_neigh, temporary_queue_watershed;


        // init part

        typename t_im_label::iterator out_it = imout.begin();
        const typename t_im_label::iterator out_it_end = imout.end();
        for(;out_it != out_it_end; ++out_it) 
        {
          const t_label label_center = *out_it;

          // background points are neutral
          if(label_center == label_value_background)
            continue;

          const offset_t offset_center = out_it.Offset();


          // neighborhood test : we use the neighborhood to determine wheather the point is watershed or not
          bool b_is_watershed = false;
          temporary_queue1.clear();

          if(neighb_out.setCenter(out_it) != yaRC_ok)
            YAYI_THROW("neighb_out.setCenter failed");
          typename t_imlabel_neigh::const_iterator		nit(neighb_out.begin_const());
          const typename t_imlabel_neigh::const_iterator	nend(neighb_out.end_const());
          for( ; nit != nend; ++nit)
          {
            const offset_t offset = nit.Offset();
            
            /* on teste les voisins, pas le point en cours */
            if(offset == offset_center) 
              continue;
          
            const t_label label_neighbor = *nit;

            // we don't handle the case neighbor = watershed point because imOut is updated during this pass 
            if(label_neighbor != label_value_background)
            {
              if(label_neighbor != label_center)
              {
                b_is_watershed = true;
                break;
              }
            }
            else
              temporary_queue1.push_back(offset);
          }


          
          if(b_is_watershed)
          {
            // the point belongs to the watershed, we don't push it into the queue
            // but mark imout and imwork accordingly
            work.pixel(offset_center) = labelWatershed;
            imout.pixel(offset_center) = lpeVal;
          }
          else
          {

            // the point does not belong to the watershed: we process its neighbors
            work.pixel(offset_center) = labelDone;
            
            // already done in the copy_image_t
            //imout.pixel(offset_center) = label_center;
            assert(imout.pixel(offset_center) == label_center);

            // update the region
            map_region_list[label_center].push_back(offset_center);

            while(!temporary_queue1.empty())
            {
              const offset_t offset = temporary_queue1.front();
              temporary_queue1.pop_front();
              if(work.pixel(offset) == labelCandidate)
              {
                work.pixel(offset) = labelQueued;

                // update the front of the corresponding region
                map_front_list[label_center].insert(offset);
                temporary_queue_pfp.push_back(typename t_first_pass_queue::value_type(offset, label_center));
              }
            }
          }
        } // for all points of imout

        
        
        
        // update the forces with the region list points:
        for(typename map_region_list_type::const_iterator it = map_region_list.begin(), ite = map_region_list.end();
          it != ite;
          ++it)
        {
          res = map_constraint[it->first]->initialize(it->second);
          if(res != yaRC_ok)
          {
            DEBUG_INFO("Error during initializing of a priority modifier");
            return res;
          }

        }
        map_region_list.clear();
        


        // update the front points, and insert them into the queue after modification of the priority
        for(typename t_first_pass_queue::const_iterator it = temporary_queue_pfp.begin(), it_e = temporary_queue_pfp.end();
          it != it_e;
          ++it)
        {
          const offset_t offset_center = it->first;
          const t_label label_center = it->second;
          imout.pixel(offset_center) = label_center;
          assert(work.pixel(offset_center) == labelQueued);


          const key_type res = imin.pixel(offset_center) + imAlpha.pixel(offset_center) * map_constraint[label_center]->priority_modifier(offset_center);
          priority_queue.push(res, offset_center);

          priority_queue_cleaning_operator.insert_point(offset_center, res);
        }



        // process the queue
        while(!priority_queue.empty())
        {

          // priority order
          typename t_priority_queue_type::iterator it_plateau = priority_queue.top_plateau_begin();
          const typename t_priority_queue_type::iterator it_plateau_end = priority_queue.top_plateau_end();

          const key_type current_priority = it_plateau.key();
          temporary_queue_pfp.clear();
          temporary_queue_pfp2.clear();
          temporary_queue_watershed.clear();

          for(;it_plateau != it_plateau_end; ++it_plateau)
          {
            bool b_is_watershed = false, b_is_labeled = false;
            const offset_t offset_center = it_plateau.data();

            if(!priority_queue_cleaning_operator.is_priority_accurate(offset_center, current_priority))
              continue;
  #if 1
            t_label label_center = lpeVal;
  #else
            t_label label_center;
  #endif

            temporary_queue1.clear();
            temporary_queue_neigh.clear();
            work_neighb.setCenter(offset_center);
            wit = work_neighb.begin();
            wend= work_neighb.end();

            for(; wit != wend; ++wit)
            {
              const offset_t offset = wit.Offset();

              // discard the center point
              if(offset == offset_center) continue;
              const Label state_neighbor = *wit;
      
              if(state_neighbor == labelCandidate)
              {
                temporary_queue1.push_back(offset);
              }								
              
              else if(state_neighbor == labelDone)
              {
                if(b_is_labeled)
                {
                  // has alredy a 'done' neighbor
                  assert(label_center != lpeVal);
                  const t_label label_neighbor = imout.pixel(offset);
                  
                  if((label_neighbor != label_center) && (label_neighbor != label_value_background))
                  {
                    assert(imout.pixel(offset) != 0);
                    // no further computing, the point is watershed
                    b_is_watershed = true;
                    break;
                  }
                }
                else
                {
                  label_center = imout.pixel(offset);
                  b_is_labeled = true;
                }
              }
              
              else if(state_neighbor == labelQueued)
              {
                // the neighbor is also in the queue, we should further process this point
                temporary_queue_neigh.push_back(offset);
              }
              else
                //assert(state_neighbor == labelWatershed);
                if(state_neighbor != labelWatershed)
                  YAYI_THROW("Unknown configuration");

            } // for all neighbors


            if(!b_is_watershed)
            {

              for(std::deque<offset_t>::const_iterator it = temporary_queue_neigh.begin(), ite = temporary_queue_neigh.end();
                it != ite;
                ++ it)
              {

                const offset_t offset = *it;

                // if the neighbor's temporary label is different and the priorities matches, we have a thick watershed line
                const t_label weak_label = imout.pixel(offset);

                

                // ajout de la condition b_is_labeled
                if(weak_label != label_center/*imout.pixel(offset_center)*/)
                {

                  // priorité + ou - alpha par rapport à la priorité courante: on suppose alors que les points appartiennent
                  // au même niveau.
                  
                  if(current_priority >= imin.pixel(offset))
                  {
                    // no further computing, the point is watershed
                    // do not forget b_is_labeled
                    b_is_labeled = b_is_watershed = true;

                    // can break there since we do not change the state of neighbor points
                    break;
                                          
                    // the weak neighbor is flagged as 'watershed to be'
                    //work.pixel(offset) = labelQueued2;
                    //temporary_queue_watershed.push_back(offset);
                    
                  }
                }
              }
            }

            if(b_is_watershed)
            {
              // the point is watershed, we discard the neighbors and mark it accordingly
              // temporary_queue1.clear(); -> already done before the parsing of each neighborhood
              //if(b_is_labeled)
              temporary_queue_watershed.push_back(offset_center);
            }
            else if(label_center != label_value_background) // which means b_is_labeled
            {
              // the point is not watershed, we wait before inserting the neighbors into the queue
              // label is strong now
              
              // important: we cannot modify work at this point. It will be later used for the modification
              // of priorities
              assert(label_center != label_value_background);
              temporary_queue_pfp.push_back(typename t_first_pass_queue::value_type(offset_center, label_center));

              // the discovered neighbors : they are put inside another queue, for later insertion into the HQ
              while(!temporary_queue1.empty())
              {
                const offset_t offset = temporary_queue1.front();
                temporary_queue1.pop_front();

                // we cannot push the points into the main queue nor can we change work
                // since it will be used for the computation of new priorities
                temporary_queue_pfp2.push_back(std::make_pair(std::make_pair(offset, offset_center), label_center));

              }

            } // if/else watershd point
            else
            {
              if(true/*b_intended_for_removal*/)
              {
                typename t_im_label::coordinate_system coord;
                t_GetCoordsFromOffset(work, offset_center, coord);
                std::cout << "Un point non labelisé découvert en (2) : " << coord << std::endl;
              }
            }

            
          } // end of the current plateau


          // update the watershed points
          //typedef std::map< t_label, std::set<offset_t> > map_fast_look_type;
          //map_fast_look_type map_region_set;
          for(std::deque<offset_t>::const_iterator it = temporary_queue_watershed.begin(), ite = temporary_queue_watershed.end();
            it != ite;
            ++it)
          {
            const offset_t offset_center = *it;

            const t_label old_label = imout.pixel(offset_center);

            // test if already labelled
            //if(old_label == lpeVal)
            //	continue;
            if(work.pixel(offset_center) == labelWatershed) 
              continue;

            
            // put the point into watershed state
            imout.pixel(offset_center) = lpeVal;
            work.pixel(offset_center) = labelWatershed;
            //map_region_set[old_label].insert(offset_center);
            map_front_list[old_label].erase(offset_center);
          }

          
  #if 0
          // removal of watershed points from the front point lists
          for(typename map_front_list_type::iterator it = map_front_list.begin(), ite = map_front_list.end();
            it != ite;
            ++it)
          {

            if(map_region_set.count(it->first) == 0) 
              continue;


            off_list_type &current_list = it->second;
            std::set<offset_t> &current_set = map_region_set[it->first];
            std::deque<typename off_list_type::iterator> element_to_erase;
            for(typename off_list_type::iterator itl = current_list.begin(), itle = current_list.end();
              itl != itle;
              ++itl)
            {
              std::set<offset_t>::iterator it_set = current_set.find(*itl);
              if(it_set != current_set.end())
              //if(work.pixel(*itl) == labelWatershed)
              {
                element_to_erase.push_back(itl);
                //(it->second).erase(itl);
                current_set.erase(it_set);
                if(current_set.empty()) 
                  break;
              }
            }
            for(typename std::deque<typename off_list_type::iterator>::iterator itl = element_to_erase.begin(), itle = element_to_erase.end();
              itl != itle;
              ++itl)
            {
              current_list.erase(*itl);
            }

          }
          map_region_set.clear();
  #endif




          // update of the strongly labelled points
          map_region_list.clear();
          for(typename t_first_pass_queue::const_iterator it = temporary_queue_pfp.begin(), ite = temporary_queue_pfp.end();
            it != ite;
            ++it)
          {
            const offset_t offset_center = it->first;
            const t_label label = it->second;

            work.pixel(offset_center) = labelDone;
            imout.pixel(offset_center) = label;		// normalement pas besoin de cette ligne
            //map_region_set[it->second].insert(offset_center);
            map_front_list[label].erase(offset_center);
            map_region_list[label].push_back(offset_center);

  #ifdef __WATERSHED_VISQUEUX_FILE_OUT__
              // trace sur le nombre de points ajoutés
              i_counter += 1;
              if(i_counter % nb_pixels_between_each_trace == 0)
              {
                std::cout << '.';
                t_ImCompareOp_sss(work, operationCompare_Equal<Label, Label>(), labelDone, 255, 0, imtemp);
                t_ImCompareOp_ssi(work, operationCompare_Equal<Label, Label>(), labelQueued, 50, imtemp, imtemp);
                t_ImCompareOp_ssi(work, operationCompare_Equal<Label, Label>(), labelQueued2, 100, imtemp, imtemp);
                pngFileWrite(
                  &imtemp, 
                  filesystem::joinPaths(root_path, string("trace_viscous_watershed_") + AnyToStringFormatted(i_file++, 5, '0') + string(".png")));
                
                
                std::cout << 'o';
                pngFileWrite(
                  &imout, 
                  filesystem::joinPaths(root_path, string("out_trace_viscous_watershed_") + AnyToStringFormatted(i_file++, 5, '0') + string(".png")));
              }
  #endif
          }


          // update of the discovered points
          // push the discovered points into temporary_queue_pfp
          temporary_queue_pfp.clear();
          for(typename t_first_pass_discovered::const_iterator it = temporary_queue_pfp2.begin(), ite = temporary_queue_pfp2.end();
            it != ite;
            ++it)
          {
            const offset_t offset_discovered	= it->first.first;
            const offset_t offset_source		= it->first.second;


            // the source point became watershed
            if(work.pixel(offset_source) == labelWatershed)
              continue;
            if(work.pixel(offset_discovered) != labelCandidate)
              continue;

            work.pixel(offset_discovered) = labelQueued;
            imout.pixel(offset_discovered) = it->second;
            temporary_queue_pfp.push_back(std::make_pair(offset_discovered, it->second));


          }






          // removal of the strongly labelled points (voir si on peut mettre ca av les machins watershed)
          // put them in the update lists

  #if 0
          //s_remove_if_from_image<work_image_type> op_erase_done_points(work, labelDone);
          for(typename map_front_list_type::iterator it = map_front_list.begin(), ite = map_front_list.end();
            it != ite;
            ++it)
          {

            const t_label label_center = it->first;
            if(map_region_set.count(label_center) == 0) 
              continue;


  #if 0
            //std::cout << "it->first : " << it->first << std::endl;
            //std::cout << "it->second : " << &(it->second) << std::endl;

            

            off_list_type &current_list = it->second;

            typename off_list_type::iterator it_new_end = remove_if(current_list.begin(), current_list.end(), op_erase_watershed_points);
            typename off_list_type::iterator itl = it_new_end, itle = current_list.end();
            for(itl = it_new_end; itl != itle; ++itl)
            {
              const offset_t offset_center = *itl;
              const t_label label_center = imout.pixel(offset_center);
              map_update_list[label_center].push_back(offset_center);
            }
            current_list.erase(it_new_end, itle);


  #else
            std::list<offset_t> current_list;
            std::set<offset_t> &current_set = map_region_set[label_center];
            off_list_type& current_front_list = it->second;
            std::deque<typename off_list_type::iterator> element_to_erase;
            for(typename off_list_type::iterator itl = current_front_list.begin(), itle = current_front_list.end();
              itl != itle;
              ++itl)
            {
              const offset_t offset_center = *itl;
              //std::cout << "offset_center : " << offset_center << std::endl;
              //if(work.pixel(offset_center) == labelDone)
              std::set<offset_t>::iterator it_set = current_set.find(offset_center);
              if(it_set != current_set.end())
              {
                //const t_label label_center = imout.pixel(offset_center);
                //(it->second).erase(itl);

                

                element_to_erase.push_back(itl);
                current_list.push_back(offset_center);

                if(b_intended_for_removal)
                { // intended for removal
                  
                  if(map_constraint.count(it->first) == 0)
                    YAYI_THROW("Trying to push update for an unknown label : " + AnyToString(it->first));
                }

                current_set.erase(it_set);
                if(current_set.empty()) 
                  break;


              }
            }

            for(typename std::deque<typename off_list_type::iterator>::iterator itl = element_to_erase.begin(), itle = element_to_erase.end();
              itl != itle;
              ++itl)
            {
              current_front_list.erase(*itl);
            }

            map_update_list[label_center] = current_list;
  #endif
          }






  #endif
          // update the forces with the newly strongly labelled points
          for(typename map_region_list_type::const_iterator it = map_region_list.begin(), ite = map_region_list.end();
            it != ite;
            ++it)
          {
            res = map_constraint[it->first]->new_points(it->second);
            if(res != yaRC_ok)
              YAYI_THROW("Error (yaRC) returned from the new_points function : " 
              + getErrorUnderstandableName(res) 
              + ", label :" + AnyToString(it->first));

            res = map_constraint[it->first]->update();
            if(res != yaRC_ok)
              YAYI_THROW("Error (yaRC) returned from the update function : " 
              + getErrorUnderstandableName(res) 
              + ", label :" + AnyToString(it->first));

          }


          if(b_update)
          {
            // update of the known front points with the nerw forces
            // only for regions who witnessed a modification
            for(typename map_region_list_type::const_iterator it = map_region_list.begin(), ite = map_region_list.end();
              it != ite;
              ++it)
            {
              const t_label label_center = it->first;
              const typename map_front_list_type::mapped_type &list_front = map_front_list[label_center];//it->second;

              for(typename map_front_list_type::mapped_type::const_iterator itl = list_front.begin(), itle = list_front.end();
                itl != itle;
                ++itl)
              {
                const offset_t offset_center = *itl;
                const key_type res = imin.pixel(offset_center) + imAlpha.pixel(offset_center) * map_constraint[label_center]->priority_modifier(offset_center);

                if(priority_queue_cleaning_operator.need_update(offset_center, res))
                {
                  priority_queue.push_buffered(res, offset_center);
                  priority_queue_cleaning_operator.insert_point(offset_center, res);
                }
              }
            }
          }

          // push the new points into the queue
          for(typename t_first_pass_queue::const_iterator it = temporary_queue_pfp.begin(), ite = temporary_queue_pfp.end();
            it != ite;
            ++it)
          {
            const offset_t	offset_center = it->first;
            const t_label	label_center = it->second;
            
            const key_type res = imin.pixel(offset_center) + imAlpha.pixel(offset_center) * map_constraint[label_center]->priority_modifier(offset_center);
            priority_queue.push_buffered(res, offset_center);
            priority_queue_cleaning_operator.insert_point(offset_center, res);
            map_front_list[label_center].insert(offset_center);

          }

          temporary_queue_pfp.clear();

          // ok this is the end of the plateau, we can continue to the next
          priority_queue.top_plateau_pop();


          // priority queue cleaner, for algorithms doubling points in the queue
          priority_queue_cleaning_operator.clean_priority_queue(work, priority_queue);



          std::cout << ".";



        } // while !priority_queue.empty()


  #ifdef __WATERSHED_VISQUEUX_FILE_OUT__

        std::cout << "end image...";
        t_ImCompareOp_sss(work, operationCompare_Equal<Label, Label>(), labelDone, 255, 0, imtemp);
        t_ImCompareOp_ssi(work, operationCompare_Equal<Label, Label>(), labelQueued, 50, imtemp, imtemp);
        t_ImCompareOp_ssi(work, operationCompare_Equal<Label, Label>(), labelQueued2, 100, imtemp, imtemp);
        pngFileWrite(
          &imtemp, 
          filesystem::joinPaths(root_path, string("trace_viscous_watershed_") + AnyToStringFormatted(i_file++, 5, '0') + string(".png")));
                
        std::cout << 'o';
        pngFileWrite(
          &imout, 
          filesystem::joinPaths(root_path, string("out_trace_viscous_watershed_") + AnyToStringFormatted(i_file++, 5, '0') + string(".png")));
  #endif
        return yayi::yaRC_ok;
      }








      template < 
        class t_image_gradient, 
        class t_image_label,
        class t_image_alpha,
        class SE,
        class t_hue_image_type>
      yaRC t_ImGlobalHueConstrainedWatershed(
        const t_image_gradient& im_gradient,
        const t_image_label &im_label,
        const t_image_alpha &im_alpha, 
        const SE& nl,
        const t_hue_image_type& im_hue,
        t_image_label &im_out)
      {
        typedef s_hue_constraint_factory<
          typename t_image_label::value_type,
          t_hue_image_type> constraint_factory_operator;

        constraint_factory_operator op(im_hue);

        /*return t_ImGloballyConstrainedWatershed(
          im_gradient,
          im_label,
          im_alpha,
          nl,
          op,
          im_out);*/
        return t_ImGloballyConstrainedWatershedNoUpdate<t_image_gradient, t_image_label, t_image_alpha, constraint_factory_operator, true>(
          im_gradient,
          im_label,
          im_alpha,
          nl,
          op,
          im_out);

      }


      template < 
        class t_image_gradient, 
        class t_image_label,
        class t_image_alpha,
        class SE,
        class t_weighted_hue_image_type>
      yaRC t_ImGlobalWeightedHueConstrainedWatershed(
        const t_image_gradient& im_gradient,
        const t_image_label &im_label,
        const t_image_alpha &im_alpha, 
        const SE& nl,
        const t_weighted_hue_image_type& im_hue,
        t_image_label &im_out)
      {
        typedef s_weighted_hue_constraint_factory<
          typename t_image_label::value_type,
          t_weighted_hue_image_type> constraint_factory_operator;

        constraint_factory_operator op(im_hue);

        /*return t_ImGloballyConstrainedWatershed(
          im_gradient,
          im_label,
          im_alpha,
          nl,
          op,
          im_out);*/
        return t_ImGloballyConstrainedWatershedNoUpdate<t_image_gradient, t_image_label, t_image_alpha, constraint_factory_operator, true>(
          im_gradient,
          im_label,
          im_alpha,
          nl,
          op,
          im_out);

      }



      template < 
        class t_image_gradient, 
        class t_image_label,
        class t_image_alpha,
        class SE,
        class t_hue_image_type>
      yaRC t_ImGlobalHueConstrainedWatershedNoUpdate(
        const t_image_gradient& im_gradient,
        const t_image_label &im_label,
        const t_image_alpha &im_alpha, 
        const SE& nl,
        const t_hue_image_type& im_hue,
        t_image_label &im_out)
      {
        typedef s_hue_constraint_factory<
          typename t_image_label::value_type,
          t_hue_image_type> constraint_factory_operator;

        constraint_factory_operator op(im_hue);

        return t_ImGloballyConstrainedWatershedNoUpdate<t_image_gradient, t_image_label, t_image_alpha, constraint_factory_operator, false>(
          im_gradient,
          im_label,
          im_alpha,
          nl,
          op,
          im_out);

      }


      template < 
        class t_image_gradient, 
        class t_image_label,
        class t_image_alpha,
        class SE,
        class t_weighted_hue_image_type>
      yaRC t_ImGlobalWeightedHueConstrainedWatershedNoUpdate(
        const t_image_gradient& im_gradient,
        const t_image_label &im_label,
        const t_image_alpha &im_alpha, 
        const SE& nl,
        const t_weighted_hue_image_type& im_hue,
        t_image_label &im_out)
      {
        typedef s_weighted_hue_constraint_factory<
          typename t_image_label::value_type,
          t_weighted_hue_image_type> constraint_factory_operator;

        constraint_factory_operator op(im_hue);

        return t_ImGloballyConstrainedWatershedNoUpdate<t_image_gradient, t_image_label, t_image_alpha, constraint_factory_operator, false>(
          im_gradient,
          im_label,
          im_alpha,
          nl,
          op,
          im_out);

      }



//! @} doxygroup: seg_details_grp

















  }
}

#endif /* YAYI_VISCOUS_SEGMENTATION_HPP__ */
