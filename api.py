"""Bardemir World API implemented using Google Cloud Endpoints.

Defined here are the ProtoRPC messages needed to define Schemas for methods
as well as those methods defined in an API.
"""

import pprint
import endpoints
import json
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

class Post(messages.Message):
    """Greeting that stores a message."""
    title = messages.StringField(1)
    content = messages.StringField(2)
    link = messages.StringField(3)


class PostsCollection(messages.Message):
    """Collection of Posts."""
    items = messages.MessageField(Post, 1, repeated=True)

STORED_EVENTS = PostsCollection(items=[
    Post(title='Post 1'),
    Post(title='Post 2'),
])

# url = "http://www.facebook.com/dialog/oauth?client_id=433202543531394&redirect_url=http://bardemir-api.appspot.com"
#	result = urlfetch.fetch(url)
#post = Post()
#	post.description = result.content

@endpoints.api(name='bardemir', version='v1',
               allowed_client_ids=[WEB_CLIENT_ID, ANDROID_CLIENT_ID,
                                   IOS_CLIENT_ID],
               audiences=[ANDROID_AUDIENCE])
class BardemirService(remote.Service):
    """Bardemir API v1."""

    AUTH_RESOURCE = endpoints.ResourceContainer(
            message_types.VoidMessage,
            auth=messages.StringField(1))

    @endpoints.method(AUTH_RESOURCE, PostsCollection,
                      path='listPosts', http_method='POST',
                      name='posts.list')
    def list(self, request):
      bardemir_properties = Properties()
      if not bardemir_properties or not bardemir_properties.group_id:
        post = Post()
        post.description = "No bardemir properties"
        return post
        
      group_id = bardemir_properties.group_id
      url = "https://graph.facebook.com/v2.5/%s/feed?access_token=%s" % (group_id, request.auth)
      result = urlfetch.fetch(url)
      response = json.loads(result.content)
      posts = []

      for e in response['data']:
        if 'message' not in e:
          continue
        post = Post()
        post.title = e['message'].encode('ascii', 'ignore')  
        PPRINTER.pprint(post)
        posts.append(post)

      return PostsCollection(items=posts)

    ID_RESOURCE = endpoints.ResourceContainer(
            message_types.VoidMessage,
            id=messages.IntegerField(1, variant=messages.Variant.INT32))

    @endpoints.method(ID_RESOURCE, Post,
                      path='post/{id}', http_method='GET',
                      name='posts.getPost')
    def getPost(self, request):
        try:
            return STORED_EVENTS.items[request.id]
        except (IndexError, TypeError):
            raise endpoints.NotFoundException('Post %s not found.' %
                                              (request.id,))


APPLICATION = endpoints.api_server([BardemirService])
