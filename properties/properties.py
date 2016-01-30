import webapp2
from google.appengine.ext import ndb
import os

class BardemirProperties(ndb.Model):
  admin_facebook_id = ndb.StringProperty()
  admin_auth_token = ndb.StringProperty()
  group_id = ndb.StringProperty()
  client_id = ndb.StringProperty()

PROPERTIES_KEY_STR = "properties@bardemir-api.appspot.com"
PROPERTIES_KEY = ndb.Key(BardemirProperties, PROPERTIES_KEY_STR)
GROUP_ID = "371519946346115"
CLIENT_ID = "433202543531394"
ADMIN_FACEBOOK_ID = "107332446315090"

def Properties():
  properties = PROPERTIES_KEY.get()
  if properties:
    return properties

  resetProperties()
  return PROPERTIES_KEY.get()

def resetProperties():
  bardemir_properties = BardemirProperties(
      admin_facebook_id=ADMIN_FACEBOOK_ID, admin_auth_token="",
      group_id=GROUP_ID, client_id=CLIENT_ID, id=PROPERTIES_KEY_STR)
  bardemir_properties.put()
