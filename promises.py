def resolveAfter(promises, r):
  i = 0;
  l = len(promises)
  while True:
    i = i + 1
    if i < l:
      print "yield"
      yield
    else:
      break

  r.resolve([p.result for p in promises])
  yield

class Promise:
  def __init__(self, waitter = lambda: None):
    self.result = None
    self.observers = []
    self.waitter = waitter

  def __addObserver(self, o):
    if self.result:
      o(self.result)
      return
    self.observers.append(o)

  def then(self, f):
    p = Promise(self.waitter)
    self.__addObserver(lambda result: self.__then(result, f, p))
    return p

  def __then(self, result, f, p):
    f_result = f(result)
    if isinstance(f_result, Promise):
      f_result.__addObserver(lambda r: p.resolve(r))
      return
    p.resolve(f_result)

  def resolve(self, result):
    self.result = result
    for o in self.observers:
      o(self.result)

  def result(self):
    return self.result

  def wait(self):
    self.waitter()
    return self

  @staticmethod
  def all(promises):
    r = Promise(lambda: Promise.waitAll(promises))
    f = resolveAfter(promises, r)
    for p in promises:
      p.__addObserver(lambda _: f.next())
    return r

  @staticmethod
  def waitAll(promises):
    for p in promises:
      p.wait()


