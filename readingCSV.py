import csv

def sort_matrix_by_winrate(matrix):
    # sort champions based on winrate (name, wins, games)
    return sorted(matrix, key=lambda row: row[1] / row[2])

def sort_matrix_by_games(matrix):
    # sort champions based on games (name, wins, games)
    return sorted(matrix, key=lambda row: row[2])

with open("output/test.csv", 'r') as file:
    csvFile = csv.reader(file)
    champs = {} 
    for lines in csvFile:
        if len(lines) > 0:
            champs.update({lines[0]: lines[0]})
            if lines[1] == "True":
                champs.update({lines[0]+"W": champs.get(lines[0]+"W", 0) + 1})
            else:
                champs.update({lines[0]+"W": champs.get(lines[0]+"W", 0)})
            champs.update({lines[0]+"G": champs.get(lines[0]+"G", 0) + 1})
    counter = 0
    champions = []
    newEntry = []
    for element in champs:
        counter += 1
        newEntry.append(champs[element])
        if counter == 3:
            champions.append(newEntry)
            newEntry = []
            counter = 0
    print(sort_matrix_by_winrate(champions))
    print(sort_matrix_by_games(champions))
