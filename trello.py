import argparse
import os
import sys
from urllib.parse import unquote, urlparse

import requests

ATTACHMENT_REQUEST_TIMEOUT = 30  # 30 seconds

# Read the API keys from the environment variables
key = os.getenv("TRELLO_API_KEY", "")
token = os.getenv("TRELLO_TOKEN", "")

parser = argparse.ArgumentParser()
parser.add_argument("--card", "-c", help="card")
args = parser.parse_args()
card: str = args.card
if card.startswith("http"):
    card_id = urlparse(card).path.lstrip("/").split("/")[1]
else:
    card_id = card
print(f"card_id is {card_id}")
url = (
    f"https://api.trello.com/1/cards/{card_id}"
    + "?attachments=true&attachment_fields=url"
)

params = {"key": key, "token": token}
headers = {"Accept": "application/json"}


def decode_if_url_encoded(string):
    try:
        decoded = unquote(string)
        return decoded
    except:
        return string


response = requests.get(url, headers=headers, params=params)
card_data = response.json()

md_content = card_data["desc"]
card_name = card_data["name"]

attachments = card_data["attachments"]

for attachment in attachments:
    attachment_url = attachment["url"]
    attachment_id = attachment["id"]
    filename = decode_if_url_encoded(attachment_url.split("/")[-1])
    folder_name = f"attachments_{card_id}/{attachment_id}"
    os.makedirs(folder_name, exist_ok=True)

    try:
        response = requests.get(
            attachment_url,
            stream=True,
            timeout=ATTACHMENT_REQUEST_TIMEOUT,
            headers={
                "Authorization": 'OAuth oauth_consumer_key="{}",oauth_token="{}"'.format(
                    key, token
                )
            },
        )
    except Exception:
        sys.stderr.write("Failed download: {}".format(filename))
        continue

    filepath = os.path.join(folder_name, filename)
    md_content = md_content.replace(attachment_url, filepath)

    with open(filepath, "wb") as f:
        f.write(response.content)

with open(f"{card_name}.md", "w", encoding="utf-8") as f:
    f.write(md_content)
print(f"下载完成！{card_name}.md")
