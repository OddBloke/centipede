from pyrally.client import RallyAPIClient

from centipede.plugins import PluginInterface


def get_ticket_from_rally_object():
    pass


class Rally(PluginInterface):

    def get(self, ticket_id):
        story = RallyAPIClient('', '').get_story_by_name(ticket_id)
        return get_ticket_from_rally_object(story)
