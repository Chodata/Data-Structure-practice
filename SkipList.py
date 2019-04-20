from random import randint
from os import sys

class SkipList:
    class Node:
        __slots__ = 'key', 'value','up','down','left','right'
        def __init__(self, k, v):
            self.key = k
            self.value = v
            self.up = None
            self.down = None
            self.left = None
            self.right = None

    def __init__(self):
        self.height = 1
        self.length = 0
        self.first = self.Node(float("-inf"),None)
        self.last = self.Node(float("inf"),None)
        self.first.right = self.last    #top left , dummy
        self.last.left = self.first     #top right , dummy



    def add(self,k,v):
        cursor = self.find_Node(k)
        if cursor.key == k:
            return self.update_value(k,v)


        node_height = 1
        n = 2
        while( 1 == randint(1,n)):
            node_height += 1
            n *= 2



        if self.height < node_height:
            self.increase_dummy_height(node_height)


        lowest = self.Node(k,v)
        cursor = lowest

        for i in range(node_height - 1):
            cursor.up = self.Node(k,v)
            cursor.up.down = cursor

            cursor = cursor.up

        lower_bound = self.first
        diff = self.height - node_height
        for i in range(diff):
            lower_bound = lower_bound.down

        for i in range(node_height):
            while lower_bound.right.key < cursor.key:
                lower_bound = lower_bound.right

            temp = lower_bound.right
            lower_bound.right = cursor
            cursor.left = lower_bound

            temp.left = cursor
            cursor.right = temp

            cursor = cursor.down
            lower_bound = lower_bound.down

        self.length += 1




    def increase_dummy_height(self,h):
        diff = h - self.height
        for i in range(diff):
            self.first.up = self.Node(self.first.key,self.first.value)
            self.last.up = self.Node(self.last.key,self.last.value)
            self.first.up.down = self.first
            self.last.up.down = self.last
            self.first = self.first.up
            self.last = self.last.up
            self.first.right = self.last
            self.last.left = self.first
        self.height = h


    def update_value(self,k,v):
        pass

    def find(self,k): #find Node and return value

        cursor = self.find_Node(k)
        if cursor.key != k:
            raise KeyError("Key not found")
            return None
        else:
            return cursor.value

    def find_Node(self,k):  #return node that equal than or more than k
        # left_bound = self.first
        # right_bound = self.right
        cursor = self.first
        for i in range(self.height-1): #go down until last level
            while  cursor.right.key < k :
                cursor = cursor.right
            cursor = cursor.down

        while cursor.right.key <= k:
            cursor = cursor.right

        return cursor

    def find_min(self):
        cursor = self.first
        for i in range(self.height -1):
            cursor = cursor.down

        return cursor.right.key,cursor.right.value

    def find_max(self):
        cursor = self.last
        for i in range(self.height -1):
            cursor = cursor.down

        return cursor.left.key,cursor.left.value


    def delete_key(self,k):
        cursor = self.find_Node(k)
        if cursor.key != k:
            raise KeyError("Key not found")
        while(cursor != None):
            cursor.right.left = cursor.left
            cursor.left.right = cursor.right
            cursor = cursor.up

    def range(self,lowerbound,upperbound):
        lowerbound = self.find_Node(lowerbound)
        li = list()
        while(lowerbound.key <= upperbound):
            li.append(lowerbound.key)
            lowerbound = lowerbound.right

        return li

if __name__ == "__main__":  #example use
    skList = SkipList()
    skList.add(1,2)
    skList.add(2,3)
    skList.add(3,4)
    skList.add(4,'a')

    print(skList.find(1))
    print(skList.find(2))
    print(skList.find(3))
    print(skList.find(4))
    print('--')
    print(skList.find_max())
    print(skList.find_min())
    print('--')
    skList.delete_key(4)
    print(skList.find_max())
    print('--')
    print(skList.range(1,4))
    print(skList.range(1,2))
    print(skList.range(1,3))
