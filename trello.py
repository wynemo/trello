import requests, os
from urllib.parse import unquote, urlparse
import argparse
from PIL import Image
import io
import hashlib
import re
import sys
ATTACHMENT_REQUEST_TIMEOUT = 30  # 30 seconds
from urllib import  parse
# Read the API keys from the environment variables
key = os.getenv('TRELLO_API_KEY', '')
token = os.getenv('TRELLO_TOKEN', '')
# key = r'7298aecff5a0da0a0bd40d1665ec56e9'
# token = r'ATTAcac28ff8d501cd25bd88a028295fd5603b1e409802a78ae33fb582a08d8544ceE45A3437'
# card_id = 'fm5ttZRn'
parser = argparse.ArgumentParser()
parser.add_argument('--card_id',  help='id of card')
parser.add_argument('--host', help = 'spcify the host')
args = parser.parse_args()
host = args.host
card_id = args.card_id
url = f"https://api.trello.com/1/cards/{card_id}" + "?attachments=true&attachment_fields=url"
current_directory = os.getcwd()
params = {
    "key": key,
    "token": token
}
headers = {
    "Accept": "application/json"
}

def replace_img(markdown_path):
    with open(markdown_path, 'r', encoding='utf-8') as f:
        content = f.read()
    directory,_ = os.path.split(markdown_path)
    # find all image urls in the markdown file
    pattern = r'!\[.*?\]\((.*?)\)'
    for url in re.findall(pattern, content):
        # download the image if it's from a url and replace the url with the path to the downloaded image
        if url.startswith('http'):
            img_path = download_img(url, directory = directory)
            content = content.replace(url, img_path)

    # write the modified content back to the markdown file
    with open(markdown_path, 'w', encoding='utf-8') as f:
        f.write(content)
def download_img(url, directory = None):
    if host:
        url = url.replace(urlparse(url).netloc, host)
    if url.startswith("https://api.trello.com/1/cards"):
        try:
            response = requests.get(attachment_url,
                                    stream=True,
                                    timeout=ATTACHMENT_REQUEST_TIMEOUT,
                                    headers={
                                        "Authorization": "OAuth oauth_consumer_key=\"{}\",oauth_token=\"{}\"".format(
                                            key,
                                            token)})
        except Exception:
            sys.stderr.write('Failed download: {}'.format(url))
    else:
        response = requests.get(url)
    print(response)
    md5_hash = hashlib.md5(response.content)
    md5_digest = md5_hash.hexdigest()
    file_ext = os.path.splitext(url)[-1]
    if not file_ext:
        img = Image.open(io.BytesIO(response.content))
        file_ext = '.' + img.format.lower()
    os.makedirs("images", exist_ok=True)
    img_name = md5_digest + file_ext

    # Create a directory to store the images if it doesn't exist
    if directory:
        img_dir = os.path.join(directory, 'images')
    else:
        img_dir = 'images'
    os.makedirs(img_dir, exist_ok=True)

    # Create the full path to the image file
    img_path = os.path.join(img_dir, img_name)

    # Write the image content to the file
    with open(img_path, 'wb') as f:
        f.write(response.content)
    img_path = os.path.join("images", img_name)
    # Return the path to the downloaded image file
    return img_path
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
attachments_directory = os.path.join(current_directory, f'{card_id}-attachments')
os.makedirs(attachments_directory, exist_ok=True)
os.chdir(attachments_directory)

for attachment in attachments:
    attachment_url = attachment["url"]
    filename = decode_if_url_encoded(attachment_url.split("/")[-1])

    try:
        response = requests.get(attachment_url,
                                stream=True,
                                timeout=ATTACHMENT_REQUEST_TIMEOUT,
                                headers={
                                    "Authorization": "OAuth oauth_consumer_key=\"{}\",oauth_token=\"{}\"".format(key,
                                                                                                                 token)})
    except Exception:
        sys.stderr.write('Failed download: {}'.format(filename))
        continue
    with open(filename, "wb") as f:
        f.write(response.content)


for root, dirs, files in os.walk(current_directory):
    for f in files:
        if f.endswith('.md'):
            mdfile_path = os.path.relpath(os.path.join(root,f), os.getcwd())
            replace_img(mdfile_path)
print("下载完成！")