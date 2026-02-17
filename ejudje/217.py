n = int(input())

array = []
for _ in range(n):
    array.append(input())

freq = {}

# считаем, сколько раз встречается каждый номер
for x in array:
    if x in freq:
        freq[x] += 1
    else:
        freq[x] = 1

count = 0
for x in freq:
    if freq[x] == 3:
        count += 1

print(count)
