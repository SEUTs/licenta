

newFoods = sorted(teaDict["foods"], key=lambda d: len(d['description'].split(', ')))
print(newFoods)
print(newFoods[0])