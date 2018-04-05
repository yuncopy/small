

- 模板资源地址 [模板](https://github.com/iogbole/gentelella_on_rails)
- 安装 pip安装gunicorn，pip3 install gunicorn
- 启动 gunicorn -w 4 -b 0.0.0.0:9008 runweb:app
- 打包组件 pip3 freeze > requirements.txt
- pkill gunicorn
- nginx http代理
```
server {
    listen 9008;

    server_name _;
    access_log  /var/log/nginx/access_9008.log;
    error_log  /var/log/nginx/error_9008.log;

    location / {
        proxy_pass         http://127.0.0.1:9008/;
        proxy_redirect     off;

        proxy_set_header   Host             $host;
        proxy_set_header   X-Real-IP        $remote_addr;
        proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;
    }
}
```
