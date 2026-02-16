n = int(input())

array = list(map(int , input().split()))

array.sort()
array.reverse()

for i  in range (n):
    print(array[i], end = " ")

