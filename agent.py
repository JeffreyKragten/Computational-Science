from mesa import Agent
from random import choice

class Person(Agent):
    def __init__(self, id, model, deafness=False, genes="DD", sign_lang=None, parents=None):
        super().__init__(id, model)
        self.age = 0
        self.sex = choice(["male", "female"])
        self.parents = parents
        self.partner = None
        self.children = []
        self.deafness = deafness
        self.genes = genes

        if self.parents:
            for parent in self.parents:
                parent.children.append(self)

        self.sign_lang = sign_lang if sign_lang != None else self.determine_language()


    def determine_language(self):
        family = self.get_family()
        # If nobody in the family is deaf or nobody speaks sign language.
        if not (self.deafness or any(member.deafness > 0 for member in family)) \
            or not any(member.sign_lang > 0 for member in family):
            return 0

        for member in family:
            if member.sign_lang == 0:
                member.sign_lang = 0.5

        return 1 if any(parent.sign_lang == 1 for parent in self.parents) else 0.5

    def get_family(self):
        """
        Returns the partner, (grand)children and (grand)parents and the person
        himself.
        """
        return self.get_siblings() + self.get_parents() + self.get_children()

    def get_siblings(self):
        """
        Returns the siblings of the person.
        """
        if not self.parents:
            return []
        siblings = self.parents[0].children.copy()
        siblings.remove(self)
        return siblings

    def get_children(self):
        """
        Returns the (grand)children of the person.
        """

        children = self.children
        for child in self.children:
            children += child.get_children()
        return children

    def get_parents(self):
        """
        Returns the (grand)parents of the person.
        """
        if not self.parents:
            return []

        parents = list(self.parents)
        for parent in self.parents:
            parents += parent.get_parents()
        return parents

    def step(self):
        if self.age == 0:
            if self.deafness:
                self.model.to_be_married_deaf.append(self)
            else:
                self.model.to_be_married_hearing.append(self)
        if self.age == 2:
            self.parents = None
        elif self.age > 2:
            self.model.kill_agents.append(self)
        self.age += 1
