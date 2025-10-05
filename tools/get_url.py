import requests

def get_url(url):
    response = requests.get(url)
    return dict({
        "status_code": response.status_code,
        "headers": dict(response.headers),
        "content": response.text,
    })