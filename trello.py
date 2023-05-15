import requests, os, sys
from urllib.parse import unquote
import argparse
ATTACHMENT_REQUEST_TIMEOUT = 30  # 30 seconds

# Read the API keys from the environment variables
key = os.getenv('TRELLO_API_KEY', '')
token = os.getenv('TRELLO_TOKEN', '')

# key = r'7298aecff5a0da0a0bd40d1665ec56e9'
# token = r'ATTAcac28ff8d501cd25bd88a028295fd5603b1e409802a78ae33fb582a08d8544ceE45A3437'
# card_id = 'fm5ttZRn'


parser = argparse.ArgumentParser()
parser.add_argument('--card_id',  help='id of card')
args = parser.parse_args()
card_id = args.card_id
url = f"https://api.trello.com/1/cards/{card_id}" + "?attachments=true&attachment_fields=url"

params = {
    "key": key,
    "token": token
}
headers = {
    "Accept": "application/json"
}


def decode_if_url_encoded(string):
    try:
        decoded = unquote(string)
        return decoded
    except:
        return string


response = requests.get(url, headers=headers, params=params)
print(response)
card_data = response.json()

md_content = card_data["desc"]
with open(f"card-{card_id}.md", "w", encoding="utf-8") as f:
    f.write(md_content)

attachments = card_data['attachments']
current_directory = os.getcwd()


attachments_directory = os.path.join(current_directory, f'{card_id}-attachments')
os.makedirs(attachments_directory, exist_ok=True)
os.chdir(attachments_directory)

for attachment in attachments:
    attachment_url = attachment["url"]
    filename = decode_if_url_encoded(attachment_url.split("/")[-1])

    try:
        response = requests.get(attachment_url,
                               stream = True,
                               timeout = ATTACHMENT_REQUEST_TIMEOUT,
                               headers = {"Authorization":"OAuth oauth_consumer_key=\{}\",oauth_token=\"{}\"".format(key,token)})
    except Exception:
        sys.stderr.write('Failed download: {}'.format(filename))
        continue
        
    with open(filename, "wb") as f:
        f.write(response.content)

print("下载完成！")
