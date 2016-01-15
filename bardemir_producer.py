
from messages import Profile, Ride, RidesCollection, Hitchhike, HitchhikesCollection
from promises import Promise
import json
from messages import STORED_HITCHHIKES, STORED_RIDES, upsert, remove

def nextId():
  LAST_ID = 0
  while True:
    LAST_ID = LAST_ID + 1
    yield str(LAST_ID)

IDS = nextId()

class BardemirProducer:
  def __init__(self, facebook_api):
    self.facebook_api = facebook_api

  def _upsert(self, obj, objs):
    def upsertWithOwner(id):
      if id != obj.owner.id:
         return None

      return performUpsert(obj, objs)

    def upsertWithoutOwner(result):
      obj.owner = result;
      return performUpsert(obj, objs);

    def performUpsert(obj, objs):
      upserter, o = upsert(obj, objs)
      if o and o.owner.id != obj.owner.id:
        return None;

      if not o:
        global IDS
        obj.id = IDS.next()

      upserter()
      return obj

    if obj.owner:
      return self.facebook_api.id().then(upsertWithOwner)
    else:
      return self.getProfile().then(upsertWithoutOwner)

  def upsertRide(self, ride):
    return self._upsert(ride, STORED_RIDES.items)

  def upsertHitchhike(self, hitchhike):
    return self._upsert(hitchhike, STORED_HITCHHIKES.items)

  def _remove(self, id, objs):
    def removeId(session_user_id):
      remover, o = remove(id, objs)
      if not o:
        return None;

      if o.owner.id != session_user_id:
        return None;

      remover()
      return o

    return self.getId().then(removeId)

  def removeRide(self, id):
    return self._remove(id, STORED_RIDES.items)

  def removeHitchhike(self, id):
    return self._remove(id, STORED_HITCHHIKES.items)

  def getId(self):
    return self.facebook_api.id().then(
        lambda response: json.loads(response.content)['id'])


  def getProfile(self):
    def getProfileDone(result):
      profileResponse = json.loads(result[0].content)
      pictureResponse = json.loads(result[1].content)
      return Profile(
          id=profileResponse['id'],
          name=profileResponse['name'],
          photoUrl=pictureResponse['data']['url'])

    return Promise.all([self.facebook_api.me(), self.facebook_api.picture()]
        ).then(getProfileDone)



