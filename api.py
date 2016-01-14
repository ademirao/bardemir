"""Bardemir World API implemented using Google Cloud Endpoints.

Defined here are the ProtoRPC messages needed to define Schemas for methods
as well as those methods defined in an API.
"""

import pprint
import endpoints
import json
from messages import Profile, Ride, RidesCollection, Hitchhike, HitchhikesCollection
from messages import STORED_HITCHHIKES, STORED_RIDES
from properties.properties import Properties 
from google.appengine.api import urlfetch
from protorpc import messages
from protorpc import message_types
from protorpc import remote

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
      STORED_RIDES.items.append(request.ride)
      return UpsertRideResponse(ride=request.ride);

    @endpoints.method(UpsertHitchhikeRequest, UpsertHitchhikeResponse,
                      http_method='POST',
                      name='hitchhike.upsert')
    def upsertHitchhike(self, request):
      STORED_HITCHHIKES.items.append(request.hitchhike)
      return UpsertHitchhikeResponse(hitchhike=request.hitchhike);

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

    @endpoints.method(EmptyRequest, Profile,
                      http_method='GET',
                      name='profile.get')
    def getProfile(self, request):
      bardemir_properties = Properties()
      pictureUrl= "https://graph.facebook.com/v2.5/me/picture?access_token=%s&redirect=false&type=small&width=20" % (request.auth)
      profileUrl = "https://graph.facebook.com/v2.5/me?access_token=%s&redirect=false" % (request.auth)
      resultPicture = urlfetch.fetch(pictureUrl)
      pictureResponse = json.loads(resultPicture.content)
      resultProfile = urlfetch.fetch(profileUrl)
      profileResponse = json.loads(resultProfile.content)
      return Profile(
          id=profileResponse['id'],
          name=profileResponse['name'],
          photoUrl=pictureResponse['data']['url'])


APPLICATION = endpoints.api_server([BardemirService])
