"""
常量
"""
nginx_error_list = ['nginx: command not found']

class NginxConf:
    NGINX = 'nginx'
    NGINX_OTHER = 'conf.d'
    NGINX_HOST = '127.0.0.1'
    NGINX_PORT = '80'

    CHOICES = (
        (NGINX, 'nginx'),
        (NGINX_OTHER, '其他配置'),
        (NGINX_HOST, 'ip地址'),
        (NGINX_PORT, '端口'),

    )


class UwsgiConf:
    UWSGI = 'uwsgi'
    UWSGI_HOST = '127.0.0.1'
    UWSGI_PORT = '8000'

    CHOICES = (
        (UWSGI, 'uwsgi'),
        (UWSGI_HOST, 'ip地址'),
        (UWSGI_PORT, '端口'),

    )


class ProjectConf:
    LOGS = 'logs'
    STATIC = 'static'

    CHOICES = (
        (LOGS, 'logs'),
        (STATIC, 'static'),
    )
