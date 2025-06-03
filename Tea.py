animals = [
    "chicken", "cow", "pig", "sheep", "rabbit"
]
meatTypes = [
    "breast", "leg", "wing"
]

def getCategory(userInput):
    firstKeyWord = ""
    secondKeyWord = ""
    for word in userInput.split(' '):
        for i in range(len(animals)):
            if word.lower() == animals[i]:
                firstKeyWord = animals[i]
        for i in range(len(meatTypes)):
            if word.lower() == meatTypes[i]:
                secondKeyWord = meatTypes[i]

    if firstKeyWord == "" or secondKeyWord == "":
        return "Not found"
    else:
        return firstKeyWord + " " + secondKeyWord
    

print(getCategory("Agricola Chicken Breast"))