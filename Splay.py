class BinaryTree:
    class Node:
        def __init__(self,k):
            self.key = k
            self.left = None
            self.right = None
            self.parent = None

        def __iter__(self):
            yield self

        def __lt__(self,other):
            return self.key < other.key
        def __le__(self, other):
            return self.key <= other.key
        def __gt__(self, other):
            return self.key > other.key
        def __ge__(self, other):
            return self.key >= other.key

    def __init__(self):
        self.root = None

class SplayBinary(BinaryTree):
    def __init__(self):
        self.root = None
        self.size = 0

    def add(self,k):
        node = self.Node(k)

        if self.size == 0:
            self.root = node
            self.size += 1
            return

        cursor = self.root
        while(1):

            if k > cursor.key:
                if cursor.right is None:
                    cursor.right = node
                    node.parent = cursor
                    break
                cursor = cursor.right
                # print(333)
            else:
                # print(cursor.left.key)
                # print(cursor.key)
                if cursor.left is None:
                    cursor.left = node
                    node.parent = cursor
                    break
                # print(222)
                cursor = cursor.left

        self.size += 1
        self.update(node)

    def update(self,node):
        while(node.parent is not None):
            if node == node.parent.left:
                self.left(node)
            else:
                self.right(node)

        self.root = node



    def right(self,node):

        node_left = node.left

        parent = node.parent

        parent.right = node_left
        if node_left is not None:
            node_left.parent = parent

        node.parent = parent.parent
        if node.parent is None:
            pass
        elif node.parent.left == parent:
            node.parent.left = node
        else:
            node.parent.right = node

        node.left = parent
        parent.parent = node

    def left(self,node):
        node_right = node.right

        parent = node.parent

        parent.left = node_right
        if node_right is not None:
            node_right.parent = parent

        node.parent = parent.parent
        if node.parent is None:
            pass
        elif node.parent.left == parent:
            node.parent.left = node
        else:
            node.parent.right = node

        node.right = parent
        parent.parent = node

    def search(self,key):
        cursor = self.root
        while cursor is not None:
            if key == cursor.key:
                self.update(cursor)
                return cursor

            if key < cursor.key:
                if cursor.left is None:
                    return cursor
                cursor = cursor.left

            elif key > cursor.key:
                if cursor.right is None:
                    return cursor
                cursor = cursor.right


        return None

    def delete(self,key):
        node = self.search(key)
        if node is None or self.size == 0:
            return
        self.update(node)

        left = node.left
        right = node.right
        if left is not None and right is None:
            self.root = left
            left.parent = None
            del node
            self.size -= 1
            return

        if right is not None and left is None:
            self.root = right
            right.parent = None
            del node
            self.size -= 1
            return

        if right is None and left is None:
            self.root = None
            del node
            self.size -= 1


        self.root = left
        left.parent = None

        node.left = None
        node.right = None
        del node

        if left.right is not None:
            cursor = right

            while cursor.left is not None:
                cursor = cursor.left
            left.right.parent = cursor
            cursor.left = left.right

        left.right = right
        right.parent = left

        self.size -= 1




    def printall(self):
        self.print(self.root)

    def print(self,node):
        if node == None:
            return
        print(node.key)

        self.print(node.left)
        self.print(node.right)

    def __len__(self):
        return self.size





if __name__ == '__main__':
    p = SplayBinary()

    p.add(3)
    print(p.root.key)

    p.add(10)
    print(p.root.key)

    p.add(4)
    print(p.root.key)

    p.add(11)
    print(p.root.key)

    p.search(3)
    print(p.root.key)

    p.add(8)
    print(p.root.key)

    p.add(5)
    print(p.root.key)

    p.add(6)
    print(p.root.key)

    p.search(7)
    print("search 7:",p.root.key) #nearby value

    p.delete(10)
    print(p.root.key) #after delete check root after delete 10

    p.search(5)
    print(p.root.key)

    p.delete(5)
    print(p.root.key)

    print('----------')
    p.printall()

