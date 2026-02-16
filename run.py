class myclass():
  def __len__(self):
    return 0 # always false

myobj = myclass()
print(bool(myobj))