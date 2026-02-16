n = int(input())

first_occur = {}

for i in range(1, n + 1):
    item = input()
    if item not in first_occur:
        first_occur[item] = i

# Сортируем ключи и создаем список
sorted_keys = sorted(first_occur.keys())

# Проходим именно по отсортированному списку ключей
for key in sorted_keys:
    print(key, first_occur[key])