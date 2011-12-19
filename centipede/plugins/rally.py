from pyrally import RallyAPIClient, settings as rally_settings

from centipede.models import Ticket
from centipede.tracker import TrackerInterface


def get_ticket_from_rally_object(rally_obj):
    owner = rally_obj.Owner
    if owner is not None:
        owner = owner.DisplayName
    return Ticket(
            description=rally_obj.Description,
            title=rally_obj.Name,
            owner=owner,
            state=rally_obj.ScheduleState,
        )


class Rally(TrackerInterface):

    def get(self, ticket_id):
        client = RallyAPIClient(rally_settings.RALLY_USERNAME,
                                rally_settings.RALLY_PASSWORD)
        story = client.get_entity_by_name(ticket_id)
        return get_ticket_from_rally_object(story)
