from pyrally import RallyAPIClient, settings as rally_settings

from centipede.models import Ticket
from centipede.plugins import PluginInterface


def get_ticket_from_rally_object(rally_obj):
    return Ticket(
            description=rally_obj.Description,
            title=rally_obj.name,
            owner=rally_obj.Owner.DisplayName,
            state=rally_obj.ScheduleState,
        )


class Rally(PluginInterface):

    def get(self, ticket_id):
        client = RallyAPIClient(rally_settings.RALLY_USERNAME,
                                rally_settings.RALLY_PASSWORD)
        story = client.get_story_by_name(ticket_id)
        return get_ticket_from_rally_object(story)
