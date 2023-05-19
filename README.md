Download Trello card as a markdown file, and download attachments simultaneously.

Both TRELLO_API_KEY and TRELLO_TOKEN are read through environment variables and need to be manually specified.

Please ensure that the environment variables TRELLO_API_KEY and TRELLO_TOKEN are correctly set.

To obtain an API key, please visit: https://trello.com/app-key
To obtain a token, please visit: https://trello.com/1/authorize?scope=read&expiration=never&name=backup&key=REPLACE_WITH_YOUR_API_KEY&response_type=token

The requests package needs to be installed.

To run, specify the card:

```bash
python trello.py -c card_id
```