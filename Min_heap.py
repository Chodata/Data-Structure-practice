class LinkedBase:
    class Node:
        def __init__(self,k,v,p = None,l = None,r = None):
            self.key = k
            self.value = v
            self.parent = p
            self.left = l
            self.right = r

        def __str__(self):
            return str('Key: ' + str(self.key) + " Value: " + str(self.value))


    def __init__(self):
        self.root = None
        self.last = None
        self.next_empty_node = None
        self.current_level_size = 0
        self.dept = 0
        self.size = 0

    def printall(self):
        self.print(self.root)
        print()

    def print(self,n):
        if n == None:
            return
        print(n)
        self.print(n.left)
        self.print(n.right)

    def min(self):
        return self.root


    def add(self, k,v):
        newNode = self.Node(k,v)
        if self.size == 0:
            self.root = newNode
            self.last = newNode
        else:
            pos = bin(self.size+1)[3::]
            cursor = self.root
            for i in pos:
                newNode.parent = cursor
                if i == '0':
                    cursor = cursor.left
                else:
                    cursor = cursor.right
            if i == '0':
                newNode.parent.left = newNode
            else:
                newNode.parent.right = newNode
        self.size += 1
        self.last = newNode
        self.moveup(newNode)
        # self.printall()
        # print()
        # print()
        return newNode


    def moveup(self,e):
        if e == self.root:
            return
        cursor = e

        while cursor.parent != None and cursor.key < cursor.parent.key:
            self.swap(cursor.parent,cursor)

            cursor = cursor.parent


    def movedown(self,e):
        cursor = e
        while cursor.left != None and (cursor.key > cursor.left.key or cursor.right != None and cursor.key > cursor.right.key) :
            if cursor.key > cursor.left.key:
                self.swap(cursor,cursor.left)
                cursor = cursor.left
            else:
                self.swap(cursor,cursor.right)
                cursor = cursor.right


    def remove(self,Node_to_remove):
        temp = self.Node(Node_to_remove.key,Node_to_remove.value)
        self.swap(Node_to_remove, self.last)

        if(self.last.parent.left == self.last):
            self.last.parent.left = None
        else:
            self.last.parent.right = None
        self.last.parent = None
        del self.last
        self.bubble(Node_to_remove)
        self.size -= 1
        self.last = self.find_last()
        return temp


    def bubble(self,Node):
        if Node.parent != None and Node.parent > Node.key:
            self.moveup(Node)
        else:
            self.movedown(Node)
        return Node

    def remove_min(self):
        return self.remove(self.root)

    def update(self,loc,k,v):
        loc.key = k
        loc.value = v


    def find_last(self):
        if self.size == 0:
            return
        cursor = self.root
        pos = bin(self.size)[3::]
        for i in pos:
            if i == '0':
                cursor = cursor.left
            else:
                cursor = cursor.right
        return cursor


    def is_empty(self):
        return self.size == 0

    def __len__(self):
        return self.size

    def swap(self,a,b):
        a.key, b.key = b.key,a.key
        a.value, b.value = b.value, a.value






lb = LinkedBase()
for i in range(5,0,-1):
    lb.add(i,i)
print("All node")
lb.printall()
print()

print("Remove min")
print(lb.remove_min())
print()

print("Add key:4, value: 3")
loc = lb.add(4,3)

lb.printall()
print()
print("Delete the previously added Node")
print(lb.remove(loc))
print()

print("All node")
lb.printall()


print()


