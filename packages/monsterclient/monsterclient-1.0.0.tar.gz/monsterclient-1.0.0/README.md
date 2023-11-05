#### how to build?

1. create venv

`python3 -m venv <venv>`

2. build

```
source <venv>/bin/activate

python -m build
```

#### how to use?

set this variables in .bashrc:

```
export ST_AUTH=http://<monster_proxy_ip>:8080/auth/v1.0
export ST_USER=test:tester
export ST_KEY=testing
export ST_URL=http://<monster_proxy_ip>:8080/v1/AUTH_test

```

`pip install dist/monstercli-1.0.0-py3-none-any.whl`

enjoy :)
