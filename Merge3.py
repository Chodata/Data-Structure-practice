import math

def merge_sort3(S):
    n = len(S)

    logn = math.ceil(math.log(n,3))
    src, dest = S, [None] * n

    for i in (3**k for k in range(logn)):
        for j in range(0, n, 3*i):
            merge(src, dest, j, i)
        src, dest = dest, src
    if S is not src:
        S[0:n] = src[0:n]

def merge(src, result, start, inc):
    end1 = start+inc
    end2 = min(start+2*inc, len(src))
    end3 = min(start + 3 * inc, len(src))

    x, y, z = start, start+inc , start
    while x < end1 and y < end2:
        if src[x] < src[y]:
            result[z] = src[x]
            x += 1
        else:
            result[z] = src[y]
            y += 1
        z += 1
    if x < end1:
        result[z:end2] = src[x:end1]
    elif y < end2:
        result[z:end2] = src[y:end2]

    src[start:end2] = result[start:end2]

    x, y ,z = start, start + 2 * inc, start
    while x < end2 and y < end3:
        if src[x] < src[y]:
            result[z] = src[x]
            x += 1
        else:
            result[z] = src[y]
            y += 1
        z += 1
    if x < end2:
        result[z:end3] = src[x:end2]
    elif y < end3:
        result[z:end3] = src[y:end3]


data = [66,36,60,98,77,52,47,11,29,85]
merge_sort3(data)
print(data)
print()
data = [10,9,8,7,6,5,4,3,2,1,0]
merge_sort3(data)
print(data)