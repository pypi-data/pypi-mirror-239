import pytest
from src.bstpackage import generateBST as GenBST

class Tests:

    def test_init(self):
        node1 = GenBST.TreeNode(5)
        node2 = GenBST.TreeNode(4)
        assert(node1 is not None)
        assert(node2 is not None)
        assert(node1.val  == 5)
        assert(node2.val  == 4)
    
    def test_init_child(self):
        node1 = GenBST.TreeNode(5)
        node2 = GenBST.TreeNode(4)
        assert(node1.left  is None)
        assert(node1.right is None)
        assert(node2.left  is None)
        assert(node2.right is None)

    # test insert #1
    def test_insert(self):
        root1 = GenBST.TreeNode(5)
        GenBST.insert(root1, 10)
        GenBST.insert(root1, 7)
        assert isinstance(root1.right, GenBST.TreeNode)
        assert (root1.right.val == 10)
        assert isinstance(root1.right.left, GenBST.TreeNode)
        assert (root1.right.left.val == 7)

    # test insert #2
    def test_insert2(self):
       root2 = GenBST.TreeNode(8)
       GenBST.insert(root2, 3)
       assert isinstance(root2.left, GenBST.TreeNode)
       assert root2.left.val == 3

    # test insert #3
    def test_insert3(self):
        root3 = GenBST.TreeNode(5)
        GenBST.insert(root3, 5)
        assert root3.val == 5
        assert root3.left is None
        assert root3.right is None

    # test delete #1 (no child)
    def test_delete1(self):
        root = GenBST.TreeNode(5)
        GenBST.insert(root, 10)
        GenBST.insert(root, 7)
        GenBST.delete(root, 7)
        assert (root.right.left is None)

    # test delete #2 (two child)
    def test_delete2(self):
        root = GenBST.TreeNode(10)
        GenBST.insert(root, 6)
        GenBST.insert(root, 14)
        GenBST.insert(root, 13)
        GenBST.insert(root, 18)
        GenBST.insert(root, 16)
        GenBST.delete(root, 14)
        assert (root.right.val == 16)

    # test delete #3 (one child)
    def test_delete3(self):
        root = GenBST.TreeNode(10)
        GenBST.insert(root, 6)
        GenBST.insert(root, 14)
        GenBST.insert(root, 12)
        GenBST.insert(root, 11)
        GenBST.insert(root, 13)
        GenBST.delete(root, 14)
        assert (root.right.val == 12)
        assert (root.right.left is not None)
        assert (root.right.left.val == 11)
        assert (root.right.right is not None)
        assert (root.right.right.val == 13)

    # test get_min_value() #1
    def test_get_min1(self):
        root = GenBST.TreeNode(10)
        GenBST.insert(root, 6)
        GenBST.insert(root, 14)
        GenBST.insert(root, 12)
        GenBST.insert(root, 11)
        assert (GenBST.get_min_value(root) == 6)
        assert (GenBST.get_min_value(root.right) == 11)
    
    # test get_min_value() #2
    def test_get_min2(self):
        root = GenBST.TreeNode(10)
        assert (GenBST.get_min_value(root) == 10)
    
    # test get_min_value() #3
    def test_get_min3(self):
        root = GenBST.TreeNode(10)
        GenBST.insert(root, 12)
        GenBST.insert(root, 8)
        GenBST.insert(root, 9)
        assert (GenBST.get_min_value(root) == 8)

    # test in_order_traversal #1
    def test_traversal1(self):
        root = GenBST.TreeNode(10)
        GenBST.insert(root, 12)
        GenBST.insert(root, 8)
        GenBST.insert(root, 9)
        assert (GenBST.io_traverse(root) == [8, 9, 10, 12])
    
    # test in_order_traversal #2
    def test_traversal2(self):
        root = GenBST.TreeNode(10)
        GenBST.insert(root, 6)
        GenBST.insert(root, 14)
        GenBST.insert(root, 12)
        GenBST.insert(root, 11)
        assert (GenBST.io_traverse(root) == [6, 10, 11, 12, 14])
    
    # test in_order_traversal #3
    def test_traversal3(self):
        root = GenBST.TreeNode(10)
        GenBST.insert(root, 6)
        GenBST.insert(root, 14)
        GenBST.insert(root, 12)
        GenBST.insert(root, 11)
        GenBST.delete(root, 14)
        assert (GenBST.io_traverse(root) == [6, 10, 11, 12])
