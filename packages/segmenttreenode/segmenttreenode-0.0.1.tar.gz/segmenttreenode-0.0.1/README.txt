segmenttreenode
-------------------------------------------------------------------
link: https://pypi.python.org/pypi/segmenttreenode
Data structure for Segment Tree.

-------------------------------------------------------------------
Install:
Use 'pip' or 'easy_install' to install the package.

sudo pip install segmenttreenode
sudo easy_install segmenttreenode

-------------------------------------------------------------------
Usage:
In Python File:
from segmenttreenode import SegmentTreeNode
arr = [1, 3, 5, 7, 9, 11]
root = SegmentTreeNode.SegmentTreeNode(arr, 0, len(arr) - 1)
# Use this segment tree through the root.
# ... ...

-------------------------------------------------------------------
Explanation:
There are three necessary arguments to 
initialize a segment tree node instance from SegmetTreeNode class.

[1] one dimensional list
[2] start index
[3] end index
