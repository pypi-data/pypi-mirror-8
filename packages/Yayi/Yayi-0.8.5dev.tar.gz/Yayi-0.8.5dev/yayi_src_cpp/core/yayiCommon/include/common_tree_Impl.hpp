#ifndef YAYI_COMMON_TREE_IMPL_HPP__
#define YAYI_COMMON_TREE_IMPL_HPP__

/*!@file
 * @brief  Implementation details of common/simple node and n_tree
 * @author Thomas Retornaz
 */


namespace yayi
{

  /*!@defgroup common_tree_details_grp Tree Details
   * @ingroup common_tree_grp
   * @{
   */

  template<typename dataType>
  string_type commonNode<dataType>::GetStringRep() const
  {
    std::stringstream  os;
    os<<"\t"<<"{ "<<m_data<<" }\n";
    const_itChildren it=m_children.begin(), iend=m_children.end();
    for(; it != iend ; ++it)
    {
      os<<(*it)->GetStringRep();
    }
    return os.str();
  }




  template <typename dataType>
  const size_t  commonNode<dataType>::GetDepth() const
  {
    size_t depth = 0;
    for( const_itChildren it=m_children.begin(); it!=m_children.end(); it++ )
    {
      depth = std::max<size_t>( depth, (*it)->GetDepth() );
    }
    return depth + 1;
  }

  //warning the caller have the responsibility of the deletion if requested
  template <typename dataType>
  bool commonNode<dataType>::RemoveChild( this_type* rnode )
  {
    //check rnode in release?
    DEBUG_ASSERT(rnode != 0, "search for null pointer");

    itChildren pos = std::find(m_children.begin(), m_children.end(), rnode );
    if ( pos != m_children.end() )
    {
      m_children.erase(pos);
      rnode->SetParent(NULL);
      return true;
    }
    return false;

  }

  template <typename dataType>
  void commonNode<dataType>::AddChild( this_type* rhs)
  {
    //precondition
    DEBUG_ASSERT(rhs != NULL, "provided node is NULL");
    DEBUG_ASSERT(rhs != this, "try to assign self as child node");
    DEBUG_ASSERT( !this->HasChildren( rhs ),"provided node is already a child");

    rhs->SetParent(this);
    m_children.push_back(rhs);
  }

  template <typename dataType>
  void commonNode<dataType>::AddChild(const_reference rhs)
  {
    this_type* newNode=new this_type(rhs);
    AddChild(newNode);
  }



  //warning current node take ownsherpip of rnode children
  template <typename dataType>
  void commonNode<dataType>::MergeChildsFrom( this_type* rnode )
  {
    //check rnode in release ?
    DEBUG_ASSERT(rnode != 0, "update from null pointer");
    //make this adaptable to over container?
    m_children.splice( m_children.begin(), rnode->GetChildren() );
  }

  
  /******************* commonTree impl template part **********************/


  //TR idea stolen from http://www.aei.mpg.de/~peekas/tree/
   
  /**
   * @brief Base class for iterators, only pointers storage and
   * deferencement op
   */
  template<
    class dataType, 
    class innerNode = commonNode<dataType> 
    >
  class const_iterator_base : public std::iterator<std::bidirectional_iterator_tag, dataType>
  {
  public:
    //typedef std::iterator<std::bidirectional_iterator_tag, dataType> parent_class;

    typedef commonTree<dataType,innerNode>              tree_type;
    typedef innerNode                                   node_type;
    typedef node_type*                                  pointer_node;
    typedef const node_type*                            const_pointer_node;
    typedef node_type&                                  reference_node;
    typedef const node_type&                            const_reference_node;

    typedef dataType value_type;
    typedef dataType& reference;
    typedef dataType* pointer;
    typedef const dataType* const_pointer;
    typedef const dataType& const_reference;
    typedef std::bidirectional_iterator_tag                 iterator_category;



    //! Default constructor
    const_iterator_base():
      m_node(0), 
      m_tree(0)
    {}

    //! Copy constructor
    const_iterator_base(const const_iterator_base&rhs):
      m_node(rhs.m_node),
      m_tree(rhs.m_tree)
    {}

    //! "Generalized" copy constructor
    template<typename other>
    const_iterator_base(const other&rhs):
      m_node(rhs.m_node),
      m_tree(rhs.m_tree)
    {}

    // should be protected and not in public happy just help to set iterator state
    const_iterator_base(const tree_type* tree, const node_type* current):
      m_node(current), 
      m_tree(tree)
    {}

    ~const_iterator_base()
    {}
    
    //! Assignment
    const_iterator_base& operator=(const const_iterator_base& rhs)
    {
      //test self assignment
      if(this == &rhs)
        return *this;
      m_node = rhs.m_node;
      m_tree = rhs.m_tree;
      return *this;
    }

    //! Generalized assignment operator
    template<class other>
    const_iterator_base& operator=(const other& rhs)
    {
      //test self assignment
      if ((this)==&rhs) 
        return *this; //never occur anyway
      m_node=rhs.m_node;
      m_tree=rhs.m_tree;
      return *this;
    }

    const_reference operator*() const
    {
      //check inner node in release ?
      DEBUG_ASSERT(m_node != 0, "iterator wrap a null pointer");
      return (*m_node).GetData();
        //->data();
    }

    const_pointer operator->() const 
    {
      //check inner node in release ?
      DEBUG_ASSERT(m_node != 0, "iterator wrap a null pointer");
      return &((*m_node).GetData());
    }

    const_reference_node current_node() const
    {
      //check inner node in release ?
      DEBUG_ASSERT(m_node != 0, "iterator wrap a null pointer");
      return (*m_node);
    }                         

    /// Number of childs of the node pointed to by the iterator.
    //@warning just first hierarchy level
    size_t GetNumberOfChilds()
    {
      //check inner node in release ?
      DEBUG_ASSERT(m_node != 0, "iterator wrap a null pointer");
      return m_node->GetNumberOfChilds();
    }

    operator bool() const
    {
      return (m_node!=NULL);
    }

  protected:
     const node_type*  m_node;//!<started node
     const tree_type* m_tree;//!<keep ref on visited tree
  };


  //also know as Depth-first Traversal
  template<class dataType,class innerNode>
  class const_preorder_iterator:public const_iterator_base<dataType,innerNode>
  {
  public:
    typedef const_iterator_base<dataType,innerNode> parent_class;
    typedef commonTree<dataType,innerNode>              tree_type;
    typedef innerNode                                   node_type;
    typedef node_type*                                  pointer_node;
    typedef const node_type*                            const_pointer_node;
    typedef node_type&                                  reference_node;
    typedef const node_type&                            const_reference_node;

    typedef dataType value_type;
    typedef dataType& reference;
    typedef dataType* pointer;
    typedef const dataType* const_pointer;
    typedef const dataType& const_reference;
    typedef std::bidirectional_iterator_tag                 iterator_category;
    
    // typedef typename parent_class::tree_type tree_type;
    // typedef typename parent_class::node_type node_type;
    // typedef typename parent_class::pointer_node pointer_node;

    // typedef typename parent_class::const_pointer_node const_pointer_node;
    // typedef typename parent_class::reference_node reference_node;
    // typedef typename parent_class::const_reference_node const_reference_node;

    using parent_class::m_node;
    using parent_class::m_tree;

    //! Default constructor
    const_preorder_iterator():parent_class(),m_stack(){}


    //should be protected and not in public api just help to set iterator state
    const_preorder_iterator(const tree_type* tree,const pointer_node current):parent_class(tree,current),m_stack(){}

    //!"generalized" copy ctor
    template<class other>
    const_preorder_iterator(const other& rhs):parent_class(rhs)
    {
      //remove constiness
      other& localNonConst=const_cast<other&>(rhs);
      copyStack(localNonConst.m_stack,m_stack);
    }

    //!copy ctor 
    const_preorder_iterator (const const_preorder_iterator& rhs):parent_class(rhs)
    {
      //remove constiness
      const_preorder_iterator &localNonConst=const_cast<const_preorder_iterator&>(rhs);
      copyStack(localNonConst.m_stack,m_stack);
    }


    //!dtor
    ~const_preorder_iterator(){} 



    bool operator == (const const_preorder_iterator& rhs) const
    {
      // Not check entire stack check because it costly
      // check current node and stack size
      // note that checking node check all sub node in debug
      if (m_tree==rhs.m_tree && m_node== rhs.m_node && m_stack.size() == rhs.m_stack.size())
      {
#ifdef _DEBUG
        //implement full check of stack
        //if (m_stack!=m_node.m_stack) return false; //ok for visual ?

#endif
        return true;
      }
      return false;
    }

    bool operator != (const const_preorder_iterator& rhs) const       {return (! operator == (rhs)); }

    //! Generalized copy assignment operator
    template<class other>
    const const_preorder_iterator& operator=(const other& rhs)
    {
        //test self assignment
        if ((this)==&rhs) return *this; //never occur anyway
        //copy current node and tree
        parent_class::operator=(rhs);            
        //remove constiness
        const_preorder_iterator &localNonConst=const_cast<other&>(rhs); //not safe ?
        copyStack(localNonConst.m_stack,m_stack);
        return (*this);
      }

    //! Copy assignment operator
    const const_preorder_iterator& operator = (const const_preorder_iterator& rhs)
    {
      //test self assignment
      if ((this)==&rhs) return *this;
      parent_class::operator=(rhs);
      //remove constiness
      const_preorder_iterator &localNonConst=const_cast<const_preorder_iterator&>(rhs);
      copyStack(localNonConst.m_stack,m_stack);
      return (*this);
    }
    const_preorder_iterator& operator ++ () {return incr();}
    const_preorder_iterator operator ++(int) { const_preorder_iterator tmp(*this); ++*this; return tmp; }
    const_preorder_iterator& operator --() { return dcr(); }
    const_preorder_iterator operator --(int) { const_preorder_iterator tmp(*this); --*this; return tmp; }

  protected:
    std::stack<pointer_node> m_stack;//!<internal stack to store  traversal
     
  private:
    void copyStack(std::stack<pointer_node> & inputStack,std::stack<pointer_node> & ouputStack)//inputStack is no const for facility
    {
      //empty ouput stack
      while (!ouputStack.empty())
      {
        ouputStack.pop();
      }
      //copy temp in other container we must take care of insertion order stack note also that stack has no swap facility
      std::vector<pointer_node> tmp;
      tmp.reserve(inputStack.size());
      while (! inputStack.empty() )
      {
        tmp.push_back ( inputStack.top() );
        inputStack.pop();
      }
      //then copy reverse
      typedef typename std::vector<pointer_node>::reverse_iterator ritVec;
      ritVec rit=tmp.rbegin(),ritend=tmp.rend();
      for(;rit!=ritend;++rit)
      {
        inputStack.push(*rit);
        ouputStack.push(*rit);
      }
    }

    const_preorder_iterator& incr()
    {
      // put the current' nodes children on the stack, and 
      // then move onto the next one by popping it
      // off the stack and making it the current one 

      //if current node exist
      if (m_node)
      {//put all children on stack (reverse order)               
        typedef typename node_type::containerTypeChildren containerTypeChildren;
        containerTypeChildren children((*m_node).GetChilds());
        typedef typename containerTypeChildren::const_reverse_iterator ritVec;

        ritVec rit=children.rbegin(),ritend=children.rend();
        for ( ;rit!=ritend;rit++)
        {
          m_stack.push(*rit);// a bit ugly
        }
      }
      //if stack is not empty return new current node
      if (!m_stack.empty() ) 
      {
        m_node = m_stack.top();
        m_stack.pop(); 
      }
      else // assume we end the container 
      {
        *this = m_tree->const_preorder_end(); 
      }
      return *this; 
    } //end incr

    const_preorder_iterator& dcr()
    {
      typedef typename node_type::containerTypeChildren containerTypeChildren;
      typedef typename containerTypeChildren::const_reverse_iterator ritVec;
      typedef typename containerTypeChildren::const_iterator itVec;

      //if current node exist
      if (m_node)
      {
        //is root
        if (m_node==m_tree->GetRoot()) 
          {
            *this = m_tree->const_preorder_begin(); 
            return *this; 
          }

        itVec findCurrentNode=std::find(m_node->GetParent()->GetChilds().begin(),m_node->GetParent()->GetChilds().end(),m_node);
        DEBUG_ASSERT(findCurrentNode!=m_node->GetParent()->GetChilds().end(),"Current node not found in is proper list");
        //is not first slibbing ?
        if  (findCurrentNode!=m_node->GetParent()->GetChilds().begin())
        {
          //go backward
          findCurrentNode--;
          m_node=*findCurrentNode;
          if ((*findCurrentNode)->HasChilds()) { // childs?
            do { // true  
              m_stack.push(*findCurrentNode); // first push current node
              findCurrentNode = m_node->GetChilds().end();
              findCurrentNode--;  // then go to last child
              m_node=*findCurrentNode;
            } while ( (*findCurrentNode)->HasChilds() ); // while childs present
          }
        }
        else
        {
          //if stack is not empty return new current node
          if (!m_stack.empty() )  //bug ??      
          { 
            //first slibbing go to parent node
            m_node = m_stack.top();
            m_stack.pop(); 
          }
        }
      }
      else // assume we start from the end of tree
      { //populate stack just before end
       
        //get root
        typename tree_type::const_pointer_node root=m_tree->GetRoot();
        DEBUG_ASSERT(root!=NULL,"Tree has not root");
        //get childs from root   
        //we have to restart from root and go deeply in the tree to find last subchilds
        //start at root
        m_node=root;
        ////degenerate case root alone
        //if (!(m_node->HasChilds()))
        //{
        //   *this = m_tree->const_preorder_end(); 
        //    return *this; 
        //}
        m_stack.push((const pointer_node)root); // first push current node

        itVec findCurrentNode = m_node->GetChilds().end();
        //is not first slibbing ?
        if  (findCurrentNode!=m_node->GetChilds().begin())
        {
          //go backward
          findCurrentNode--;
          m_node=*findCurrentNode;
          if ((*findCurrentNode)->HasChilds()) { // childs?
            do { // true  
              m_stack.push(*findCurrentNode); // first push current node
              findCurrentNode = m_node->GetChilds().end();
              findCurrentNode--;  // then go to last child
              m_node=*findCurrentNode;
            } while ( (*findCurrentNode)->HasChilds() ); // while childs present
          }
        }
        else
        {
          //if stack is not empty return new current node
          if (!m_stack.empty() )  //bug ??     
          { 
            //first slibbing go to parent node
            m_node = m_stack.top();
            m_stack.pop(); 
          }
        }
      }
      return *this;
    }
  };

  template<class dataType,class innerNode>
  class preorder_iterator:public const_preorder_iterator<dataType,innerNode>
  {
public:
    typedef  const_preorder_iterator<dataType,innerNode> parent_class;

    //!Default ctor
    preorder_iterator():parent_class(){}

    //!copy ctor
    preorder_iterator(const preorder_iterator& rhs):parent_class(rhs) {}

    //!copy assignment operator
    const preorder_iterator& operator = (const preorder_iterator& rhs)
    {
      parent_class::operator =(rhs);
      return *this;
   }

    //!generalized copy assignment operator
    template<class other>
    const preorder_iterator& operator = (/*const*/ other& rhs)
    {
      parent_class::operator =(rhs);
      return *this;

    }

    template<class other>
        //!generalized copy ctor
        preorder_iterator(const other& rhs):parent_class/*<other>*/(rhs)
        {
        }


    //!dtor
    ~preorder_iterator(){} //empty

   /*!
    * @name overloaded operators
    * @{
    */
    preorder_iterator& operator ++() { ++(*static_cast<parent_class*>(this)); return *this; }
    preorder_iterator operator ++(int) { preorder_iterator tmp(*this); ++*this; return tmp; }
    preorder_iterator operator --() { --(*static_cast<parent_class*>(this)); return *this; }
    preorder_iterator operator --(int) { preorder_iterator tmp(*this); --*this; return tmp; }
    //@} //overloaded

    /*!
     * @name public interface
     * @{
     */
    typename parent_class::value_type& operator*() { return  const_cast<typename parent_class::value_type&>(parent_class::operator *());}

    typename parent_class::value_type* operator->() { return const_cast<typename parent_class::value_type*>(parent_class::operator ->());}

    typename parent_class::reference_node current_node()
    {
      return const_cast<typename parent_class::reference_node>(parent_class::current_node());
    }
    //@} //public interface

 // protected:
    //should be protected and not in public happy just help to set iterator state
    preorder_iterator(typename parent_class::tree_type* tree,typename parent_class::pointer_node current):parent_class(tree,current){}

  }; //preorder_iterator

  template<class dataType,class innerNode>
  string_type commonTree<dataType,innerNode>::GetStringRep() const
  {
    std::stringstream  os;
    const_preorder_iterator it=const_preorder_begin();
    if (it)
      os<<it.current_node();
    return os.str();
  }

  template<class dataType,class innerNode>
  commonTree<dataType,innerNode>::~commonTree()
  {
    delete m_root;    
  }

  template<class dataType,class innerNode>
  commonTree<dataType,innerNode>::commonTree(const_reference data)
  {
    node_type * node = new node_type(data);
    // update
    node->SetParent( NULL ); 
    m_root=node;
  }


  template<class dataType,class innerNode>
  void commonTree<dataType,innerNode>::SetRoot(pointer_node rnode)
  {
    if(m_root)
    {
      YAYI_THROW("Tree has already a root");
    }
    if (!rnode)
    {
      YAYI_THROW("Provided node is null");
    }
    m_root=rnode;
  }

  template<class dataType,class innerNode>
  typename commonTree<dataType,innerNode>::const_pointer_node commonTree<dataType,innerNode>::GetRoot() const
  {
    if(!m_root)
    {
      YAYI_THROW("Tree has no root");
    }
    return m_root;
  }

  //! @} // common_tree_details_grp
}//end namespace yayi

#endif //YAYI_COMMON_TREE_IMPL_HPP__
