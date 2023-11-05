import os
import pickle
import curlify
import requests
from urllib.parse import urlparse


def convert_to_curl(curl_command):
    unwanted_headers = [
        "-H 'Accept: */*'",
        "-H 'Accept-Encoding: gzip, deflate'",
        "-H 'Connection: keep-alive'",
        "-H 'Content-Length: 0'",
        "-H 'User-Agent: python-requests/2.31.0'",
    ]
    for header in unwanted_headers:
        curl_command = curl_command.replace(header, "")
    curl_parts = curl_command.split()
    curl_parts.insert(1, "-v")
    return " ".join(curl_parts)


def get_token():
    try:
        with open("token.pkl", "rb") as data:
            token = pickle.load(file=data)
            return token
    except:
        print("first run this command: monster token")    


def set_token():
    url = os.getenv("ST_AUTH", "http://127.0.0.1:8080/auth/v1.0")
    username = os.getenv("ST_USER", "test:tester")
    password = os.getenv("ST_KEY", "testing")
    heads = {"X-Storage-User": username, "X-Storage-Pass": password}
    response = requests.get(url=url, headers=heads)
    token = response.headers["X-Auth-Token"]
    with open("token.pkl", "wb") as data:
        pickle.dump(file=data, obj=token)
    return token


def create_container(container_name):
    url = os.getenv("ST_URL", "http://127.0.0.1:8080/v1/AUTH_test")
    headers = {"X-Auth-Token": get_token()}
    response = requests.put(f"{url}/{container_name}", headers=headers)
    curl = curlify.to_curl(response.request)
    modified_curl = convert_to_curl(curl)
    return response.status_code, modified_curl


def upload_object(container_name, object_name):
    url = os.getenv("ST_URL", "http://127.0.0.1:8080/v1/AUTH_test")
    headers = {"X-Auth-Token": get_token()}
    with open(object_name, "rb") as f:
        data = f.read()
    response = requests.put(
        f"{url}/{container_name}/{object_name}", headers=headers, data=data
    )
    curl = curlify.to_curl(response.request)
    modified_curl = convert_to_curl(curl)
    return response.status_code, modified_curl


def delete_container(container_name):
    url = os.getenv("ST_URL", "http://127.0.0.1:8080/v1/AUTH_test")
    headers = {"X-Auth-Token": get_token()}
    response = requests.delete(f"{url}/{container_name}", headers=headers)
    curl = curlify.to_curl(response.request)
    modified_curl = convert_to_curl(curl)
    return response.status_code, modified_curl


def delete_object(container_name, object_name):
    url = os.getenv("ST_URL", "http://127.0.0.1:8080/v1/AUTH_test")
    headers = {"X-Auth-Token": get_token()}
    response = requests.delete(f"{url}/{container_name}/{object_name}", headers=headers)
    curl = curlify.to_curl(response.request)
    modified_curl = convert_to_curl(curl)
    return response.status_code, modified_curl


def head_account():
    url = os.getenv("ST_URL", "http://127.0.0.1:8080/v1/AUTH_test")
    headers = {"X-Auth-Token": get_token()}
    response = requests.head(f"{url}", headers=headers)
    curl = curlify.to_curl(response.request)
    modified_curl = convert_to_curl(curl)
    return response.headers, modified_curl


def head_container(container_name):
    url = os.getenv("ST_URL", "http://127.0.0.1:8080/v1/AUTH_test")
    headers = {"X-Auth-Token": get_token()}
    response = requests.head(f"{url}/{container_name}", headers=headers)
    curl = curlify.to_curl(response.request)
    modified_curl = convert_to_curl(curl)
    return response.headers, modified_curl


def head_object(container_name, object_name):
    url = os.getenv("ST_URL", "http://127.0.0.1:8080/v1/AUTH_test")
    headers = {"X-Auth-Token": get_token()}
    response = requests.head(f"{url}/{container_name}/{object_name}", headers=headers)
    curl = curlify.to_curl(response.request)
    modified_curl = convert_to_curl(curl)
    return response.headers, modified_curl


def get_account():
    url = os.getenv("ST_URL", "http://127.0.0.1:8080/v1/AUTH_test")
    headers = {"X-Auth-Token": get_token()}
    response = requests.get(f"{url}", headers=headers)
    curl = curlify.to_curl(response.request)
    modified_curl = convert_to_curl(curl)
    return response.content.decode(), modified_curl


def get_container(container_name):
    url = os.getenv("ST_URL", "http://127.0.0.1:8080/v1/AUTH_test")
    headers = {"X-Auth-Token": get_token()}
    response = requests.get(f"{url}/{container_name}", headers=headers)
    curl = curlify.to_curl(response.request)
    modified_curl = convert_to_curl(curl)
    return response.content.decode(), modified_curl


def get_object(container_name, object_name):
    url = os.getenv("ST_URL", "http://127.0.0.1:8080/v1/AUTH_test")
    headers = {"X-Auth-Token": get_token()}
    response = requests.get(f"{url}/{container_name}/{object_name}", headers=headers)
    curl = curlify.to_curl(response.request)
    modified_curl = convert_to_curl(curl)
    with open(f"{object_name}", "wb") as data:
        data.write(response.content)
    return response.status_code, modified_curl


def get_info():
    url = os.getenv("ST_URL", "http://127.0.0.1:8080/v1/AUTH_test")
    parsed_url = urlparse(url)
    base_url = parsed_url.scheme + "://" + parsed_url.netloc
    response = requests.get(f"{base_url}/info")
    curl = curlify.to_curl(response.request)
    modified_curl = convert_to_curl(curl)
    return response.content.decode(), modified_curl
