from google.appengine.api import urlfetch
from promises import Promise 

class FacebookApi:
  def __init__(self, authToken):
    self.base_url = 'https://graph.facebook.com/v2.5'
    self.authToken = authToken

  def __fetch(self, url):
      rpc = urlfetch.create_rpc()
      promise = Promise(lambda: rpc.wait())
      rpc.callback = lambda: promise.resolve(rpc.get_result())
      full_url = self.base_url + url
      urlfetch.make_fetch_call(rpc, full_url)
      return promise

  def me(self):
    return self.__fetch("/me?access_token=%s&redirect=false" % self.authToken)

  def picture(self):
    return self.__fetch(
        "/me/picture?access_token=%s&redirect=false&type=small&width=20" % self.authToken)

  def id(self):
    return self.__fetch(
        "/me?fields=id&access_token=%s&redirect=false" % self.authToken)

