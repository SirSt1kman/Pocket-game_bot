cities_lis = {'1': [1, 2], '2': [3, 4], '3': [5, 6]}
cop = {}
for key in cities_lis:
    cop[key] = cities_lis[key][:]
cop['1'].remove(1)
print(cop)
print(cities_lis)
