from WebConf.nginx import Nginx
from WebConf.uwsgi import Uwsgi


class Public:

    def __init__(self, *args, **kwargs):
        self.nginx = Nginx(*args, **kwargs)
        self.uwsgi = Uwsgi(*args, **kwargs)
