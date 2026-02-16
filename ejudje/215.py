n = int(input())
numbers = n

seen = set()
array = []

for i in range(n):
    name = input()
    array.append(name)

for x in array:
    if x in seen:
        numbers -=1
    else:
        seen.add(x)

print(numbers)
    