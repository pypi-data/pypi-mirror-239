import click
from monsterclient import api


@click.command(help="get token")
def token():
    token = api.set_token()
    click.echo(f"token: {token}")


@click.command(help="put container or object")
@click.argument("container")
@click.argument("obj", required=False)
@click.option("-c", "--curl", is_flag=True, help="print curl command if specified")
def put(container, obj, curl):
    if obj:
        status_code, curl = api.upload_object(container, obj)
    else:
        status_code, curl = api.create_container(container)
    click.echo(f"{status_code}")
    if curl:
        click.echo()
        click.echo(f"{curl}")


@click.command(help="delete container or object")
@click.argument("container")
@click.argument("obj", required=False)
@click.option("-c", "--curl", is_flag=True, help="print curl command if specified")
def delete(container, obj, curl):
    if obj:
        status_code, curl = api.delete_object(container, obj)
    else:
        status_code, curl = api.delete_container(container)
    click.echo(f"{status_code}")
    if curl:
        click.echo()
        click.echo(f"{curl}")


@click.command(help="head container or object or account")
@click.argument("container", required=False)
@click.argument("obj", required=False)
@click.option("-c", "--curl", is_flag=True, help="print curl command if specified")
def head(container, obj, curl):
    if obj and container:
        headers, curl = api.head_object(container, obj)
    elif not obj and container:
        headers, curl = api.head_container(container)
    else:
        headers, curl = api.head_account()
    click.echo(f"{headers}")
    if curl:
        click.echo()
        click.echo(f"{curl}")


@click.command(help="get container or object or account")
@click.argument("container", required=False)
@click.argument("obj", required=False)
@click.option("-c", "--curl", is_flag=True, help="print curl command if specified")
def get(container, obj, curl):
    if obj and container:
        content, curl = api.get_object(container, obj)
    elif not obj and container:
        content, curl = api.get_container(container)
    else:
        content, curl = api.get_account()
    click.echo(f"{content}")
    if curl:
        click.echo(f"{curl}")

@click.command(help="get info")
@click.option("-c", "--curl", is_flag=True, help="print curl command if specified")
def info(curl):
    info, curlified = api.get_info()
    click.echo(f"{info}")
    if curl:
        click.echo()
        click.echo(f"{curlified}")

@click.group(help="CLI tool for monster")
def main():
    pass


main.add_command(token)
main.add_command(put)
main.add_command(delete)
main.add_command(head)
main.add_command(get)
main.add_command(info)

if __name__ == "__main__":
    main()
