from WebConf.base_setting import BaseSetting


class Uwsgi(BaseSetting):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def gen_uwsgi(self):
        assert self.args.uwsgi_port != 0, "请设置uwsgi端口"
        if self.args.conf_dir:
            uwsgi_file = self.path_lib(self.args.service_dir) / self.args.conf_dir / "uwsgi.ini"
            service_dir = self.path_lib(self.args.service_dir) / self.args.conf_dir
        else:
            uwsgi_file = self.path_lib(self.args.service_dir) / "uwsgi.ini"
            service_dir = self.args.service_dir
        uwsgi_file.write_text(f"""
[uwsgi]
uwsgi-socket=:{self.args.nginx_port}
env = IS_DEBUG=0
chdir={self.service_path}
module={self.args.service_name}.wsgi:application
master=True
processes=16
harakiri=1800
pidfile={service_dir}/uwsgi.pid
vacuum=True
max-requests=10000
max-requests-delta=100
#enable-threads=True
virtualenv = {self.virtualenv_path}
daemonize={self.logs_path}/uwsgi.log
log-maxsize=104857600
reload-on-rss=240
reload-mercy=180
max-worker-lifetime=3600
post-buffering=262144
post-buffering-bufsize=262144
#gevent=1000
stats={service_dir}/uwsgi_stat.sock
""", encoding='utf8')
        return uwsgi_file
