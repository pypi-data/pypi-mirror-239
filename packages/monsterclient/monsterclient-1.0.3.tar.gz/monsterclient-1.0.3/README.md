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


##### commands

1. put

```
monster put <container>
monster put <container> <object>
```

2. delete

```
monster delete <container>
monster delete <container> <object>
```

3. get

```
monster get
monster get <container>
monster get <container> <object>
```

4. head

```
monster head
monster head <container>
monster head <container> <object>
```

5. post

```
monster post -kv key:value
monster post <container> -kv key:value
monster post <container> <object> -kv key:value
```

6. info

```
monster info
```

* to see curl command use `-c` or `--curl` option. for example:

```
monster put <container> --curl
```