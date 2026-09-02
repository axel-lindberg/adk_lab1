import math
import sys

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

#Minsta höjden som krävs för ett index ska få plats i trädet
def requiredheight(index: int) -> int:
    return math.ceil(math.log2(index + 1))

#Hämta maxinsubtree
def _maxinsubtree(node: Node | None) -> int:
    return node.maxinsubtree if node is not None else -1

#Skapa ny PersistentArray
def newarray() -> PersistentArray:
    return PersistentArray(None, 0)


#Sätt värdet på index i till value
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

#Rekursiv hjälpfunktion till set
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
def unset() -> PersistentArray:
    return stack.pop()


#Skriv ut värdet på index i på standard output på en egen rad
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

#Rekursiv hjälpfunktion till get 
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


def maxininterval(a: PersistentArray, left: int, right: int) -> int:
    #Om right ligger utanför trädets bredd -> trädets bredd blir högra gränsen
    return maxsegment(a.root, a.height, left, min(right, 2**(a.height) - 1))

def maxsegment(node: Node | None, level: int, left: int, right: int) -> int:
    if node is None:
        return -1
    
    if level == 0:
        return node.maxinsubtree
    
    dir_left = bit(left, level - 1)
    dir_right = bit(right, level - 1)

    #Fall C: Om left och right båda ligger i vänster delträd
    if dir_left == 0 and dir_right == 0:
        
        return maxsegment(node.left, level - 1, left, right)
    
    #Fall D: Om left och right båda ligger i höger delträd
    elif dir_left == 1 and dir_right == 1:
        return maxsegment(node.right, level - 1, left, right)
    
    #Fall E: Om left ligger i vänster delträd och right ligger i höger delträd
    elif dir_left == 0 and dir_right == 1:
        return max(maxleftsegment(node.right, level - 1, right), maxrightsegment(node.left, level - 1, left))    

def maxrightsegment(node: Node | None, level: int, i: int) -> int:
    if node is None:
        return -1
    
    if level == 0:
        return node.maxinsubtree

    direction = bit(i, level - 1)

    #Jämför med det största värdet åt höger och forstätt åt vänster
    if direction == 0:
        return max(maxrightsegment(node.left, level - 1, i), _maxinsubtree(node.right))

    #Strunta i värdet åt vänster och forsätt åt höger
    else:
        return maxrightsegment(node.right, level - 1, i)

def maxleftsegment(node: Node | None, level: int, i: int) -> int:
    if node is None:
        return -1
    if level == 0:
        return node.maxinsubtree

    direction = bit(i, level - 1)

    #Strunta i värdet åt höger och forsätt åt vänster
    if direction == 0:
        return maxleftsegment(node.left, level - 1, i)
    
    #Jämför med det största värdet åt vänster och forstätt åt höger
    else:
        return max(maxleftsegment(node.right, level - 1, i), _maxinsubtree(node.left))

    
if __name__ == "__main__":
    a = newarray()
    print(f"Start: height={a.height}, root={a.root}")
    
    a = set(a, 6, 5)
    a = set(a, 10, 20)
    print(maxininterval(a, 6, 10000))