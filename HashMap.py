

from collections import MutableMapping
from random import randrange

class MapBase(MutableMapping):
    class _Item:
        __slots__ = '_key', '_value'
        
        def __init__(self, k, v):
            self._key = k
            self._value = v
        
        def __eq__(self, other):
            if other == None:
                return 0
            return self._key == other._key
        def __ne__(self, other):
            return not (self == other)
        def __lt__(self, other):
            return self._key < other._key

class HashMapBase(MapBase):
    def __init__(self, N=11, p=109345121):
        self._table = N * [None]
        self._n = 0
        self._p = p
        self._a = 1 + randrange(p-1)
        self._b = randrange(p)
        self._N = N

    def _hash_function(self, k):
        i = hash(k) # hash code
        # MAD : ((ai + b) % p ) % N
        return ( (self._a * i + self._b) % self._p ) % self._N
        
    def __len__(self):
        return self._n

    def __getitem__(self, k):
        # find the hash value
        hash_value = self._hash_function(k)
        # return self._table[hash_value]
        return self._getbucket_item(hash_value, k)
    
    def __setitem__(self, k, v):
        # find the hash value
        hash_value = self._hash_function(k)
        #self._table[hash_value] = Item(k,v)        
        self._setbucket_item(hash_value, k, v)
        
    def __delitem__(self, k):
        # find the hash value
        hash_value = self._hash_function(k)
        #self._table[hash_value] = None        
        self._delbucket_item(hash_value, k)
        

class ChainHashMap(HashMapBase):
    def _getbucket_item(self, hash_value, k):
        #bucket is a list
        bucket = self._table[hash_value]
        if bucket:
            # search for k
            for item in bucket:
                if item._key == k:
                    return item._value
            raise KeyError('Key not found')
        else:
            raise KeyError('Key not found')
        
    def _setbucket_item(self, hash_value, k, v):
        if self._table[hash_value] == None:
            self.table[hash_value] = []
        
        # search for the key k
        bucket = self._table[hash_value]
        index = -1
        for index in range(len(bucket)):
            if bucket[index]._key == k:
                bucket[index]._value = v
        
        if index < 0:
            # insert new item
            new_item = ChainHashMap._Item(k, v)
            bucket.append(new_item)
            self._n += 1
            
    def _delbucket_item(self, hash_value, k):
        # search for the key k
        bucket = self._table[hash_value]
        if bucket == None:
            raise KeyError('Key not found')
        index = -1
        for index in range(len(bucket)):
            if bucket[index]._key == k:
                break
        
        if index < 0:
            raise KeyError('Key not found')
        else:
            item = bucket[index]
            bucket.remove(item)
            self._n -= 1
        
    def __iter__(self):
        for bucket in self._table:
            if bucket != None:
                for item in bucket:
                    yield item._key


class LinearProbeHashMap(HashMapBase):
    def _getbucket_item(self, hash_value, k):
        item = self._table[hash_value]

        if item == None:
            raise KeyError('Key not found')
        if item._key == k:
            return item._value

        index = (hash_value + 1) % self._N
        item = self._table[index]

        for i in range(self._n):
            index = (index + 1) % self._N
            item = self._table[index]
            if item == None and item._key == k:
                break


        if item == None:
            raise KeyError('Key not found')
        else:
            return item._value
    
    def _setbucket_item(self, hash_value, k, v):
        item = self._table[hash_value]
        if item == None:
            # new element, correct slot
            self._table[hash_value] = LinearProbeHashMap._Item(k,v)
            self._n += 1
        else:
            index = (hash_value + 1) % self._N
            item = self._table[index]
            while item != None and item._key != k:
                index = (index + 1) % self._N
                item = self._table[index]
            if item == None:
                # new element
                self._table[index] = LinearProbeHashMap._Item(k, v)
                self._n += 1
            else:
                # update value
                self._table[index]._value = v
    
    # buggy version!!!
    def _delbucket_item(self, hash_value, k):
        item = self._table[hash_value]
        if item == None:
            raise KeyError('Key not found')
        else:
            if item._key == k:
                # delete
                self._table[hash_value] = None
                # shift elements

                # index = (hash_value + 1) % self._N
                # item = self._table[index]
                # while item != None and self._hash_function(k) != index:
                #     self._table[index-1] = self._table[index]
                #     index = (index + 1) % self._N
                #     item = self._table[index]

                i = 1
                index = hash_value % self._N
                # item = self._table[(index + i ** 2) % self._N]

                while item is not None and self._hash_function(k) == self._hash_function(self._table[(index + i ** 2) % self._N].key) :
                    print(self._table[(index + i ** 2) % self._N])
                    print('aaaaaaaaaaaa')
                    self._table[(index + i ** 2) % self._N], self._table[(index + (i-1) ** 2) % self._N] = self._table[(index + (i-1) ** 2) % self._N], self._table[(index + i ** 2) % self._N]
                    item = self._table[(index + i ** 2) % self._N]

                    i += 1

                    # if item[index + i ** 2]

                self._n -= 1
            else:
                # search
                # index = (hash_value + 1) % self._N
                # item = self._table[index]
                i = 1
                while item != None and item._key != k:
                    index = (index + i**2) % self._N
                    item = self._table[index]
                    i += 1
                if item == None:
                    raise KeyError('Key not found')
                else:
                    # delete
                    self._table[index] = None
                    # shift elements

                    # index = (index + 1) % self._N
                    # item = self._table[index]
                    # while item != None and self._hash_function(k) != index:
                    #     self._table[index-1] = self._table[index]
                    #     index = (index + 1) % self._N
                    #     item = self._table[index]

                    index = hash_value % self._N
                    while item is not None and self._hash_function(k) == self._hash_function(self._table[index].key):
                        self._table[(index + i ** 2) % self._N], self._table[(index + (i - 1) ** 2) % self._N] = self._table[(index + (i - 1) ** 2) % self._N], self._table[(index + i ** 2) % self._N]
                        item = self._table[(index + i ** 2) % self._N]
                        i += 1
                    self._n -= 1

                
    def __iter__(self):
        for item in self._table:
            if item != None:
                yield item._key



class QuadraticProbeHashMap(HashMapBase):
    def _getbucket_item(self, hash_value, k):
        item = self._table[hash_value]

        if item == None:
            raise KeyError('Key not found')
        if item._key == k:
            return item._value

        index = (hash_value ) % self._N
        # item = self._table[index]

        for i in range(1,self._n):
            index = (index + i**2) % self._N
            item = self._table[index]
            if item == None or item._key == k:
                break


        if item == None:
            raise KeyError('Key not found')
        else:
            return item._value

    def _setbucket_item(self, hash_value, k, v):
        item = self._table[hash_value]
            
        if item == None:
            # new element, correct slot
            self._table[hash_value] = QuadraticProbeHashMap._Item(k,v)
            self._n += 1
        else:

            index = (hash_value) % self._N
            # item = self._table[index]
            i = 1
            while item != None and item._key != k:
                index = (index + i**2) % self._N
                item = self._table[index]
                i += 1

            if item == None:
                # new element
                self._table[index] = QuadraticProbeHashMap._Item(k, v)
                self._n += 1
            else:
                # update value
                self._table[index]._value = v

        if self._n * 2 > self._N:
            self._resize(self._N * 2 + 1)

    def _resize(self, size):        
        new = []
        temp = self._n
        for i in self.items():
            new.append(i)
            
            
        self._table = [None] * size
        self._N = size
        for i in new:
            self[i._key] = i._value
        self._n = temp
        


    def get_table(self):
        return self._table


    def keys(self):
        for i in self._table:
            if i is None:
                continue
            yield i._key

    def items(self):
        for i in self._table:
            if not i:
                continue
            yield i

    def __eq__(self,M2):
        if len(self) != len(M2):
            return 0
        
        for i in self:
            if i not in M2:
                return False
            if self[i] != M2[i]:
                return False

        return True

    def __ne__(self,M2):
        return not self == M2
    
                
        

    # buggy version!!!
    def _delbucket_item(self, hash_value, k):
        item = self._table[hash_value]
        if item == None:
            raise KeyError('Key not found')
        else:
            if item._key == k:
                # delete
                self._table[hash_value] = None
                # shift elements

                # index = (hash_value + 1) % self._N
                # item = self._table[index]
                # while item != None and self._hash_function(k) != index:
                #     self._table[index-1] = self._table[index]
                #     index = (index + 1) % self._N
                #     item = self._table[index]

                i = 1
                index = hash_value % self._N
                # item = self._table[(index + i ** 2) % self._N]

                while self._table[(index + i ** 2) % self._N] is not None and self._hash_function(k) == self._hash_function(self._table[(index + i ** 2) % self._N]._key) :

                    self._table[(index + i ** 2) % self._N], self._table[(index + (i-1) ** 2) % self._N] = self._table[(index + (i-1) ** 2) % self._N], self._table[(index + i ** 2) % self._N]
                    # item = self._table[(index + i ** 2) % self._N]

                    i += 1

                    # if item[index + i ** 2]

                self._n -= 1
            else:
                # search
                # index = (hash_value + 1) % self._N
                # item = self._table[index]
                i = 1
                while item != None and item._key != k:
                    index = (index + i**2) % self._N
                    item = self._table[index]
                    i += 1
                if item == None:
                    raise KeyError('Key not found')
                else:
                    # delete
                    self._table[index] = None
                    # shift elements

                    # index = (index + 1) % self._N
                    # item = self._table[index]
                    # while item != None and self._hash_function(k) != index:
                    #     self._table[index-1] = self._table[index]
                    #     index = (index + 1) % self._N
                    #     item = self._table[index]

                    index = hash_value % self._N
                    while self._table[(index + i ** 2) % self._N] is not None and self._hash_function(k) == self._hash_function(self._table[(index + i ** 2) % self._N]._key):
                        self._table[(index + i ** 2) % self._N], self._table[(index + (i - 1) ** 2) % self._N] = self._table[(index + (i - 1) ** 2) % self._N], self._table[(index + i ** 2) % self._N]
                        item = self._table[(index + i ** 2) % self._N]
                        i += 1
                    self._n -= 1
        if self._n * 3 < self._N:
            self._resize(self._N//2 - (not self._N % 2) )
            #(not self._N % 2 ) to keep self._N an odd number



    def __iter__(self):
        for item in self._table:
            if item != None:
                yield item._key

        


# M = QuadraticProbeHashMap()
# M["a"] = 5
# M[1] = 3
#
# print(M[1])

# h = QuadraticProbeHashMap()
# h["a"] = 5
# h[1] = 2
# print(h["a"])



if  __name__ == '__main__':
    m = QuadraticProbeHashMap()
    m[0] = 1
    m['a'] = 'b'
    m[2] = 3
    for k in m:
        print(k, m[k])

    del m[0]

    print()
    for k in m:
        print(k, m[k])

    m2 = QuadraticProbeHashMap()
    m2[2] = 3
    m2['a'] = 'b'
        
