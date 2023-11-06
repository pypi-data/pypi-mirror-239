import click
from monsterclient import api

monsterAPI = api.MonsterAPI()
@click.command(help="GET a new token")
@click.option("-c", "--curl", is_flag=True, help="print curl command if specified")
def token(curl):
    response = monsterAPI.token.write_token()
    click.echo(f"{response.repr(curl=curl)}")


@click.command(help="PUT container | object")
@click.argument("container")
@click.argument("obj", required=False)
@click.option("-c", "--curl", is_flag=True, help="print curl command if specified")
def put(container, obj, curl):
    if obj:
        response = monsterAPI.upload_object(container, obj)
    else:
        response = monsterAPI.create_container(container)

    click.echo(f"{response.repr(curl=curl)}")


@click.command(help="DELETE container | object")
@click.argument("container")
@click.argument("obj", required=False)
@click.option("-c", "--curl", is_flag=True, help="print curl command if specified")
def delete(container, obj, curl):
    if obj:
        response = monsterAPI.delete_object(container, obj)
    else:
        response= monsterAPI.delete_container(container)

    click.echo(f"{response.repr(curl=curl)}")


@click.command(help="HEAD container | object | account")
@click.argument("container", required=False)
@click.argument("obj", required=False)
@click.option("-c", "--curl", is_flag=True, help="print curl command if specified")
def head(container, obj, curl):
    if obj and container:
        response = monsterAPI.head_object(container, obj)
    elif not obj and container:
        response = monsterAPI.head_container(container)
    else:
        response = monsterAPI.head_account()

    click.echo(f"{response.repr(curl=curl)}")


@click.command(help="GET container | object | account")
@click.argument("container", required=False)
@click.argument("obj", required=False)
@click.option("-c", "--curl", is_flag=True, help="print curl command if specified")
def get(container, obj, curl):
    if obj and container:
        response = monsterAPI.get_object(container, obj)
    elif not obj and container:
        response = monsterAPI.get_container(container)
    else:
        response = monsterAPI.get_account()

    click.echo(f"{response.repr(curl=curl)}")


@click.command(help="POST container | object | account")
@click.argument("container", required=False)
@click.argument("obj", required=False)
@click.option("-m", "--meta", help="key:value")
@click.option("-c", "--curl", is_flag=True, help="print curl command if specified")
def post(container, obj, meta, curl):
    if obj and container:
        response= monsterAPI.post_object(container, obj, meta)
    elif not obj and container:
        response = monsterAPI.post_container(container, meta)
    else:
        response = monsterAPI.post_account(meta)

    click.echo(f"{response.repr(curl=curl)}")


@click.command(help="Get info")
@click.option("-c", "--curl", is_flag=True, help="print curl command if specified")
def info(curl):
    response = monsterAPI.get_info()
    click.echo(f"{response.repr(curl=curl)}")

@click.group(help="CLI tool for Monster")
def main():
    pass


main.add_command(token)
main.add_command(put)
main.add_command(delete)
main.add_command(head)
main.add_command(get)
main.add_command(post)
main.add_command(info)

if __name__ == "__main__":
    main()
