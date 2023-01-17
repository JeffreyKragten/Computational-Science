import mesa
import random
from agent import Person


# model_reporters={"percentage_of_signers": self.percentage_signers
# "agent_count": lambda m: m.schedule.get_agent_count()

class SignModel(mesa.Model):
    def __init__(self, n, m, d, c):
        self.num_agents = n
        self.total_agents = n
        self.assortative_marriage = m
        self.schedule = mesa.time.RandomActivation(self)
        self.agents_age_1 = []
        self.kill_agents = []
        self.running = True
        self.datacollector = mesa.DataCollector(model_reporters={"percentage_of_signers": self.percentage_signers})
        for i in range(self.num_agents):
            deafness = True if random.random() < d else False
            a = Person(i, self, 0, None, None, None, deafness)
            self.schedule.add(a)


    def step(self):
        self.kill_agents = []
        self.datacollector.collect(self)
        self.schedule.step()
        for i in self.kill_agents:
            self.schedule.remove(i)

    def percentage_signers(self):
        agents = self.schedule.agents
        num_signers = len([agent for agent in agents if agent.sign_lang == 1])
        return num_signers / self.num_agents


    def marry(self):
        for agent in self.agents_age_1:
            self.agents_age_1.remove(agent)
            found = False
            if agent.deafness == True:
                no_require_deaf = False if random.random() < self.assortative_marriage else True
                while found == False:
                    partner = random.choice(self.agents_age_1)
                    """ Boolean logic to ensure deaf person marries deaf person at required percentage"""
                    if partner.married == False and (partner.deafness or no_require_deaf):
                        found = self.wedding(agent, partner)
            else:
                while found == False:
                    partner = random.choice(self.agents_age_1)
                    if partner.married == False:
                        found = self.wedding(agent, partner)


    def wedding(self, agent, partner):
        agent.partner = partner
        agent.married = True
        partner.partner = agent
        partner.married = True
        self.agents_age_1.remove(partner)
        return True


    def new_gen(self):
        for k in range(self.total_agents, self.num_agents + self.total_agents):
            agent = random.choice(self.agents_age_1)
            partner = agent.partner
            child = Person(k, self, 0, (agent, partner), None, None)
            self.schedule.add(child)
        self.total_agents += self.num_agents


    def age(self):
        agents = self.schedule.agent_buffer()
        debug_num = 0
        while True:
            try:
                agent = next(agents)
                if agent.age == 0:
                    self.agents_age_1.append(agent)
                # if agent.age == 1:
                #     self.agents_age_1.remove(agent)
                agent.age += 1
                debug_num += 1
            except StopIteration:
                break
            print(f"Aged {debug_num} agents!")




# INITIAL_POP = 10
# INITIAL_PROFICIENCY = 0.5
# ITERATIONS = 3
# MARRIAGES = 2


# class Person:
#     def __init__(self, sign_lang, parent1, parent2):
#         self.age = 1
#         self.sign_lang = sign_lang
#         self.parent1 = parent1
#         self.parent2 = parent2
#         self.partner = None
#         self.child = None


# # Initialize population. First generation has no parents.
# persons_unmarried = list()
# persons_married = list()
# for i in range(INITIAL_POP):
#     persons_unmarried.append(Person(INITIAL_PROFICIENCY, None, None))


# def learn(sign_1, sign_2):
#     return (sign_1 + sign_2) / 3

# def marry(num):
#     for j in range(num):
#         parent1 = persons_unmarried[j]
#         parent2 = persons_unmarried[j + num]
#         parent1.partner = parent2
#         parent2.partner = parent1
#         proficiency = learn(parent1.sign_lang, parent2.sign_lang)
#         baby = Person(proficiency, parent1, parent2)
#         persons_unmarried.append(baby)
#         persons_married.append(parent1)
#         persons_unmarried.remove(parent1)
#         persons_married.append(parent2)
#         persons_unmarried.remove(parent2)
#         parent1.child = baby
#         parent2.child = baby

# def age():
#     for person in persons_unmarried:
#         person.age += 1
#     for person in persons_married:
#         person.age += 1

# def average(lst):
#     return sum(lst) / len(lst)

# def run():
#     for j in range(ITERATIONS):
#         age()
#         marry(MARRIAGES)
#         print(average([p.sign_lang for p in persons_unmarried]))
#         print(f"Round: {j}, unmarried: {len(persons_unmarried)}, married: {len(persons_married)}")


# run()
