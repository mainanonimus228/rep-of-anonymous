n = int(input())
nums = list(map(int, input().split()))

freq = {}

# считаем частоты
for x in nums:
    if x in freq:
        freq[x] += 1
    else:
        freq[x] = 1

max_freq = 0
answer = nums[0]

# ищем элемент с максимальной частотой
for x in freq:
    if freq[x] > max_freq or (freq[x] == max_freq and x < answer):
        max_freq = freq[x]
        answer = x

print(answer)
