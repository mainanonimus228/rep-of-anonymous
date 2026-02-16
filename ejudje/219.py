n = int(input())

dorama = {}

for i in range(n):
    name , value = input().split()
    value = int(value)

    if name in dorama:
        dorama[name] += value
    else:
        dorama[name] = value

for key in sorted(dorama):
    print(key, dorama[key])