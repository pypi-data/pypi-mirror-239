import generateBST as GenBST


def main():
    root = GenBST.TreeNode(10)
    print(root.val)

    GenBST.insert(root, 12)
    GenBST.insert(root, 18)
    GenBST.insert(root, 11)
    GenBST.insert(root, 6)
    GenBST.insert(root, 6)
    GenBST.print_tree(root)
    GenBST.delete(root, 12)
    GenBST.delete(root, 13)
    GenBST.print_tree(root)
    GenBST.inorder_traversal(root)


if __name__ == '__main__':
    main()