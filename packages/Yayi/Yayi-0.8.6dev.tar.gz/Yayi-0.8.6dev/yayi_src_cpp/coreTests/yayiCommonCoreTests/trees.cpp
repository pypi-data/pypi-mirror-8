#include "main.hpp"


#include <yayiCommon/include/common_tree.hpp>
#include <yayiCommon/common_variant.hpp>

BOOST_AUTO_TEST_SUITE(trees)

BOOST_AUTO_TEST_CASE(node_class)
{

  typedef yayi::commonNode<int> intNode;
  //default construction node is root with no leaf aka alone in the world :)
  intNode node(0);
  
  //std::cout<<"Empty lonely node\n"<<node;

  BOOST_CHECK(node.GetParent()==NULL);
  BOOST_CHECK_EQUAL(node.GetNumberOfChilds(),static_cast<size_t>(0));
  BOOST_CHECK_EQUAL(node.IsRoot(),true);
  BOOST_CHECK_EQUAL(node.IsLeaf(),true);
  
  //add child
  intNode* child0=(intNode*)0;
  intNode* child1=(intNode*)0;
  intNode* child10=(intNode*)0;

  child0=new intNode(1);
  child1=new intNode(2);
  child10=new intNode(3);

  node.AddChild(child0);
  node.AddChild(child1);
  (*child1).AddChild(child10);

  BOOST_CHECK(node.GetParent()==NULL);
  BOOST_CHECK_EQUAL(node.GetNumberOfChilds(),static_cast<size_t>(2)); //direct children not subchildren
  BOOST_CHECK_EQUAL(node.IsRoot(),true);
  BOOST_CHECK_EQUAL(node.IsLeaf(),false);

  //child0 doesnt have child
  BOOST_CHECK(child0->GetParent()==&node);
  BOOST_CHECK_EQUAL(child0->GetNumberOfChilds(),static_cast<size_t>(0)); //direct children not subchildren
  BOOST_CHECK_EQUAL(child0->IsRoot(),false);
  BOOST_CHECK_EQUAL(child0->IsLeaf(),true);

  //child1 has 1 child
  BOOST_CHECK(child1->GetParent()==&node);
  BOOST_CHECK_EQUAL(child1->GetNumberOfChilds(),static_cast<size_t>(1)); //first level childs not subchilds
  BOOST_CHECK_EQUAL(child1->IsRoot(),false);
  BOOST_CHECK_EQUAL(child1->IsLeaf(),false);

  //child10
  BOOST_CHECK(child10->GetParent()==child1);
  BOOST_CHECK_EQUAL(child10->GetNumberOfChilds(),static_cast<size_t>(0)); //first level childs not subchilds
  BOOST_CHECK_EQUAL(child10->IsRoot(),false);
  BOOST_CHECK_EQUAL(child10->IsLeaf(),true);

  (*child10).AddChild((int)5); //create child node from data 

  //std::cout<<"Grand father node\n"<<node;
  //deletions of nodes is done by dtor of node
   
}

BOOST_AUTO_TEST_CASE(tree)
{
  typedef yayi::commonTree<std::string> stree;

  stree tree;
  typedef stree::node_type node_type;

  //intTree::const_preorder_iterator it=emptyTree.const_preorder_begin(),itend=emptyTree.const_preorder_end();
  node_type* root =new node_type("A");
  tree.SetRoot(root);

  //add child
  node_type* child1=(node_type*)0;

  child1=new node_type("B");

  (*root).AddChild("C");
  (*root).AddChild(child1);
  (*child1).AddChild("D");
}

BOOST_AUTO_TEST_CASE(tree_iterator)
{
  typedef yayi::commonTree<int> intTree;
  intTree tree;
  typedef intTree::node_type node_type;
  node_type* root =new node_type(0);
  tree.SetRoot(root);
  
  //we have a tree with a root but no children
  intTree::const_preorder_iterator it;
  intTree::const_preorder_iterator itend;
  //add child
  node_type* child1=(node_type*)0;
  child1=new node_type(2);
  (*root).AddChild(1);
  (*root).AddChild(child1);
  (*child1).AddChild(3);

  //std::cout<<"treeIt"<<tree; 
  it=tree.const_preorder_begin();
  itend=tree.const_preorder_end();
  //std::cout<<std::endl<<std::endl;
  //std::cout<<"tree iterate begin->end";
  //for (;it!=itend;it++)
  //  std::cout<<*it<<"\t";

  //std::cout<<std::endl<<std::endl;
  //std::cout<<"treeIterator operator<<"<<tree;


  it=tree.const_preorder_begin();
  itend=tree.const_preorder_end();
  //std::cout<<std::endl<<std::endl;

  //std::cout<<"tree iterate end->begin";

  if (it!=itend)
  {
    do
    {
      itend--;
      //std::cout<<*itend<<"\t";
    } while(it!=itend);
  }
}

BOOST_AUTO_TEST_CASE(tree_traversal_depthfirst)
{
   typedef yayi::commonTree<std::string> strTree;
   typedef strTree::node_type node_type;
   strTree::preorder_iterator it,itend;
   
   strTree tree("A");
   
   it=tree.begin();
   //add bcd above root
   it.current_node().AddChild("B");
   it.current_node().AddChild("C");
   it.current_node().AddChild("D");
   
   it=tree.begin();
   it++; //advance to B
   BOOST_CHECK_EQUAL(*it,"B");
   it.current_node().AddChild("E");
   it.current_node().AddChild("F");

   it=tree.end();
   it--; // D
   BOOST_CHECK_EQUAL(*it,"D");
   it.current_node().AddChild("G");
   it.current_node().AddChild("H");

//   std::cout<<std::endl<<std::endl;
//   std::cout<<"tree"<<tree;
   // A->H label of node
   // 0->7 order traversal
   //                  A(0)    
   //         B(1)     C(4)     D(5)
   //      E(2)  F(3)        G(6)   H(7)
   unsigned int index=0;
   it=tree.begin();
   itend=tree.end();
   std::vector<std::string> tabCorrect;
   tabCorrect.push_back("A");
   tabCorrect.push_back("B");
   tabCorrect.push_back("E");
   tabCorrect.push_back("F");
   tabCorrect.push_back("C");
   tabCorrect.push_back("D");
   tabCorrect.push_back("G");
   tabCorrect.push_back("H");

   for(;it!=itend;it++,index++)
     BOOST_CHECK_EQUAL(*it,tabCorrect[index]);
}

BOOST_AUTO_TEST_SUITE_END()


