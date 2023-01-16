INITIAL_POP = 10
INITIAL_PROFICIENCY = 0.5
ITERATIONS = 3
MARRIAGES = 2


class Person:
    def __init__(self, sign_lang, parent1, parent2):
        self.age = 1
        self.sign_lang = sign_lang
        self.parent1 = parent1
        self.parent2 = parent2
        self.partner = None
        self.child = None


# Initialize population. First generation has no parents.
persons_unmarried = list()
persons_married = list()
for i in range(INITIAL_POP):
    persons_unmarried.append(Person(INITIAL_PROFICIENCY, None, None))



def learn(sign_1, sign_2):
    return (sign_1 + sign_2) / 3

def marry(num):
    for j in range(num):
        parent1 = persons_unmarried[j]
        parent2 = persons_unmarried[j + num]
        parent1.partner = parent2
        parent2.partner = parent1
        proficiency = learn(parent1.sign_lang, parent2.sign_lang)
        baby = Person(proficiency, parent1, parent2)
        persons_unmarried.append(baby)
        persons_married.append(parent1)
        persons_unmarried.remove(parent1)
        persons_married.append(parent2)
        persons_unmarried.remove(parent2)
        parent1.child = baby
        parent2.child = baby

def age():
    for person in persons_unmarried:
        person.age += 1
    for person in persons_married:
        person.age += 1

def average(lst):
    return sum(lst) / len(lst)

def run():
    for j in range(ITERATIONS):
        age()
        marry(MARRIAGES)
        print(average([p.sign_lang for p in persons_unmarried]))
        print(f"Round: {j}, unmarried: {len(persons_unmarried)}, married: {len(persons_married)}")


run()
