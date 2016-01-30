import webapp2
from google.appengine.ext import ndb
import os
from properties.properties import Properties, resetProperties
from bardemir_producer import BardemirProducer
from facebook_api import FacebookApi

def home_page():
  return BardemirProducer(FacebookApi(Properties().admin_auth_token)).getProfile().then(
      lambda result: """
<html>
<body>
Broker <b>%s</b>
<form action="/SetProperty" method="POST">
  Group Id: <input type="text" name="group_id"><br>
  <input type="submit" name=change value="define">
  <input type="submit" name=reset value="reset">
</form>

</body>
</html>
""" % (result.name)).wait().result

class PropertyHome(webapp2.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/html charset=utf-8'
    self.response.write(home_page())

class SetProperty(webapp2.RequestHandler):
  def get(self):
    self.post()
    
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
  ('/SetProperty', SetProperty),
  ('.*', PropertyHome),
])
