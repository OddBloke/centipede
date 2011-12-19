from pyrally.client import RallyAPIClient

from centipede.plugins import PluginInterface


class Rally(PluginInterface):

    def get(self, ticket_id):
        RallyAPIClient('', '').get_story_by_name(ticket_id)
