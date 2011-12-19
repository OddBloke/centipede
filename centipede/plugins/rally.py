from pyrally import RallyAPIClient, settings as rally_settings

from centipede.tracker import TrackerInterface
from centipede.tracker.entities import Ticket


def get_ticket_from_rally_object(rally_obj):
    owner = rally_obj.Owner
    if owner is not None:
        owner = owner.DisplayName
    return Ticket(
            identifier=rally_obj.FormattedID,
            description=rally_obj.Description,
            title=rally_obj.Name,
            owner=owner,
            state=rally_obj.ScheduleState,
        )


class Rally(TrackerInterface):

    def get_ticket(self, ticket_id):
        client = RallyAPIClient(rally_settings.RALLY_USERNAME,
                                rally_settings.RALLY_PASSWORD)
        story = client.get_story_by_name(ticket_id)
        return get_ticket_from_rally_object(story)
