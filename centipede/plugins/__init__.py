class PluginInterface(object):

    def get(self, ticket_id):
        raise NotImplementedError()
