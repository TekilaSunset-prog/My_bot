distance_matrix = {
    "Depot": {'A': 10, 'B': 15, 'C': 20},
    "A": {'Depot': 10, 'B': 5, 'C': 10},
    "B": {'Depot': 15, 'A': 5, 'C': 5},
    "C": {'Depot': 20, 'A': 10, 'B': 5}
}

path = []
min_value = 1000000000000
appen = False
i = 0
q = 0
key = 'Depot'

for _ in distance_matrix:
    dict1 = distance_matrix[key]
    i += 1
    for key1, value in dict1.items():
        if value < min_value:
            if key1 not in path:
                if key1 == 'Depot' and i != 4:
                    continue
                min_value = value
                if appen:
                    path.pop()
                key = key1
                path.append(key1)
                appen = True
    q += min_value
    min_value = 1000000000000
    appen = False


path.insert(0, 'Depot')
print(q)
print(path)