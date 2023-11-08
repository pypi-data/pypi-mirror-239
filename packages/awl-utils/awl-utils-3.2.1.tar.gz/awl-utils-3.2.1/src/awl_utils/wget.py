
import requests

def wget(url):
    r = requests.get(url, allow_redirects=True)
    return r.content.decode('utf-8')
