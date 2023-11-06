import os
import pickle
import curlify
import requests
from urllib.parse import urlparse
from dataclasses import dataclass
import json


class Authentication:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self) -> None:
        self.auth_endpoint = os.getenv("ST_AUTH", "http://127.0.0.1:8080/auth/v1.0")
        self.url_endpoint = os.getenv("ST_URL", "http://127.0.0.1:8080/v1/AUTH_test")
        self.username = os.getenv("ST_USER", "test:tester")
        self.password = os.getenv("ST_KEY", "testing")


class Token:
    def __init__(self) -> None:
        self.auth = Authentication()
        self.read_token()

    def read_token(self):
        try:
            with open("/tmp/token.pkl", "rb") as data:
                self.value = pickle.load(file=data)
        except:
            self.value = None

    def write_token(self):
        url = self.auth.auth_endpoint
        username = self.auth.username
        password = self.auth.password

        heads = {"X-Storage-User": username, "X-Storage-Pass": password}
        response = requests.get(url=url, headers=heads)
        self.value = response.headers["X-Auth-Token"]
        with open("/tmp/token.pkl", "wb") as data:
            pickle.dump(file=data, obj=self.value)
        modified_curl = convert_to_curl(response.request)
        return Response(
            status_code=response.status_code,
            token=self.value,
            curl=modified_curl,
        )


def convert_to_curl(curl_command):
    unwanted_headers = [
        "-H 'Accept: */*'",
        "-H 'Accept-Encoding: gzip, deflate'",
        "-H 'Connection: keep-alive'",
        "-H 'Content-Length: 0'",
        "-H 'User-Agent: python-requests/2.31.0'",
    ]

    curl = curlify.to_curl(curl_command)

    for header in unwanted_headers:
        curl = curl.replace(header, "")
    curl_parts = curl.split()
    curl_parts.insert(1, "-v")
    return " ".join(curl_parts)


class Response:
    def __init__(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)

    def repr(self, **kwargs):
        ans = ""
        for key, value in vars(self).items():
            if key in kwargs and kwargs[key] == False:
                continue
            elif value is not None:
                ans += self.prettify(value) + "\n\n"

        return ans

    def prettify(self, inp):
        res = str(inp).replace("'", '"')
        try:
            data = json.loads(res)
            return json.dumps(data, indent=4)
        except:
            return res


class MonsterAPI:
    def __init__(self) -> None:
        self.token = Token()
        self.headers = {"X-Auth-Token": self.token.value}
        self.auth = Authentication()

    # Create
    def create_container(self, container_name):
        url = self.auth.url_endpoint
        response = requests.put(f"{url}/{container_name}", headers=self.headers)
        modified_curl = convert_to_curl(response.request)

        return Response(
            status_code=response.status_code,
            content=response.content.decode(),
            curl=modified_curl,
        )

    def upload_object(self, container_name, object_name):
        url = self.auth.url_endpoint

        with open(object_name, "rb") as f:
            data = f.read()
        response = requests.put(
            f"{url}/{container_name}/{object_name}", headers=self.headers, data=data
        )
        modified_curl = convert_to_curl(response.request)
        return Response(
            status_code=response.status_code,
            content=response.content.decode(),
            curl=modified_curl,
        )

    # Delete
    def delete_container(self, container_name):
        url = self.auth.url_endpoint
        response = requests.delete(f"{url}/{container_name}", headers=self.headers)
        modified_curl = convert_to_curl(response.request)
        return Response(
            status_code=response.status_code,
            content=response.content.decode(),
            curl=modified_curl,
        )

    def delete_object(self, container_name, object_name):
        url = self.auth.url_endpoint

        response = requests.delete(
            f"{url}/{container_name}/{object_name}", headers=self.headers
        )
        modified_curl = convert_to_curl(response.request)
        return Response(
            status_code=response.status_code,
            content=response.content.decode(),
            curl=modified_curl,
        )

    # Head
    def head_account(self):
        url = self.auth.url_endpoint

        response = requests.head(f"{url}", headers=self.headers)
        modified_curl = convert_to_curl(response.request)
        return Response(
            status_code=response.status_code,
            headers=response.headers,
            curl=modified_curl,
        )

    def head_container(self, container_name):
        url = self.auth.url_endpoint

        response = requests.head(f"{url}/{container_name}", headers=self.headers)
        modified_curl = convert_to_curl(response.request)
        return Response(
            status_code=response.status_code,
            headers=response.headers,
            curl=modified_curl,
        )

    def head_object(self, container_name, object_name):
        url = self.auth.url_endpoint

        response = requests.head(
            f"{url}/{container_name}/{object_name}", headers=self.headers
        )
        modified_curl = convert_to_curl(response.request)
        return Response(
            status_code=response.status_code,
            headers=response.headers,
            curl=modified_curl,
        )

    # Get
    def get_account(self):
        url = self.auth.url_endpoint

        response = requests.get(f"{url}", headers=self.headers)
        modified_curl = convert_to_curl(response.request)
        return Response(
            status_code=response.status_code,
            content=response.content.decode(),
            curl=modified_curl,
        )

    def get_container(self, container_name):
        url = self.auth.url_endpoint

        response = requests.get(f"{url}/{container_name}", headers=self.headers)
        modified_curl = convert_to_curl(response.request)
        return Response(
            status_code=response.status_code,
            content=response.content.decode(),
            curl=modified_curl,
        )

    def get_object(self, container_name, object_name):
        url = self.auth.url_endpoint

        response = requests.get(
            f"{url}/{container_name}/{object_name}", headers=self.headers
        )
        modified_curl = convert_to_curl(response.request)
        with open(f"{object_name}", "wb") as data:
            data.write(response.content)

        try:
            return Response(
                status_code=response.status_code,
                content=response.content.decode(),
                curl=modified_curl,
            )
        except:
            return Response(
                status_code=response.status_code,
                curl=modified_curl,
            )

    # Metadata
    def post_account(self, kv):
        key, value = kv.split(":")[0], kv.split(":")[1]
        url = self.auth.url_endpoint
        headers = self.headers
        headers |= {f"X-Account-Meta-{key}": f"{value}"}

        response = requests.post(f"{url}", headers=headers)
        modified_curl = convert_to_curl(response.request)

        return Response(
            status_code=response.status_code,
            content=response.content.decode(),
            curl=modified_curl,
        )

    def post_container(self, container_name, kv):
        key, value = kv.split(":")[0], kv.split(":")[1]
        url = self.auth.url_endpoint
        headers = self.headers
        headers |= {f"X-Container-Meta-{key}": f"{value}"}

        response = requests.post(f"{url}/{container_name}", headers=headers)
        modified_curl = convert_to_curl(response.request)
        return Response(
            status_code=response.status_code,
            content=response.content.decode(),
            curl=modified_curl,
        )

    def post_object(self, container_name, object_name, kv):
        key, value = kv.split(":")[0], kv.split(":")[1]
        url = self.auth.url_endpoint
        headers = self.headers
        headers |= {f"X-Object-Meta-{key}": f"{value}"}

        response = requests.post(
            f"{url}/{container_name}/{object_name}", headers=headers
        )
        modified_curl = convert_to_curl(response.request)
        return Response(
            status_code=response.status_code,
            content=response.content.decode(),
            curl=modified_curl,
        )

    # Info
    def get_info(self):
        url = self.auth.url_endpoint

        parsed_url = urlparse(url)
        base_url = parsed_url.scheme + "://" + parsed_url.netloc
        response = requests.get(f"{base_url}/info")
        modified_curl = convert_to_curl(response.request)
        return Response(
            status_code=response.status_code,
            content=response.content.decode(),
            curl=modified_curl,
        )
