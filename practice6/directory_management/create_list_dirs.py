import os

# текущая папка
print("Current directory:", os.getcwd()) #gt currnt wrkng drctry

# создать папку
os.mkdir("test_folder") 

# список файлов
print("Files:", os.listdir())

# перейти в папку
os.chdir("test_folder") #chang drctry
print("Now in:", os.getcwd())

# вернуться назад
os.chdir("..")  #.. перейти на уровень выше

# удалить папку
os.rmdir("test_folder")