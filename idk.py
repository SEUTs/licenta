import json

pairs = []
total = 0

with open("samples\\sampleTeammatesReduced.json", 'r') as f:
    data = json.load(f)
    f.close()
    for champion in data:
        for teammate in data[champion]:
            if data[champion][teammate]["met"] > 2000:
                print(teammate, champion, str(data[champion][teammate]["met"]))
            pairs.append([champion, teammate])
            total += data[champion][teammate]["met"]

print(f"Pairs: {len(pairs)}")
print(f"Total: {total}")
print(f"Average: {round(total / len(pairs), 2)}")