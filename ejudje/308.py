def WithDraw(Acc, Bank):
    if Acc < Bank:
        return "Insufficient Funds"
    else:
        return Acc - Bank
    
Acc , Bank = map(int, input().split())
print(WithDraw(Acc, Bank))