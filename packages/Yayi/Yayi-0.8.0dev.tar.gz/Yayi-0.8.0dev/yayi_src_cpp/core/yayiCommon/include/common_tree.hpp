#ifndef YAYI_COMMON_TREE_HPP__
#define YAYI_COMMON_TREE_HPP__

#include <yayiCommon/common_types.hpp>
#include <yayiCommon/common_errors.hpp>
//#include <yayiCommon/common_variant.hpp>
#include <iterator>
#include <list>
//#include <vector> //may be switch to vector for nodes storage
#include <stack>

#include <memory>
#include <algorithm>
#include <boost/utility.hpp>


#include <boost/type_traits/add_const.hpp>
#include <boost/type_traits/remove_reference.hpp>
#include <boost/type_traits/add_reference.hpp>

/**
 * @file   common_tree.hpp
 * @author Thomas Retornaz
 * @brief  Definition of common/simple node structures and N_tree
 * 
 * 
 */

//TR Note, this code is inspirated by previous implementation
//http://www.codeproject.com/script/Articles/ViewDownloads.aspx?aid=12822
//http://www.aei.mpg.de/~peekas/tree/
//http://www.codeproject.com/KB/library/tree_container.aspx
//and was rewritten from scratch

namespace yayi
{
  /*!@defgroup common_tree_grp Tree
   * @brief Tree structure suitable for @c MaxTree, @c ComponentTree
   * @ingroup common_grp
   * @{
   */

  // @todo add tests
  // @todo implement find/insert/remove 
  // @todo add allocator type
  // @todo use set instead of list ?

   
  /*!@brief Node structure used for N-level tree
   * @author Retornaz Thomas
   */
  template<typename dataType>
  class commonNode : boost::noncopyable
  {
  public:
    typedef dataType          value_type;
    typedef dataType*         pointer;
    typedef const dataType*   const_pointer;
    typedef dataType&         reference;
    typedef const dataType&   const_reference;

    typedef commonNode<dataType> this_type;
    typedef std::list<commonNode*> containerTypeChildren;
    typedef typename containerTypeChildren::iterator itChildren;
    typedef typename containerTypeChildren::const_iterator const_itChildren;
    typedef typename containerTypeChildren::reverse_iterator ritChildren;
    typedef typename containerTypeChildren::const_reverse_iterator const_ritChildren;
    
    
    /*!@name Object Creation/Destruction
     * @{
     */
    
    //! Empty constructor
    commonNode() : m_parent(0), m_children(), m_data()
    {}
    

    //! Constructor from data and (optional) parent node.
    commonNode(const_reference data, this_type* parent = 0) :
      m_parent(parent), m_data(data), m_children()
    {
    }


    ~commonNode()
    {
      for( const_itChildren it=m_children.begin(); it!=m_children.end(); it++ )
      {
        delete *it;
      }
      m_children.clear(); // Raffi: no need
    }

    //! Clones the current node (deep copy)
    this_type* Clone()
    {
      //TODO add try catch to avoid memory leak ?

      // create a new node
      this_type * root = new this_type(m_data);

      // clone the childs
      for(const_itChildren it = GetChilds().begin(); it != GetChilds().end(); it++ )
      {
        this_type * child = (*it)->Clone();
        root->AddChild( child );
      }
      return root;
    
    }
     
    //!@}

    /*!@brief Returns the parent node
     */
    const this_type* GetParent() const
    {
      return m_parent;
    }

    void SetParent(this_type* iParrent)
    {
      #ifndef NDEBUG
      if (iParrent !=NULL) //for sure parent could be null
        DEBUG_ASSERT(iParrent  != this, "try to assign self as parent node");
      #endif
      m_parent = iParrent ;
    }

    const containerTypeChildren& GetChilds() const
    {
      return m_children;
    }

    const bool IsLeaf() const
    {
      return m_children.empty();
    }


    const bool IsRoot() const
    {
      return m_parent == 0;
    }

    void SetData(const_reference iData)
    {
      m_data = iData;
    }

    const std::size_t GetNumberOfChilds() const
    {
      return m_children.size();
    }

    const_reference GetData() const
    {
      return m_data;
    }

    reference data()
    {
      return m_data;
    }


    bool operator==(const this_type& rhs) const
    {
      //check parent
      // Raffi: really ? In that case, the tree should be exactly the same
      // I do not think sharing the nodes accross trees is a good idea.
      if (rhs.m_parent != m_parent)
        return false;
      
      //check value
      // Raffi: this one may be costly
      if (rhs.data() != data())
        return false;
      
      //check size first
      // Raffi: this one is O(1)
      if (rhs.m_children.size() != m_children.size())
        return false;
      
      //then check content
      #ifndef NDEBUG
      //FIXME ONLY IN DEBUG maybe costly
      const_itChildren it= m_children.begin(), iend= m_children.end();
      const_itChildren itrhs=rhs.m_children.begin(), iendrhs=rhs.m_children.end();
      for(; it != iend, itrhs != iendrhs; ++it, ++itrhs) // no need of second inequality check, since same size
      {
        if(*it != *itrhs)
          return false;
      }
      #endif
      return true;
    }

    friend bool operator!=(const this_type& lhs,const this_type& rhs) 
    {
      return !(lhs == rhs);
    }

    const size_t GetDepth() const;

    bool RemoveChild( this_type* rnode );
    void AddChild(this_type* rnode);
    void AddChild(const_reference data);

    //! Checks if the provided node is a child of the current node
    //! @todo rename to is_child_of
    bool HasChildren( const this_type* rnode ) const
    {
      //check rnode in release?
      DEBUG_ASSERT(rnode != 0, "search for null pointer");
      return std::find(m_children.begin(), m_children.end(), rnode ) != m_children.end();    
    }
    
    bool HasChilds() const
    {
      return !m_children.empty();
    }
    
    void MergeChildsFrom( this_type* rnode );


  private:
    //! Parent node, may be 0 for the root
    this_type* m_parent;
    
    //! Data stored in the node
    dataType m_data;
    
    //! Children of the current node
    containerTypeChildren m_children;
    
    /*!@name Streaming methods
     * @{
     */
     
    /*!@brief Stringizer operator
     * @return a string describing the content of the node
     */
    string_type GetStringRep() const;

  public:
     
    template <class o_stream>
    friend o_stream& operator<<(o_stream& os,const commonNode<dataType>& rnode)
    {
      os<<rnode.GetStringRep();
      return os;
    }
    //!@} Streaming methods 

  };

  //predeclared iterator on tree structure
  template<class dataType,class innerNode>  class preorder_iterator;
  template<class dataType,class innerNode>  class const_preorder_iterator;

  //TODO add erase find insert facility (discuss ->at wich level ?)
   
  /*!@brief Tree structure used for N-level tree
   * @author Retornaz Thomas
   */
  template<class dataType,class innerNode=commonNode<dataType> >
  class commonTree:boost::noncopyable
  {
  public:
    typedef commonTree<dataType,innerNode> this_type;
    typedef typename innerNode::const_reference const_reference;
    typedef innerNode node_type;
    typedef node_type* pointer_node; 
    typedef const node_type* const_pointer_node;

    friend class preorder_iterator<dataType,node_type>;
    friend class const_preorder_iterator<dataType,node_type>;

    typedef typename yayi::const_preorder_iterator<dataType,node_type> const_preorder_iterator; //namespace required by gcc
    typedef typename yayi::preorder_iterator<dataType,node_type> preorder_iterator;

  private:
    /**
     * @brief Stringizer operator
     * 
     *  
     * @return a string representing the tree
     */
     string_type GetStringRep() const;

  public:
    
    /*!@name Object Creation/Destruction
     * @{
     */
     
    /*!@brief Constructor
     * @param root root of the tree.
     */
    explicit commonTree(pointer_node root) : m_root(root)
    {
      if (!root) YAYI_THROW("You must provide non null node");
    }

    //! ctor from data 
    explicit commonTree(const_reference data);

    //! Empty constructor.
    commonTree():m_root(0){};
    //pointer Clone();

    ~commonTree();
    //! @}
    
    
    /*!@brief Get Root Pointer
     *
     * @throw if root not set
     * @return const pointer to root node
     */
    const_pointer_node GetRoot() const;

   /**
    * @brief Set root node
    * @throw if provided node is NULL
    * @param rNode allocated node
    */
    void SetRoot(pointer_node rNode);

    
     
    /*!@name Streaming methods
     * @{
     */
    template <class o_stream>
    friend o_stream& operator<<(o_stream& os,const commonTree<dataType,innerNode>& rtree)
    {
      os << rtree.GetStringRep();
      return os;
    }
    //! @}
     
    /*!@name Iterator
     * @{
     */
    preorder_iterator preorder_begin()                        {return ( preorder_iterator( this, m_root) );}
    preorder_iterator preorder_end()                          {return (  preorder_iterator( this, NULL ) );}

    const_preorder_iterator   const_preorder_begin()  const   {return (  const_preorder_iterator( this, m_root) );}
    const_preorder_iterator   const_preorder_end()    const   {return (  const_preorder_iterator( this, NULL ) );}

    preorder_iterator begin()       {return preorder_begin();}
    preorder_iterator end()         {return preorder_end();}
    const_preorder_iterator begin()   const    {return const_preorder_begin();}
    const_preorder_iterator end()     const    {return const_preorder_end();}
    //! @}

  private:

    //! The root of the tree
    pointer_node m_root;
  };
  //@} // common_tree_grp

}//end namespace yayi

#include <yayiCommon/include/common_tree_Impl.hpp>

#endif //YAYI_COMMON_TREE_HPP__
