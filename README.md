# WebHunter

> https://github.com/WebHunt-Kits/WebHunt WEB API

## dev

[.env-example](./conf/development/.env-example)

- web: `flask run`
- celery: `celery -A core.cookcelery.app:application worker --loglevel=info`
