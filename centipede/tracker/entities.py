class Ticket(object):

    def __init__(self, identifier, description, title, owner, state):
        self.identifier = identifier
        self.description = description
        self.title = title
        self.owner = owner
        self.state = state
