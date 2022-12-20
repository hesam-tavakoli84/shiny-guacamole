import itertools
import random 
import math
import time
import copy
attributes = input("attribute titles : ").split()
attributes_ids = []
for i in range(len(attributes)):
    attributes_ids.append(input(f"{attributes[i]} attributes : ").split())

floor_count = len(attributes_ids[0])
same_row_querys = [["biazar", "binavayan"], ["matin", "baz"], ["hajikhani", "lenovo"], ["koori", "apple"], ["masaref", "206"], ["sad_sal_tanhayi", "pejo_pars"], ["asus", 3], ["valadkhani", 1], ["reno", "del"], ["behrooz", "benz"]]
neighboring_querys = [["zantiya", "digital"], ["pejo_pars", "behbood_tajrobe_hamkari"], ["valadkhani", "ghale_heyvanat"], ["zantiya", "microsoft"]]
query_count = 15
mutation_chance = 0.008
# gen_population = (math.factorial(floor_count)) ** len(attributes)
gen_population = 200
current_gen = []
best_child = None

def generate_random_table():
    permulated_attributes = []
    for i in range(len(attributes)):
        permulations = list(itertools.permutations(attributes_ids[i], len(attributes_ids[i])))
        permulated_attributes.append(permulations[random.randint(0, len(permulations)-1)])
    table = []
    for i in range(floor_count):
        tmp = []
        for j in range(len(attributes)):
            tmp.append(permulated_attributes[j][i])
        table.append(tmp)

    return table

def is_neighbor(table, atr1, atr2):
    for i in range(len(table)):
        if atr1 in table[i]:
            atr1_floor = i
        if atr2 in table[i]:
            atr2_floor = i

    if type(atr1) == int:
        atr1_floor = atr1 - 1
    if type(atr2) == int:
        atr2_floor = atr2 - 1

    try:
        if abs(atr1_floor - atr2_floor) == 1:
            return True
        return False
    except:
        print(table,atr1,atr2)

def on_same_row(table, atr1, atr2):
    for i in range(len(table)):
        if atr1 in table[i]:
            atr1_floor = i
        if atr2 in table[i]:
            atr2_floor = i
    if type(atr1) == int:
        atr1_floor = atr1 - 1
    if type(atr2) == int:
        atr2_floor = atr2 - 1
    try:
        return atr1_floor == atr2_floor
    except:
        print(table, atr1, atr2)
    
def get_fitness_score(table):
    fitnes_score = 0

    for i in range(len(table)):
        if "koori" in table[i]:
            atr1_floor = i
        if "shazde_koochooloo" in table[i]:
            atr2_floor = i
    if atr2_floor+1 == atr1_floor:
        fitnes_score += 1

    for query in neighboring_querys:
        fitnes_score += is_neighbor(table, query[0], query[1])
    for query in same_row_querys:
        fitnes_score += on_same_row(table, query[0], query[1])


    # fitnes_score += on_same_row(table, "valadkhani", 1)
    # fitnes_score += on_same_row(table, "biazar", "masaref")
    # fitnes_score += is_neighbor(table, "baz", 3)
    # fitnes_score += is_neighbor(table, "baz", "biazar")

    return fitnes_score

# def sort_by_fitness(gen):
#     for i in range(len(gen)):
#         for j in range(len(gen)-i-1):
#             if get_fitness_score(gen[j]) < get_fitness_score(gen[j+1]):
#                 gen[j], gen[j+1] = gen[j+1], gen[j]
#     return gen

def partition(array, low, high):
    pivot = array[high]
    i = low - 1

    for j in range(low, high):
        if get_fitness_score(array[j]) >= get_fitness_score(pivot):
            i = i + 1
            (array[i], array[j]) = (array[j], array[i])

    (array[i + 1], array[high]) = (array[high], array[i + 1])
    return i + 1


def sort_by_fitness(array, low, high):
    if low < high:
        pi = partition(array, low, high)
        sort_by_fitness(array, low, pi - 1)
        sort_by_fitness(array, pi + 1, high)

def weighted_random_choice(gen):
    weighted_gen = []
    for i in range(len(gen)):
        for j in range(get_fitness_score(gen[i])):
            weighted_gen.append(gen[i])
    return random.choice(weighted_gen), random.choice(weighted_gen)

def mutate(index, used):
    selected = attributes_ids[index][random.randint(0, len(attributes_ids[index])-1)]
    while selected in used:
        selected = attributes_ids[index][random.

adarsak, [12/20/22 2:27 PM]
randint(0, len(attributes_ids[index])-1)]
    return selected

def get_child(mom_dad):
    mom,dad = mom_dad
    used = []
    child = []
    for i in range(len(mom)):
        tmp = []
        for j in range(len(mom[i])):
            if random.random() < mutation_chance or (mom[i][j] in used and dad[i][j] in used):
                selected = mutate(j, used)
                tmp.append(selected)
                used.append(selected)
            elif mom[i][j] not in used and dad[i][j] not in used:
                if random.randint(0,1):
                    tmp.append(mom[i][j])
                    used.append(mom[i][j])
                else:
                    tmp.append(dad[i][j])
                    used.append(dad[i][j])
            elif mom[i][j] not in used and dad[i][j] in used:
                tmp.append(mom[i][j])
                used.append(mom[i][j])
            elif mom[i][j] in used and dad[i][j] not in used:
                tmp.append(dad[i][j])
                used.append(dad[i][j])
        child.append(tmp)
    return child

start = time.time()

for i in range(gen_population):
    current_gen.append(generate_random_table())
sort_by_fitness(current_gen, 0, len(current_gen)-1)
best_child = current_gen[0]

gen_count = 0
print(gen_count, get_fitness_score(best_child), "-", best_child, "\n")

while get_fitness_score(best_child) < query_count:
    before_new_gen = time.time()
    gen_count += 1
    new_gen = []
    for i in range(gen_population):
        new_gen.append(get_child(weighted_random_choice(current_gen)))
    
    current_gen = copy.copy(new_gen)
    sort_by_fitness(current_gen, 0, len(current_gen)-1)
    best_child = current_gen[0]
    print(gen_count, get_fitness_score(best_child), round(time.time() - before_new_gen, 1), best_child, "\n")

print(best_child, get_fitness_score(best_child), gen_count, time.time()-start)

# name team
# valadkhani biazar matin
# baz masaref digital

# team name pc book car
# baz masaref digital fanavary behbood_tajrobe_hamkari
# biazar matin valadkhani hajikhani behrooz
# del lenovo asus apple microsoft
# binavayan koori shazde_koochooloo sad_sal_tanhayi ghale_heyvanat
# benz 206 zantiya reno pejo_pars
