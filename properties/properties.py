import webapp2
from google.appengine.ext import ndb
import os

class BardemirProperties(ndb.Model):
  group_id = ndb.StringProperty()
  client_id = ndb.StringProperty()

PROPERTIES_KEY_STR = "properties@bardemir-api.appspot.com"
PROPERTIES_KEY = ndb.Key(BardemirProperties, PROPERTIES_KEY_STR)
GROUP_ID = "371519946346115"
CLIENT_ID = "433202543531394"

def Properties():
  properties = PROPERTIES_KEY.get()
  if properties:
    return properties

  resetProperties()
  return PROPERTIES_KEY.get()

def resetProperties():
  bardemir_properties = BardemirProperties(group_id=GROUP_ID,
      client_id=CLIENT_ID, id=PROPERTIES_KEY_STR)
  bardemir_properties.put()

def home_page():
  return """
<html>
<body>
<form action="/properties/SetProperty" method="POST">
  Group Id: <input type="text" name="group_id"><br>
  <input type="submit" name=change value="define">
  <input type="submit" name=reset value="reset">
</form>

</body>
</html>
"""


class PropertyHome(webapp2.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/html charset=utf-8'
    self.response.write(home_page())

class SetProperty(webapp2.RequestHandler):
  def post(self):
    if self.request.get("reset"):
      resetProperties();
      self.response.write("Properties reset")
      return

    group_id = self.request.get("group_id")
    bardemir_properties = Properties()

    if group_id:
      bardemir_properties.group_id = group_id

    bardemir_properties.put()
    self.response.write('Done')

APPLICATION = webapp2.WSGIApplication([
  ('/properties/SetProperty', SetProperty),
  ('/properties.*', PropertyHome),
])
