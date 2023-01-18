from mesa import Agent
from random import choice

class Person(Agent):
    def __init__(self, id, model, sign_lang=0, parents=(), partner=None, children=[], deafness=False, genes=None):
        super().__init__(id, model)
        self.age = 0
        self.sex = "male" if choice([False, True]) else "female"
        self.sign_lang = sign_lang
        self.parents = parents
        self.partner = partner
        self.children = children
        self.deafness = deafness
        self.genes = genes

        # for parent in self.parents:
        #     parent.children.append(self)

        if self.partner:
            self.partner.partner = self

        # for child in self.children:
        #     child.parents.append(self)

    def get_family(self):
        """
        Returns the partner, (grand)children and (grant)parents and the person
        himself.
        """

        return self.parents[0].children + [self.partner] + self.get_children() + self.get_parents()

    def get_children(self):
        return self.children + [child.get_children() for child in self.children]

    def get_parents(self):
        return self.parents + [parent.get_parents() for parent in self.parents]

    def die(self):
        if self.children is not None:
            for child in self.children:
                child.parents.remove(self)
        self.model.kill_agents.append(self)

    def step(self):
        if self.age > 2:
            self.die()
