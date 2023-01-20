import mesa
import random
from agent import Person

# model_reporters={"percentage_of_signers": self.percentage_signers
# "agent_count": lambda m: m.schedule.get_agent_count()

class SignModel(mesa.Model):
    def __init__(self, n, m, d, c):
        self.d = d
        self.num_agents = n
        self.total_agents = n
        self.assortative_marriage = m
        self.schedule = mesa.time.RandomActivation(self)
        self.to_be_married_deaf = []
        self.to_be_married_hearing = []
        self.married = []
        self.kill_agents = []
        self.running = True
        self.datacollector = mesa.DataCollector(model_reporters=
            {"agent_count": lambda m: m.schedule.get_agent_count(),
             "percentage_signers": self.percentage_signers,
             "percentage_deaf": self.percentage_deaf,
             "percentage_carry": self.percentage_carry})
        sex = "male"
        for i in range(self.num_agents):
            if i >= self.num_agents / 2:
                sex = "female"
            deafness, genes, language = self.init_genes(d, c)
            a = Person(i, self, deafness, genes, language)
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
        possible_genes = [(True, "dd"), (False, "Dd"), (False, "dD"), (False, "DD")]
        h = 1 - d - c
        chances = [d, (c / 2), (c / 2), h]
        agent_genes = random.choices(possible_genes, chances)
        agent_deafness, agent_genes = agent_genes[0]
        agent_language = 0
        if agent_deafness:
            agent_language = 1

        return agent_deafness, agent_genes, agent_language


    def inherit_genes(self, parents):
        gene_1 = random.choice(parents[0].genes)
        gene_2 = random.choice(parents[1].genes)
        child_genes = gene_1 + gene_2
        deafness = False
        if child_genes == "dd":
            deafness = True

        return (deafness, child_genes)

    def percentage_signers(self):
        agents = self.schedule.agents
        num_signers = len([agent for agent in agents if agent.sign_lang == 1])
        return num_signers / self.num_agents


    def percentage_deaf(self):
        return 100 * len([agent for agent in self.schedule.agents
            if agent.deafness]) / self.schedule.get_agent_count()


    def percentage_carry(self):
        return 100 * len([agent for agent in self.schedule.agents
            if agent.genes in ["dD", "Dd"]]) / self.schedule.get_agent_count()


    def marry(self):
        ndm, nhm = self.assortative_couples()

        self.to_marry(self.to_be_married_deaf, ndm)
        self.to_marry(self.to_be_married_hearing, nhm)
        remaining_marriage_list = self.to_be_married_deaf + self.to_be_married_hearing
        self.to_marry(remaining_marriage_list, int(len(remaining_marriage_list)/2))
        self.to_be_married_deaf = []
        self.to_be_married_hearing = []

    def to_marry(self, list, amount):
        for i in range(amount):
            found = False
            tries = 0
            while not found:
                tries += 1
                agent, partner = random.sample(list, 2)
                if self.able_to_marry(agent, partner) or tries > 5:
                    found = self.wedding(agent, partner)
                    list.remove(agent)
                    list.remove(partner)


    def amount_deaf(self):
        return len([agent for agent in self.schedule.agents if agent.deafness and agent.age == 1])

    def assortative_couples(self):
        nd = len(self.to_be_married_deaf)
        nk = self.num_agents - nd
        return int((nd*self.assortative_marriage)/2), int((nk*self.assortative_marriage)/2)


    def able_to_marry(self, agent, partner):
        if agent.sex == partner.sex:
            return False
        if agent in partner.get_siblings():
            return False
        return True


    def wedding(self, agent, partner):
        agent.partner = partner
        partner.partner = agent
        self.share_language(agent, partner)
        self.married.extend((agent, partner))
        return True

    def share_language(self, agent, partner):
        if agent.sign_lang and partner.sign_lang == 1:
            return
        elif agent.sign_lang and partner.sign_lang == 0:
            return
        else:
            family_1 = agent.deaf_family_member() # return true if deaf person in family
            family_2 = partner.deaf_family_member()
            if family_1:
                partner.sign_lang = 1
            if family_2:
                agent.sign_lang = 1


    def new_gen(self):
        self.d = 0
        # num_women = self.num_agents / 2
        for k in range(self.total_agents, self.num_agents + self.total_agents):
            # num_women -= 1
            # sex = "female"
            # if num_women > 0:
            #     sex = "male"
            agent = random.choice(self.married)
            partner = agent.partner
            deafness, genes = self.inherit_genes((agent, partner))
            child = Person(k, self, deafness, genes, None, (agent, partner))
            self.schedule.add(child)
        self.total_agents += self.num_agents


    def age(self):
        agents = self.schedule.agents
        for agent in agents:
            if agent.age == 0:
                if agent.deafness:
                    self.to_be_married_deaf.append(agent)
                else:
                    self.to_be_married_hearing.append(agent)
            agent.age += 1
        self.married = []
