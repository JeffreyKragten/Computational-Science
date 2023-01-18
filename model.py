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
        self.to_be_married = []
        self.married = []
        self.kill_agents = []
        self.running = True
        self.datacollector = mesa.DataCollector(model_reporters=
            {"agent_count": lambda m: m.schedule.get_agent_count(),
             "percentage_signers": self.percentage_signers,
             "percentage_deaf": self.percentage_deaf,
             "percentage_carry": self.percentage_carry,
             "percentage_dd": self.double_d})
        for i in range(self.num_agents):
            deafness, genes = self.init_genes(d, c)
            a = Person(i, self, deafness, genes, 0)
            self.schedule.add(a)


    def step(self):
        self.kill_agents = []
        self.age()
        self.schedule.step()
        for i in self.kill_agents:
            self.schedule.remove(i)
        self.marry()
        self.new_gen()
        self.datacollector.collect(self)


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


    def percentage_signers(self):
        agents = self.schedule.agents
        num_signers = len([agent for agent in agents if agent.sign_lang == 1])
        return num_signers / self.num_agents


    def percentage_deaf(self):
        return 100 * len([agent for agent in self.schedule.agents if agent.deafness]) / self.schedule.get_agent_count()


    def percentage_carry(self):
        return 100 * len([agent for agent in self.schedule.agents if agent.genes != "DD"]) / self.schedule.get_agent_count()


    def double_d(self):
        return 100 * len([agent for agent in self.schedule.agents if agent.genes == 'dd']) / self.schedule.get_agent_count()


    def marry(self):
        while self.to_be_married:
            agent = random.choice(self.to_be_married)
            self.to_be_married.remove(agent)
            found = False
            while found == False:
                """Kind of a hack to place the chance here, but makes the program work."""
                require_deaf = True if agent.deafness == True and random.random() < self.assortative_marriage else False
                partner = random.choice(self.to_be_married)
                if partner.deafness or not require_deaf or len(self.to_be_married) < 3:
                    found = self.wedding(agent, partner)


    def wedding(self, agent, partner):
        agent.partner = partner
        partner.partner = agent
        self.to_be_married.remove(partner)
        self.married.extend((agent, partner))
        return True


    def new_gen(self):
        for k in range(self.total_agents, self.num_agents + self.total_agents):
            agent = random.choice(self.married)
            partner = agent.partner
            deafness, genes = self.inherit_genes((agent, partner))
            child = Person(k, self, deafness, genes, 0, (agent, partner))
            self.schedule.add(child)
        self.total_agents += self.num_agents


    def age(self):
        agents = self.schedule.agents
        for agent in agents:
            if agent.age == 0:
                self.to_be_married.append(agent)
            if agent.age == 1:
                self.married.remove(agent)
            agent.age += 1
