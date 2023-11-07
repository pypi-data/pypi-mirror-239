from WebConf.base_setting import BaseSetting


class Nginx(BaseSetting):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def gen_nginx(self):
        assert self.folder_exists(self.args.uwsgi_path), '生成uwsgi才可以生成nginx配置'
        assert self.args.nginx_host, "请设置nginx域名"
        nginx_file_path = self.nginx_conf_file
        nginx_file_path.write_text(f"""
server{{
  listen {self.args.uwsgi_port};
  server_name {self.args.nginx_host};
  access_log {self.logs_path}/nginx-access.log;
  error_log {self.logs_path}/nginx-error.log;
  location /static/ {{
    alias {self.static_path}/;
  }}

  location / {{
    if ($request_method ~* HEAD)
    {{
      return 200;
    }}
    include uwsgi_params;
    uwsgi_connect_timeout   10;
    uwsgi_send_timeout      600;
    uwsgi_read_timeout      600;
    uwsgi_pass 127.0.0.1:{self.args.uwsgi_port};
  }}
}}
""", encoding='utf8')
        return nginx_file_path
