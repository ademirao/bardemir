"""Bardemir World API implemented using Google Cloud Endpoints.

Defined here are the ProtoRPC messages needed to define Schemas for methods
as well as those methods defined in an API.
"""

import pprint
import endpoints

from properties.properties import Properties 
from bardemir_producer import BardemirProducer
from messages import Profile, Ride, RidesCollection, Hitchhike, HitchhikesCollection, Event
from messages import STORED_HITCHHIKES, STORED_RIDES, upsert

from google.appengine.api import urlfetch
from protorpc import messages
from protorpc import message_types
from protorpc import remote
from facebook_api import FacebookApi

# TODO: Replace the following lines with client IDs obtained from the APIs
# Console or Cloud Console.
WEB_CLIENT_ID = 'replace this with your web client application ID'
ANDROID_CLIENT_ID = 'replace this with your Android client ID'
IOS_CLIENT_ID = 'replace this with your iOS client ID'
ANDROID_AUDIENCE = WEB_CLIENT_ID
PPRINTER = pprint.PrettyPrinter(indent=4)

package = 'Bardemir'
class EmptyRequest(messages.Message):
  auth=messages.StringField(1)

class UpsertRideRequest(messages.Message):
  auth=messages.StringField(1)
  ride=messages.MessageField(Ride, 2)

class UpsertRideResponse(messages.Message):
  ride = messages.MessageField(Ride, 1)

class UpsertHitchhikeRequest(messages.Message):
  auth=messages.StringField(1)
  hitchhike=messages.MessageField(Hitchhike, 2)
 
class UpsertHitchhikeResponse(messages.Message):
  hitchhike=messages.MessageField(Hitchhike, 2)

class RemoveRequest(messages.Message):
  auth=messages.StringField(1)
  id=messages.StringField(2)

class EventsResponse(messages.Message):
  events = messages.MessageField(Event, 1, repeated=True)

def pprint(result):
  print(result)

@endpoints.api(name='bardemir', version='v1',
               allowed_client_ids=[WEB_CLIENT_ID, ANDROID_CLIENT_ID,
                                   IOS_CLIENT_ID],
               audiences=[ANDROID_AUDIENCE])
class BardemirService(remote.Service):

    """Bardemir API v1."""
    @endpoints.method(UpsertRideRequest, UpsertRideResponse,
                      http_method='POST',
                      name='rides.upsert')
    def upsertRide(self, request):
      return BardemirProducer(FacebookApi(request.auth)).upsertRide(
          request.ride).then(
              lambda ride: UpsertRideResponse(ride=ride)).wait().result

    @endpoints.method(RemoveRequest, message_types.VoidMessage,
                      http_method='POST',
                      name='rides.remove')
    def removeRide(self, request):
      return BardemirProducer(FacebookApi(request.auth)).removeRide(
          request.id).then(lambda r: message_types.VoidMessage()).wait().result

    @endpoints.method(UpsertHitchhikeRequest, UpsertHitchhikeResponse,
                      http_method='POST',
                      name='hitchhike.upsert')
    def upsertHitchhike(self, request):
      return BardemirProducer(FacebookApi(request.auth)).upsertHitchhike(
          request.hitchhike).then(
              lambda hitchhike: UpsertHitchhikeResponse(hitchhike=hitchhike)
              ).wait().result

    @endpoints.method(RemoveRequest, message_types.VoidMessage,
                      http_method='POST',
                      name='hitchhike.remove')
    def removeHitchhike(self, request):
      return BardemirProducer(FacebookApi(request.auth)).removeHitchhike(
          request.id).then(lambda r: message_types.VoidMessage()).wait().result

    @endpoints.method(EmptyRequest, message_types.VoidMessage,
                      http_method='POST',
                      name='admin.setToken')
    def setToken (self, request):
      def setToken(profile):
        if profile.id != Properties().admin_facebook_id:
          print("NOT SETTING! " + str(profile.id) + " != " + str(Properties().admin_facebook_id))
          return message_types.VoidMessage() 

        prop = Properties()
        prop.admin_auth_token = request.auth
        prop.put()
        return message_types.VoidMessage();

      return BardemirProducer(FacebookApi(request.auth)).getProfile().then(setToken).wait().result

    @endpoints.method(EmptyRequest, RidesCollection,
                      http_method='GET',
                      name='rides.list')
    def listRides(self, request):
      return RidesCollection(items=STORED_RIDES.items);

    @endpoints.method(EmptyRequest, HitchhikesCollection,
                      http_method='GET',
                      name='hitchhike.list')
    def listHitchhikes(self, request):
      return HitchhikesCollection(items=STORED_HITCHHIKES.items);

    @endpoints.method(EmptyRequest, EventsResponse,
                      http_method='GET',
                      name='events.get')
    def events(self, request):
      return BardemirProducer(FacebookApi(request.auth)).getEvents().then(
          lambda events: EventsResponse(events = events)).wait().result

    @endpoints.method(EmptyRequest, Profile,
                      http_method='GET',
                      name='profile.get')
    def getProfile(self, request):
      return BardemirProducer(FacebookApi(request.auth)).getProfile().wait().result

APPLICATION = endpoints.api_server([BardemirService])
