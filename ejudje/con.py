n = int(input())

nums = list(map(int, input().split()))

freq = {}

for x in nums:
    if x in freq:
        freq[x] += 1
    else:
        freq[x] = 1

max_freq = 0

for x in freq:
    if freq[x] > max_freq:
        max_freq = freq[x]
        answer = x

print(answer)