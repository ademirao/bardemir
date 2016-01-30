from protorpc import messages

class Profile(messages.Message):
  id = messages.StringField(1)
  name = messages.StringField(2)
  photoUrl = messages.StringField(3)

class Ride(messages.Message):
  id = messages.StringField(1)
  owner = messages.MessageField(Profile, 2)
  directions = messages.StringField(3)
  time = messages.StringField(4)

class RidesCollection(messages.Message):
  """Collection of Rides"""
  items = messages.MessageField(Ride, 1, repeated=True)

STORED_RIDES = RidesCollection(items=[]);

class Hitchhike(messages.Message):
  id = messages.StringField(1)
  owner = messages.MessageField(Profile, 2)
  position = messages.StringField(3)

class HitchhikesCollection(messages.Message):
  """Collection of Hitchhikes."""
  items = messages.MessageField(Hitchhike, 1, repeated=True)

STORED_HITCHHIKES = HitchhikesCollection(items=[])

class Event(messages.Message):
  name = messages.StringField(1)
  time = messages.StringField(2)

def upsert(obj, items):
  for i, item in enumerate(items):
    if (obj.id == item.id):
      def replacer():
        items[i] = obj

      return replacer, items[i] 

  def appender():
    items.append(obj)

  return appender, None


def remove(id, items):
  for i, item in enumerate(items):
    if (id == item.id):
      def remover():
        del items[i]

      return remover, items[i] 

  return lambda: None, None

