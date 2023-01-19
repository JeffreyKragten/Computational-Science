from mesa import Agent

class Person(Agent):
    def __init__(self, id, model, deafness=False, genes="DD", sign_lang=0, parents=None, sex="male"):
        super().__init__(id, model)
        self.age = 0
        self.sex = sex
        self.sign_lang = sign_lang
        self.parents = parents
        self.partner = None
        self.children = []
        self.deafness = deafness
        self.genes = genes

        if self.parents:
            for parent in self.parents:
                parent.children.append(self)

    def get_family(self):
        """
        Returns the partner, (grand)children and (grant)parents and the person
        himself.
        """

        return self.get_siblings() + self.get_children() + self.get_parents()

    def get_extended_family(self):
        return self.get_family() + [self.partner] + self.partner.get_family()

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

        return self.children + [child.get_children() for child in self.children]

    def get_parents(self):
        """
        Returns the (grand)parents of the person.
        """

        return self.parents + [parent.get_parents() for parent in self.parents]

    def step(self):
        if self.age == 2:
            self.parents = None
        elif self.age > 2:
            self.model.kill_agents.append(self)
