import argparse
from pathlib import Path
import os
from WebConf.utils import str2bool
from WebConf import const
from WebConf.utils import execute_command
from WebConf.error import MyNginxException


class BaseSetting(object):

    def __init__(self, *args, **kwargs):
        self.parser = argparse.ArgumentParser()
        # uwsgi配置
        conf_dir = ""
        self.parser.add_argument("--uwsgi_port", type=int, default=const.UwsgiConf.UWSGI_PORT, help="uwsgi端口号")
        self.parser.add_argument("--nginx_port", type=int, default=const.NginxConf.NGINX_PORT, help="nginx端口号")

        self.parser.add_argument("--service_dir", type=str, default=kwargs.get('service_dir'), help="项目目录")
        self.parser.add_argument("--conf_dir", type=str, default=kwargs.get('conf_dir'), help="项目配置目录")
        self.parser.add_argument("--virtualenv_dir", type=str, default=kwargs.get('virtualenv_dir'),
                                 help="虚拟环境配置目录")
        self.parser.add_argument("--logs_dir", type=str, default=const.ProjectConf.LOGS, help="日志目录")
        self.parser.add_argument("-u", "--gen_uwsgi", type=str2bool, default=True, help="生成uwsgi")

        # nginx配置
        service_name = self.get_service_name(kwargs.get('service_dir'))
        uwsgi_path = self.get_uwsgi_path(kwargs.get('service_dir'), kwargs.get('uwsgi_path'))
        self.parser.add_argument("--nginx_host", type=str, help="nginx域名",
                                 default=const.NginxConf.NGINX_HOST)
        self.parser.add_argument("--nginx_conf_dir", type=str, default=self.nginx_exists(),
                                 help="nginx配置目录")
        self.parser.add_argument("--service_name", type=str, default=service_name,
                                 help="nginx配置文件名称/项目名称")
        self.parser.add_argument("--uwsgi_path", type=str, default=uwsgi_path,
                                 help="uwsgi.ini文件路径")
        self.parser.add_argument("--static_dir", type=str, default=const.ProjectConf.STATIC, help="静态文件目录")

        self.args = self.parser.parse_args()

    def base_path(self, path):
        return Path(path)

    def path_lib(self, path):
        return Path(path)

    @property
    def service_path(self):
        return self.base_path(self.args.service_dir)

    @property
    def logs_path(self, add_logs_name=True):
        assert self.args.logs_dir
        logs_path = self.base_path(self.args.service_dir)
        if add_logs_name:
            logs_path /= self.args.logs_dir
        logs_path.mkdir(parents=True, exist_ok=True)
        return logs_path

    @property
    def static_path(self):
        assert self.args.static_dir
        path = self.base_path(self.args.service_dir)
        path /= self.args.static_dir
        path.mkdir(parents=True, exist_ok=True)
        return path

    def folder_exists(self, folder_path):
        if os.path.exists(folder_path):
            return True
        else:
            return False

    @property
    def virtualenv_path(self):
        flag = self.folder_exists(self.args.virtualenv_dir)
        if flag:
            return self.args.virtualenv_dir
        else:
            raise "虚拟环境不存在"

    def traverse_nginx_directory(self, directory, folder):
        for _, dirs, _ in os.walk(directory):
            if folder in dirs:
                nginx_conf_path = self.base_path(directory) / folder
                return nginx_conf_path
            else:
                nginx_conf_path = self.base_path(directory) / folder
                nginx_conf_path.mkdir(parents=True, exist_ok=True)
                return nginx_conf_path

    @property
    def nginx_conf_file(self):
        path = self.traverse_nginx_directory(self.args.nginx_conf_dir, const.NginxConf.NGINX_OTHER)
        return path / f"{self.args.service_name}.conf"

    def nginx_exists(self):
        _, result, _ = execute_command(f"{const.NginxConf.NGINX} -t")
        if result in const.nginx_error_list:
            raise MyNginxException(result)
        result = result.split('nginx: configuration file ')[-1].split('/nginx.conf')[0]
        return result


    def get_uwsgi_path(self, service_dir, uwsgi_path):
        return f"{service_dir}/{uwsgi_path}"

    def get_service_name(self, service_dir):
        return service_dir.split('/')[-1]
