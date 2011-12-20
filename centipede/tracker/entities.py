
class IAmSterile(Exception):
    """
    Exception to be raised when entity cannot have any children.

    Means children option is not implemented.
    
    """

class Ticket(object):

    def __init__(self, identifier, description, title, owner, state):
        self.identifier = identifier
        self.description = description
        self.title = title
        self.owner = owner
        self.state = state

    def as_dict(self):
        d = {}
        for attribute in ['identifier', 'description', 'title', 'owner',
                          'state']:
            d[attribute] = getattr(self, attribute)
        return d
