import mesa
import random
from agent import Person


"""
Agent-based model simulator using the Mesa framework.
Initialised by specifying the size of a generation (n),
assortative marriage parameter (m), proportion of Deaf agents in first generation (d),
proportion of 'carrying' agents in first generation.
"""

class SignModel(mesa.Model):
    def __init__(self, n, m, d, c):
        self.agents_per_gen = n
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
             "percentage_fluent_signers": self.percentage_fluent_signers,
             "percentage_non_fluent_signers": self.percentage_non_fluent_signers,
             "percentage_deaf": self.percentage_deaf,
             "percentage_carry": self.percentage_carry})
        for i in range(self.agents_per_gen):
            deafness, genes, language = self.init_genes(d, c)
            a = Person(i, self, deafness, genes, language)
            self.schedule.add(a)


    """
    Execute agent step, remove agents age > 2, marry agents age 1,
    create new generation of agents, collect data on population.
    """
    def step(self):
        self.kill_agents = []
        self.schedule.step()
        for i in self.kill_agents:
            self.schedule.remove(i)
        self.marry()
        self.new_gen()
        self.datacollector.collect(self)


    """
    Initialize genes for first generation of agents using specified parameters.
    """
    def init_genes(self, d, c):
        possible_genes = [(True, "dd"), (False, "Dd"), (False, "dD"), (False, "DD")]
        h = 1 - d - c
        chances = [d, (c / 2), (c / 2), h]
        agent_genes = random.choices(possible_genes, chances)
        agent_deafness, agent_genes = agent_genes[0]
        agent_language = int(agent_deafness)

        return agent_deafness, agent_genes, agent_language


    """
    Randomly determine agents for child agent.
    """
    def inherit_genes(self, parents):
        gene_1 = random.choice(parents[0].genes)
        gene_2 = random.choice(parents[1].genes)
        child_genes = gene_1 + gene_2
        deafness = False
        if child_genes == "dd":
            deafness = True

        return (deafness, child_genes)


    """
    Marry all agents age 1. Marry ndm Deaf couples, nhm hearing couples,
    then marry indiscriminately.
    """
    def marry(self):
        self.married = []
        ndm, nhm = self.assortative_couples()

        self.to_marry(self.to_be_married_deaf, ndm)
        self.to_marry(self.to_be_married_hearing, nhm)
        remaining_marriage_list = self.to_be_married_deaf + self.to_be_married_hearing
        self.to_marry(remaining_marriage_list, int(len(remaining_marriage_list)/2))
        self.to_be_married_deaf = []
        self.to_be_married_hearing = []


    """
    Iterate through agent list to find suitable couples.
    """
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


    """
    Determine the number of assortative marriages:
    nd = number of deaf agents age 1
    nk = number of hearing agents age 1
    Multiply numbers by assortative marriage value, divide by 2 for number of couples.
    """
    def assortative_couples(self):
        nd = len(self.to_be_married_deaf)
        nk = self.agents_per_gen - nd
        return int((nd*self.assortative_marriage)/2), int((nk*self.assortative_marriage)/2)


    """
    Agents are able to marry if they are of opposite sex and not siblings.
    """
    def able_to_marry(self, agent, partner):
        return not (agent.sex == partner.sex or agent in partner.get_siblings())


    """
    Agents learn sign language of their partner is a signer.
    """
    def wedding(self, agent, partner):
        agent.partner = partner
        partner.partner = agent
        self.share_language(agent, partner)
        self.married.extend((agent, partner))
        return True


    """
    both agents a couple learn non-fluent signing if there
    is at least one Deaf person and one singing person in the couple.
    """
    def share_language(self, agent, partner):
        if agent.sign_lang == partner.sign_lang:
            return

        couple = (agent, partner)
        if any(person.deafness for person in couple):
            if any(person.sign_lang > 0 for person in couple):
                if agent.sign_lang == 0:
                    agent.sign_lang = 0.5
                if partner.sign_lang == 0:
                    partner.sign_lang = 0.5


    """
    Create new generation of agents by randomly choosing recently married couples.
    New agents inherit genes and possibly deafness from parents and are added to
    the scheduler.
    """
    def new_gen(self):
        for k in range(self.total_agents, self.agents_per_gen + self.total_agents):
            agent = random.choice(self.married)
            partner = agent.partner
            deafness, genes = self.inherit_genes((agent, partner))
            child = Person(k, self, deafness, genes, None, (agent, partner))
            self.schedule.add(child)
        self.total_agents += self.agents_per_gen



    """
    Data collecting functions.
    """
    def amount_deaf(self):
        return len([agent for agent in self.schedule.agents if agent.deafness and agent.age == 1])


    def percentage_signers(self):
        num_signers = len([agent for agent in self.schedule.agents if agent.sign_lang > 0])
        return num_signers / self.schedule.get_agent_count()


    def percentage_non_fluent_signers(self):
        num_signers = len([agent for agent in self.schedule.agents if agent.sign_lang == 0.5])
        return num_signers / self.schedule.get_agent_count()


    def percentage_fluent_signers(self):
        num_signers = len([agent for agent in self.schedule.agents if agent.sign_lang == 1])
        return num_signers / self.schedule.get_agent_count()


    def percentage_deaf(self):
        return len([agent for agent in self.schedule.agents
            if agent.deafness]) / self.schedule.get_agent_count()


    def percentage_carry(self):
        return len([agent for agent in self.schedule.agents
            if agent.genes in ["dD", "Dd"]]) / self.schedule.get_agent_count()
