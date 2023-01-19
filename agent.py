from mesa import Agent
from random import choice

class Person(Agent):
    def __init__(self, id, model, deafness=False, genes="DD", sign_lang=0, parents=None, partner=None, children=[]):
        super().__init__(id, model)
        self.age = 0
        self.sex = "male" if choice([False, True]) else "female"
        self.sign_lang = sign_lang
        self.parents = parents
        self.partner = partner
        self.children = children
        self.deafness = deafness
        self.genes = genes

        if self.parents:
            for parent in list(self.parents):
                parent.children.append(self)

        if self.partner:
            self.partner.partner = self

        # for child in self.children:
        #     child.parents = tuple(list(child.parents) + [self])

    def get_family(self):
        """
        Returns the partner, (grand)children and (grant)parents and the person
        himself.
        """

        return [self.partner] + self.get_siblings() + self.get_children() + self.get_parents()

    def get_siblings(self):
        return self.parents[0].children if self.parents else []

    def get_children(self):
        return self.children + [child.get_children() for child in self.children]

    def get_parents(self):
        return self.parents + [parent.get_parents() for parent in self.parents]

    def step(self):
        if self.age == 2:
            self.parents = None
        elif self.age > 2:
            self.model.kill_agents.append(self)
