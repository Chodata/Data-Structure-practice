from Tree import BinaryTree


class ArrayBinaryTree(BinaryTree):
    DEFAULT_CAPACITY = 10

    def __init__(self):
        self._data = [None] * ArrayBinaryTree.DEFAULT_CAPACITY
        self._size = 0

    def _resize(self, new_size):
        old = self._data
        self._data = [None] * new_size
        for i in range(len(old)):
            self._data[i] = old[i]

    def __len__(self):
        return self._size
    def is_empty(self):
        return self._size == 0

    def root(self):
        if self._size == 0:
            return None
        else:
            return self._data[0]
    def add_root(self,e):
        self._data[0] = e
        self._size += 1
        return 0


    def left(self, p):
        if self.have_left(p):
            return self._data[2*p+1]

    def right(self, p):
        if self.have_right(p):
            return self._data[2*p+2]

    def parent(self, p):
        return self._data[(p-1) // 2]

    def have_left(self,p):
        if p != None and self._size >= 2*p+1 and self._data[2*p+1] != None:
            return 1
        return 0

    def have_right(self,p):
        if p != None and self._size >= 2*p+2 and self._data[2*p+2] != None:
            return 1
        return 0


    def num_children(self,p):
        n_child = 0
        if self.have_left(p):
            n_child += 1
        if self.have_right(p):
            n_child += 1
        return n_child

    def is_leaf(self,p):
        if p == None:
            return 0
        if self.have_left(p) or self.have_right(p):
            return 0
        return 1

    def is_root(self,p):
        return p == self.root()

    def __len__(self):
        return self._size

    def add_left(self,p,e):
        if p == None or self.left(p) != None:
            raise Exception("Invalid position")
        if p*2 + 1 >= len(self._data):
            self._resize(len(self._data) * 2 + 1)
        self._data[2*p+1] = e
        self._size += 1
        return 2 * p + 1

    def add_right(self,p,e):
        if p == None or self.right(p) != None:
            raise Exception("Invalid position")

        if p*2 + 2 >= len(self._data):
            self._resize(len(self._data) * 2 + 2)
        self._data[2*p+2] = e
        self._size += 1
        return 2 * p + 2

    def set(self,p,e):
        if p == None:
            raise Exception("invalid position")
        if p >= len(self._data):
            self._resize(p+1)
        if self._data[p] == None:
            self._size += 1
        self._data[p] = e
        return e


    def attach_one(self,p,pos,T):
        if T.left(pos) != None:
            self.add_left(p, T.left(pos))
            self.attach_one(p*2+1, pos * 2 + 1, T)
        if T.right(pos) != None:
            self.add_right(p,T.right(pos))
            self.attach_one(p*2 + 2, pos * 2 + 2, T)

    def attach(self,p,T1,T2):
        if p < 0 or not self.is_leaf(p):
            print('o',p)
            raise Exception("Invalid position")
        if T1 != None and T1.root() != None:
            self.add_left(p,T1.root())
            self.attach_one(self.left(p), 0 , T1)

        if T2 != None and T2.root() != None:
            self.add_right(p,T2.root())
            self.attach_one(self.right(p),0, T2)


    def __iter__(self):
        for i in self._data:
            if(i != None):
                yield i


    def remove(self,p):
        if not self.is_leaf(p):
            return
        self._size -=1
        return self.set(p,None)



# if __name__ == '__main__':
#     abt = ArrayBinaryTree()
#     for i in range(10):
#         abt.set(i,i)
#
#     for i in abt:
#         print(i)
#     print('--')
#     abt.remove(4)
#     for i in abt:
#         print(i)
#

if __name__ == '__main__':
    t1 = ArrayBinaryTree()

    p = t1.add_root(10)
    p1 = t1.add_left(p, 1)
    p2 = t1.add_right(p, 20)
    print(len(t1))
    print('--')
    for e in t1:
        print(e)
    print('--')
    try:
        t1.add_left(p, 10)
        t1.add_right(p, 20)
    except Exception:
        pass
    t1.set(p, 2)
    # for pos in t1.inorder(p):
    #     print(pos.element())
    for i in t1:
        print(i)

    print("--")
    t1.remove(p2)
    print(len(t1))
    print('--')
    t2 = ArrayBinaryTree()
    t2.add_root(100)
    t1.attach(p1, None, t2)
    for e in t1:
        print(e)
