n = int(input())

array = []

seen = set()

for i in range(n):
    array.append(input())

for i in range (n):
    if not(array[i] in seen):
        print(array[i], end = " ")
        print(i+1)
        seen.add(array[i])
    else:
        continue


