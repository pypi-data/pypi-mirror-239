from httpx import get

def cli():
    url = "https://httpbin.org/get?arg=Live%20de%20Python"
    content = get(url=url
                  ).json()
    print(content['args']['arg'])
