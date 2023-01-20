from mesa import Agent

class Person(Agent):
    def __init__(self, id, model, deafness=False, genes="DD", sign_lang=None, parents=None, sex="male"):
        super().__init__(id, model)
        self.age = 0
        self.sex = sex
        self.parents = parents
        self.partner = None
        self.children = []
        self.deafness = deafness
        self.genes = genes

        if self.parents:
            for parent in self.parents:
                parent.children.append(self)

        self.sign_lang = self.determine_language(sign_lang)


    def determine_language(self, input):
        if not input:
            family = self.get_family()
            for member in family:
                if member.genes == "dd":
                    return 1
        return input

    def get_family(self):
        """
        Returns the partner, (grand)children and (grand)parents and the person
        himself.
        """
        return self.get_siblings() + self.get_children() + self.get_parents()

    def deaf_family_member(self):
        family = self.get_family()
        for person in family:
            if person.deafness:
                return True
        return False

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
        if self.age == 2:
            self.parents = None
        elif self.age > 2:
            self.model.kill_agents.append(self)
