# Description of the Project 
This Python project provides a versatile and efficient implementation of a Binary Search Tree (BST) through a TreeNode class and associated functions. A Binary Search Tree is a hierarchical data structure that allows rapid search, insertion, and deletion of elements in a sorted manner. This package encapsulates key operations on a BST, allowing the students to learn BST through a vivid demonstration.

# Use the Package 
## Functions supported by the package 
### insert()
The insert function allows the addition of new elements while preserving the BST property, ensuring efficient insertion of values into the tree.
```\python
def insert(root, key):
    if root is None:
        return TreeNode(key)
    else:
        if root.val < key:
            root.right = insert(root.right, key)
        elif root.val > key:
            root.left = insert(root.left, key)
        else:
            print("Value already exists!")
            return root
    return root
```

### delete()
The delete function removes nodes based on specified keys, maintaining the BST structure by handling cases with one or two children elegantly.
```\python
def delete(root, key):
    if root is None:
        print("Value Not Found!")
        return root

    if key < root.val:
        root.left = delete(root.left, key)
    elif key > root.val:
        root.right = delete(root.right, key)
    else:
        # Node with only one child or no child
        if root.left is None:
            return root.right
        elif root.right is None:
            return root.left

        # Node with two children
        root.val = get_min_value(root.right)
        root.right = delete(root.right, root.val)
    return root
```

### inorder_traversal()
The inorder_traversal function performs an in-order traversal of the BST, generating a sorted sequence of elements, a fundamental operation in binary trees.
```\python
def inorder_traversal(root):
    seq = io_traverse(root)
    print(seq)

def io_traverse(root):
    if root is not None:
        result = []
        result += io_traverse(root.left)
        result.append(root.val)
        result += io_traverse(root.right)
        return result
    else:
        return []
```

### print_tree()
The print_tree function visualizes the BST's hierarchical structure, aiding developers in understanding and debugging their tree-based algorithms.
```\python
def print_tree(root, val="val", left="left", right="right"):
    def display(root, val=val, left=left, right=right):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if getattr(root, right) is None and getattr(root, left) is None:
            line = '%s' % getattr(root, val)
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if getattr(root, right) is None:
            lines, n, p, x = display(getattr(root, left))
            s = '%s' % getattr(root, val)
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if getattr(root, left) is None:
            lines, n, p, x = display(getattr(root, right))
            s = '%s' % getattr(root, val)
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = display(getattr(root, left))
        right, m, q, y = display(getattr(root, right))
        s = '%s' % getattr(root, val)
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2

    lines, _, _, _ = display(root, val, left, right)
    for line in lines:
        print(line)
```

## Sample Program to use the package 
```
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
```

Here is a sample outptut for running the program
![Sample Run](https://github.com/software-students-fall2023/3-python-package-exercise-ayr/blob/BST-Generation-and-Visualization/SampleRun.jpg)


# Future contribution to the project 
## Set up the virtual environment
Install pipenv, build, and twine if not already installed.
Create and activate up the `pipenv` virtual environment as before.
Run the package directly from the command line: `python3 -m bstpackage`. This should run the code in the `__main__.py` file.
Exit the virtual environment.
