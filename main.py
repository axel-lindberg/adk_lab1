import math

class Node:
    def __init__(self, left=None, right=None, maxinsubtree=-1):
        self.left = left
        self.right = right
        self.maxinsubtree = maxinsubtree
    
class PersistentArray:
    def __init__(self, root=None, height=0):
        self.root = root
        self.height = height
        

def bit(index: int, level: int) -> int: 
    mask = 1 << level
    bit = (index & mask) >> level
    return bit

def requiredheight(index: int) -> int:
    return math.ceil(math.log2(index + 1))

def _maxinsubtree(node: Node | None) -> int:
    return node.maxinsubtree if node is not None else -1

        
def newarray() -> PersistentArray:
    return PersistentArray(None, 0)


def set(a: PersistentArray, i: int, value: int) -> PersistentArray:
    new_height = max(a.height, requiredheight(i))
    
    if new_height > a.height:
        left_side = fill_left_tree(a.root, a.height, new_height - 1)
        right_side = _set(None, new_height - 1, i , value)
        new_root = Node(left_side, right_side, maxinsubtree=max(_maxinsubtree(a.root), _maxinsubtree(right_side)))
        return PersistentArray(new_root, new_height)
    
    new_root = _set(a.root, a.height, i, value)
    return PersistentArray(new_root, a.height)
    
         
def _set(node: Node | None, level: int, i: int, value: int):
    if level == 0:
        return Node(None, None, maxinsubtree = value)
     
    direction = bit(i, level - 1)
     
    if direction == 0:
        new_child = _set(node.left if node is not None else None, level - 1, i, value)
        other_child = node.right if node is not None else None
        return Node(new_child, other_child, maxinsubtree=max(_maxinsubtree(new_child), _maxinsubtree(other_child)))
    
    else:
        new_child = _set(node.right if node is not None else None, level - 1, i, value)
        other_child = node.left if node is not None else None
        return Node(other_child, new_child, maxinsubtree=max(_maxinsubtree(new_child), _maxinsubtree(other_child)))
    
def fill_left_tree (node: Node | None, current_height: int, target_height: int) -> Node | None:
    while current_height < target_height:
        node = Node(left = node, right = None, maxinsubtree=_maxinsubtree(node))
        current_height += 1
    return node

# def get()

# def maxininterval

# def maxsegment

# def maxrightsegment

# def maxleftsegment

    
if __name__ == "__main__":
    a = newarray()
    print(f"Start: height={a.height}, root={a.root}")

    a = set(a, 3, 17)
    print(f"Efter set(3, 17): height={a.height}")
    print(f"  root.maxinsubtree = {a.root.maxinsubtree}")
    
    a = set(a, 3, 4177)
    print(f"Efter set(3, 4177): height={a.height}")
    print(f"  root.maxinsubtree = {a.root.maxinsubtree}")
    
    a = set(a, 5, 8)
    print(f"Efter set(5, 8): height={a.height}")
    print(f"  root.maxinsubtree = {a.root.maxinsubtree}")
    
    a = set(a, 16, 20)
    print(f"Efter set(16, 20): height={a.height}")
    print(f"  root.maxinsubtree = {a.root.maxinsubtree}")