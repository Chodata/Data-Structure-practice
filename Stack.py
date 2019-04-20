class Stack:
    def __init__(self,a = []):
        self.items = a
        self.size = len(a)

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)
        self.size += 1

    def pop(self):
        self.size -= 1
        return self.items.pop()

    def peek(self):
        return self.items[self.size - 1]
    def printself(self):
        print(self.items)
    

n = "5 2 + 8 3 - * 4 /".split()
s = Stack()
result = 0
for i in n:
    if i == "+" or i == "-" or i == "*" or i == "/":
        temp1 = s.pop()
        temp2 = s.pop()

        s.push(str(eval(temp2 + i + temp1)))
    else:
        s.push(i)

print(s.pop())
