class Ticket(object):

    def __init__(self, description, title, owner, state):
        super(Ticket, self).__init__()
        self.description = description
        self.title = title
        self.owner = owner
        self.state = state
