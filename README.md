# WebHunter

> https://github.com/Buzz2d0/WebHunt WEB API

## Usage
1. 安装 Mysql、redis
2. 注册 Github application.
3. 配置 `.env` [.env-example](./conf/development/.env-example)
4. 安装 [WebHunt](https://github.com/Buzz2d0/WebHunt)
```bash
$ cd thirdparty
$ git clone https://github.com/Buzz2d0/WebHunt
$ pip install -r WebHunt/requirements.txt
$ ./WebHunt/webhunt manage --pull_webanalyzer # 拉取指纹组件到本地
$ ./WebHunt/webhunt manage --sync --host localhost --port 3306 --db WEBHUNTER --user root --passwd [password] # 同步到数据库
```

- web: `flask run`
- celery: `celery -A core.cookcelery.app:application worker --loglevel=info`
