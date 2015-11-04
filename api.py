"""Bardemir World API implemented using Google Cloud Endpoints.

Defined here are the ProtoRPC messages needed to define Schemas for methods
as well as those methods defined in an API.
"""

import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote

# TODO: Replace the following lines with client IDs obtained from the APIs
# Console or Cloud Console.
WEB_CLIENT_ID = 'replace this with your web client application ID'
ANDROID_CLIENT_ID = 'replace this with your Android client ID'
IOS_CLIENT_ID = 'replace this with your iOS client ID'
ANDROID_AUDIENCE = WEB_CLIENT_ID

package = 'Bardemir'

class Event(messages.Message):
    """Greeting that stores a message."""
    description = messages.StringField(1)


class EventsCollection(messages.Message):
    """Collection of Events."""
    items = messages.MessageField(Event, 1, repeated=True)


STORED_EVENTS = EventsCollection(items=[
    Event(description='Event 1'),
    Event(description='Event 2'),
])

@endpoints.api(name='bardemir', version='v1',
               allowed_client_ids=[WEB_CLIENT_ID, ANDROID_CLIENT_ID,
                                   IOS_CLIENT_ID],
               audiences=[ANDROID_AUDIENCE])
class BardemirService(remote.Service):
    """Bardemir API v1."""

    @endpoints.method(message_types.VoidMessage, EventsCollection,
                      path='listEvents', http_method='GET',
                      name='events.list')
    def listEvents(self, unused_request):
        return STORED_EVENTS

    ID_RESOURCE = endpoints.ResourceContainer(
            message_types.VoidMessage,
            id=messages.IntegerField(1, variant=messages.Variant.INT32))

    @endpoints.method(ID_RESOURCE, Event,
                      path='event/{id}', http_method='GET',
                      name='events.getEvent')
    def getEvent(self, request):
        try:
            return STORED_EVENTS.items[request.id]
        except (IndexError, TypeError):
            raise endpoints.NotFoundException('Event %s not found.' %
                                              (request.id,))


APPLICATION = endpoints.api_server([BardemirService])
