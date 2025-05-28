from os import listdir
files = listdir("E:\\licenta\\games")
with open("C:\\Users\\SasEUnTicnit\\Desktop\\text.txt", 'x') as f:
    for file in files:
        f.write(file + '\n')
    f.close()