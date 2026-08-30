class Node:
    def __init__(self, left=None, right=None, maxinsubtree=-1):
        self.left = left
        self.right = right
        self. maxinsubtree = maxinsubtree
    
class PersistentArray:
    def __init__(self, root=None, height=0):
        self.root = root
        self.height = height

# tar in nodens riktiga nivå (inte nivå - 1 som i labb instruktionen utan det görs i funktionen)
def bit(index: int, level: int) -> int: 
    mask = 1 << (level - 1)
    bit = (index & mask) >> (level - 1)
    return bit
        
def newarray() -> PersistentArray:
    return PersistentArray(None, 0)

    
if __name__ == "__main__":
    i = bit(5, 1)
    print(i)