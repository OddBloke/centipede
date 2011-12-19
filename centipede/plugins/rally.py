from pyrally import RallyAPIClient

from centipede.models import Ticket
from centipede.plugins import PluginInterface


def get_ticket_from_rally_object(rally_obj):
    return Ticket(
            description=rally_obj.Description,
            title=rally_obj.name,
            owner=rally_obj.user.DisplayName,
            state=rally_obj.ScheduleState,
        )


class Rally(PluginInterface):

    def get(self, ticket_id):
        story = RallyAPIClient('', '').get_story_by_name(ticket_id)
        return get_ticket_from_rally_object(story)
