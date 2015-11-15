import webapp2
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
import os

class BardemirProperties(ndb.Model):
  facebook_secret = ndb.StringProperty()

PROPERTIES_KEY = "properties@bardemir.appspot.com"
PROPERTIES = ndb.Key(BardemirProperties, PROPERTIES_KEY)

CLIENT_ID = "433202543531394"
FACEBOOK_URL = "https://graph.facebook.com/v2.3/oauth/access_token?"

if os.environ['SERVER_SOFTWARE'].startswith('Development'):
  REDIRECT_URL = "http://localhost:8080/login"
else:
  REDIRECT_URL = "https://bardemir-api.appspot.com/login"

HOME_PAGE="""
<html>
<body>

<a href="https://www.facebook.com/dialog/oauth?client_id=433202543531394&redirect_uri=%s">
Allow Bardemir to see my facebook information
</a>

<form action="appsecret" method="POST">
  App Secret: <input type="password" name="secret"><br>
  <input type="submit" name=change value="define">
  <input type="submit" name=delete value="delete">
</form>

</body>
</html>
""" % REDIRECT_URL

class HomePage(webapp2.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/html charset=utf-8'
    self.response.write(HOME_PAGE)

class LoginPage(webapp2.RequestHandler):
  def get(self):
    code=self.request.get("code")
    self.response.headers['Content-Type'] = 'text/plain'

    bardemir_properties = PROPERTIES.get()
    if not bardemir_properties or not bardemir_properties.facebook_secret:
      self.response.write('Missing bardemir properties ')
      return

    url = "%sclient_id=%s&redirect_uri=%s&client_secret=%s&code=%s" % (
                    FACEBOOK_URL,
                    CLIENT_ID,
                    REDIRECT_URL,
                    bardemir_properties.facebook_secret,
                    code)
    result = urlfetch.fetch(url)
    self.response.write('Done')
    self.response.write(result.content)

class SetAppSecret(webapp2.RequestHandler):
  def post(self):
    if self.request.get("delete"):
      PROPERTIES.delete()
      self.response.write("App secret deleted")
      return

    secret = self.request.get("secret")
    if not secret:
      self.response.write("App secret is mandatory")
      return

    bardemir_properties = PROPERTIES.get()
    if bardemir_properties:
      bardemir_properties.facebook_secret = secret
    else:
      bardemir_properties = BardemirProperties(facebook_secret=secret,
                      id=PROPERTIES_KEY)
    bardemir_properties.put()
    self.response.write('Done')

APPLICATION = webapp2.WSGIApplication([
  ('/login', LoginPage),
  ('/appsecret', SetAppSecret),
  ('/.*', HomePage),
], debug=True)
