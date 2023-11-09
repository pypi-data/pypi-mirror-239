import requests
import time


class APIError(Exception):
    pass


class API:
    _obj = None  # Warning: use on own risk

    def __init__(self, url, user, password, version=2, retries=0,
                 ssl_verify=False, retry_timeout=1) -> None:
        self.url = url
        self.vstr = f'/api/v{version}'
        self.session = requests.Session()
        self.session.auth = (user, password)
        self.session.verify = ssl_verify
        self.timeout = retry_timeout
        self.retries = retries
        API._obj = self

    def request(self, method, path, json=None, retries=3, parse=True):
        if retries is None:
            retries = self.retries
        if not path.startswith('/') and not path.startswith('https://'):
            path = '/' + path
        if not path.startswith(self.vstr) and not path.startswith('https://'):
            path = self.vstr + path
        if not path.startswith('https://'):
            path = self.url + path
        response = self.session.request(method, path, json=json)
        if response.status_code >= 500 and retries > 0:
            # retry on server error
            time.sleep(self.timeout)
            return self.request(method, path, json, retries - 1, parse)
        if not 200 <= response.status_code < 300:
            raise APIError(path, response.text)
        return response.json() if parse else response

    def load(self, path):
        p = path
        while p:
            resp = self.request('GET', p)
            p = resp.get('next')
            for i in resp['results']:
                yield i


class APIObject:
    _router = {}
    _related = {}
    _sub = {}
    _on_demand = {}
    _actions = []
    _path = None
    _map = {}
    _cache = {}
    _display = 'name'

    def __init_subclass__(cls) -> None:
        cls._cache = {}
        if getattr(cls, '_path'):
            APIObject._router[cls._path.strip('/')] = cls

    def __init__(self, data, api) -> None:
        self._data = data
        self.api = api
        self._cache[data['id']] = self

    def _reload(self):
        del self._cache[self._data['id']]
        self._data = self.load(self._data['id'], self.api)._data

    def delete(self):
        # Invalidates object
        self.api.request('DELETE', self._path +
                         str(self._data['id']) + '/', parse=False)

    def get_sub(self, path, obj_type):
        for obj in self.api.load(self._path + f'{self.id}/{path}/'):
            yield obj_type(obj, self.api)

    def _action(self, action, method="POST"):
        def foo(**kwargs):
            self.api.request(method, self._path +
                             f'{self.id}/{action}/', kwargs)
        return foo

    def __on_demand(self, path):
        return self.api.request("GET", self.url + path, parse=False).text

    def __getattribute__(self, __name: str):
        if __name.startswith('_'):
            return super().__getattribute__(__name)
        if __name in self._sub:
            return self.get_sub(__name, self._sub[__name])
        if __name in self._related:
            return self._related[__name](self, __name)
        if __name in self._on_demand:
            return self.__on_demand(self._on_demand[__name])
        if __name in self._actions:
            return self._action(__name)
        if __name in self._map:
            return self._map[__name](self._data[__name])
        if __name in self._data:
            return self._data[__name]
        return super().__getattribute__(__name)

    @classmethod
    def find(cls, query, order_by=None, api=None):
        url = cls._path + '?search=' + query
        if order_by:
            url += '&order_by=' + ','.join(order_by)
        if not api:
            api = API._obj
        yield from map(lambda x: cls(x, api), api.load(url))

    @classmethod
    def find_first(cls, query, order_by=None, api=None):
        for i in cls.find(query, order_by, api):
            return i
        return None

    @classmethod
    def load(cls, oid, api=None):
        if oid in cls._cache:
            return cls._cache[oid]
        if not api:
            api = API._obj
        return cls(api.request('GET', cls._path + f'{oid}/'), api)

    @classmethod
    def load_url(cls, url, api=None):
        if not api:
            api = API._obj
        otp, oid = url.strip('/').replace('api/v2/', '').split('/')
        if otp not in cls._router:
            raise Exception(f'Undefined endpoint {otp}')
        return cls._router[otp].load(oid, api)

    @property
    def name(self):
        return self._data.get(self._display, None)

    def __repr__(self) -> str:
        name = self._data.get(self._display, '-')
        return f'<{type(self).__name__} {name} {self.id}>'


class Related:
    def __init__(self, obj_type, *key, iterable=False,
                 prefix=None, allow_none=True) -> None:
        self.key = key
        self.obj = obj_type
        self.iterable = iterable
        self.prefix = prefix
        self.none = allow_none

    def __get_attr(self, key, obj):
        if not key:
            return obj
        head, *key = key
        return self.__get_attr(key, obj[head])

    def __iter(self, obj, path):
        for i in obj.api.load(path):
            yield self.obj(i, obj.api)

    def __call__(self, obj, k):
        key = self.key
        if not key:
            key = [k]
        path = str(self.__get_attr(key, obj._data))
        if self.none and path is None:
            return
        if self.prefix:
            path = self.prefix + path
        if not self.iterable:
            return self.obj(
                obj.api.request('GET',
                                path
                                ),
                obj.api
            )
        return self.__iter(obj, path)
