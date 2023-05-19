下载trello card为markdown文件，同时下载附件

TRELLO_API_KEY 与 TRELLO_TOKEN 均通过环境变量读取，需要手动指定

请确保环境变量 TRELLO_API_KEY 和 TRELLO_TOKEN 已经正确设置。

获取 API key，请访问：https://trello.com/app-key
获取 token，请访问：https://trello.com/1/authorize?scope=read&expiration=never&name=backup&key=REPLACE_WITH_YOUR_API_KEY&response_type=token

运行时指定card:

```bash
python trello.py -c card_id
```

