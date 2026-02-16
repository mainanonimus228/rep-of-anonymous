n = int(input())

arr = []

for i in range (n):
    name = input()
    arr.append(name)


seen = set()
for x in arr:
    if x in seen:
        n -= 1
    else:
        seen.add(x)

print(n)