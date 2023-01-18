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
        self.datacollector = mesa.DataCollector(model_reporters={"agent_count": lambda m: m.schedule.get_agent_count()})
        for i in range(self.num_agents):
            deafness, genes = self.init_genes(d, c)
            a = Person(i, self, 0, None, None, None, deafness)
            self.schedule.add(a)


    def init_genes(self, d, c):
        # possible_genes = [("deaf", "dd"), ("carrying", "Dd"), ("carrying", "dD"), ("hearing", "DD")]
        possible_genes = [(True, "dd"), (False, "Dd"), (False, "dD"), (False, "DD")]
        h = 1 - d - c
        chances = [d, (c / 2), (c / 2), h]
        agent_genes = random.choices(possible_genes, chances)
        return agent_genes[0]


    def inherit_genes(self, parents):
        gene_1 = random.choice(parents[0].genes)
        gene_2 = random.choice(parents[1].genes)
        child_genes = gene_1 + gene_2
        if child_genes == "dd":
            deafness = True
        else:
            deafness = False

        return (deafness, child_genes)


    def step(self):
        self.kill_agents = []
        self.age()
        self.schedule.step()
        for i in self.kill_agents:
            self.schedule.remove(i)
        self.marry()
        self.new_gen()
        self.datacollector.collect(self)


    def percentage_signers(self):
        agents = self.schedule.agents
        num_signers = len([agent for agent in agents if agent.sign_lang == 1])
        return num_signers / self.num_agents


    def marry(self):
        for agent in self.agents_age_1:
            self.agents_age_1.remove(agent)
            found = False
            no_require_deaf = False if random.random() < self.assortative_marriage or agent.deafness == False else True
            while found == False:
                partner = random.choice(self.agents_age_1)
                if partner.deafness or no_require_deaf or True: # Need to decide what to do in case of odd number of deaf people
                    found = self.wedding(agent, partner)


    def wedding(self, agent, partner):
        agent.partner = partner
        partner.partner = agent
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
        agents = self.schedule.agents
        for agent in agents:
            if agent.age == 0:
                self.agents_age_1.append(agent)
            agent.age += 1
