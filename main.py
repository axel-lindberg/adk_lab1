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
        
stack = []
        
def bit(index: int, level: int) -> int: 
    mask = 1 << level
    bit = (index & mask) >> level
    return bit

def requiredheight(index: int) -> int:
    return math.ceil(math.log2(index + 1))

def _maxinsubtree(node: Node | None) -> int:
    return node.maxinsubtree if node is not None else -1

#Skapa ny PersistentArray
def newarray() -> PersistentArray:
    return PersistentArray(None, 0)


#Sätt värdet på index i till value. Det ska vara ett mellanslag mellan set och i samt mellan i och value.
def set(a: PersistentArray, i: int, value: int) -> PersistentArray:
    stack.append(a)
    new_height = max(a.height, requiredheight(i))
    
    if new_height > a.height:
        left_side = fill_left_tree(a.root, a.height, new_height - 1)
        right_side = _set(None, new_height - 1, i , value)
        new_root = Node(left_side, right_side, maxinsubtree=max(_maxinsubtree(a.root), _maxinsubtree(right_side)))
        return PersistentArray(new_root, new_height)
    
    new_root = _set(a.root, a.height, i, value)
    return PersistentArray(new_root, a.height)

#rekursiv hjälpfunktion till set
def _set(node: Node | None, level: int, i: int, value: int):
    #Om det är ett löv retuneras value
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

#Backa tillbaka till läget en set-operation tidigare. Om ingen set-operation gjorts händer inget.
def unset():
    stack.pop()

#	Skriv ut värdet på index i på standard output på en egen rad
def get(a: PersistentArray, i: int):
    #Om a[i] inte har tilldelats ett värde tidigare skrivs 0
    if a.root is None: print(0)
    
    required_height = requiredheight(i)
    
    #Om index ligger utanför trädet retuneras 0
    if required_height > a.height: print(0)
    
    node = _get(a.root, a.height, i)
    
    if node is not None:
        print(node.maxinsubtree)
    
    else:
        print(0)

#rekursiv hjälpfunktion till get 
def _get(node: Node | None, level: int, i: int) -> Node:
    if level == 0:
        return node
    
    direction = bit(i, level - 1)
    
    if direction == 0:
        next_node = _get(node.left if node is not None else None, level - 1, i)
        return next_node
        
    else:
        next_node = _get(node.right if node is not None else None, level - 1, i)
        return next_node


# def maxininterval(a: PersistentArray: left: int, right: int) -> int:

# def maxsegment

# def maxrightsegment

# def maxleftsegment

    
if __name__ == "__main__":
    a = newarray()
    print(f"Start: height={a.height}, root={a.root}")
    
    a = set(a, 5, 12)
    get(a, 5)
    
    a = set(a, 5, 15)
    get(a, 5)
    
    a = unset()
    get(a, 5)
