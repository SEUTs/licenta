champions = []
with open("C:\\Users\\teata\\OneDrive\\Desktop\\toplaners.txt", 'r') as f:
    lines = f.readlines()
    for line in lines:
        champions.append(line[:-1])
print(champions)