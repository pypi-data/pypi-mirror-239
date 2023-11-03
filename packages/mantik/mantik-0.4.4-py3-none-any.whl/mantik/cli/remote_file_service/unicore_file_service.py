import uuid

import click

import mantik.cli.main as main
import mantik.remote_file_service.data_client as data_client

GROUP_NAME = "unicore-file-service"


@main.cli.group(GROUP_NAME)
def cli() -> None:
    """Interaction with the unicore file service."""


@cli.command("copy-file")
@click.argument("source", type=str, nargs=1, required=True)
@click.argument("target", type=str, nargs=1, required=True)
@click.option(
    "--connection-id",
    type=uuid.UUID,
    default=None,
)
def copy_file(source: str, target: str, connection_id: uuid.UUID) -> None:
    unicore_file_service = _import_unicore_file_service()
    uc_fs = data_client.DataClient.from_env(
        connection_id=connection_id,
        remote_fs_type=unicore_file_service.UnicoreFileService,
    )
    file = uc_fs.copy_file(source=source, target=target)
    click.echo(file)


@cli.command("remove-file")
@click.argument("target", type=str, nargs=1, required=True)
@click.option(
    "--connection-id",
    type=uuid.UUID,
    default=None,
)
def remove_file(target: str, connection_id: uuid.UUID) -> None:
    unicore_file_service = _import_unicore_file_service()
    uc_fs = data_client.DataClient.from_env(
        connection_id=connection_id,
        remote_fs_type=unicore_file_service.UnicoreFileService,
    )
    uc_fs.remove_file(target=target)
    click.echo("File removed!")


@cli.command("create-file")
@click.argument("target", type=str, nargs=1, required=True)
@click.option(
    "--connection-id",
    type=uuid.UUID,
    default=None,
)
def create_file_if_not_exists_file(
    target: str, connection_id: uuid.UUID
) -> None:
    unicore_file_service = _import_unicore_file_service()
    uc_fs = data_client.DataClient.from_env(
        connection_id=connection_id,
        remote_fs_type=unicore_file_service.UnicoreFileService,
    )
    file = uc_fs.create_file_if_not_exists(target=target)
    click.echo(file)


@cli.command("list-directory")
@click.argument("target", type=str, nargs=1, required=True)
@click.option(
    "--connection-id",
    type=uuid.UUID,
    default=None,
)
def list_directory(target: str, connection_id: uuid.UUID) -> None:
    unicore_file_service = _import_unicore_file_service()
    uc_fs = data_client.DataClient.from_env(
        connection_id=connection_id,
        remote_fs_type=unicore_file_service.UnicoreFileService,
    )
    directory = uc_fs.list_directory(target=target)
    click.echo(directory)


@cli.command("create-directory")
@click.argument("target", type=str, nargs=1, required=True)
@click.option(
    "--connection-id",
    type=uuid.UUID,
    default=None,
)
def create_directory(target: str, connection_id: uuid.UUID) -> None:
    unicore_file_service = _import_unicore_file_service()
    uc_fs = data_client.DataClient.from_env(
        connection_id=connection_id,
        remote_fs_type=unicore_file_service.UnicoreFileService,
    )
    directory = uc_fs.create_directory(target=target)
    click.echo(directory)


@cli.command("remove-directory")
@click.argument("target", type=str, nargs=1, required=True)
@click.option(
    "--connection-id",
    type=uuid.UUID,
    default=None,
)
def remove_directory(target: str, connection_id: uuid.UUID) -> None:
    unicore_file_service = _import_unicore_file_service()
    uc_fs = data_client.DataClient.from_env(
        connection_id=connection_id,
        remote_fs_type=unicore_file_service.UnicoreFileService,
    )
    uc_fs.remove_directory(target=target)
    click.echo("Directory removed!")


@cli.command("copy-directory")
@click.argument("source", type=str, nargs=1, required=True)
@click.argument("target", type=str, nargs=1, required=True)
@click.option(
    "--connection-id",
    type=uuid.UUID,
    default=None,
)
def copy_directory(source: str, target: str, connection_id: uuid.UUID) -> None:
    unicore_file_service = _import_unicore_file_service()
    uc_fs = data_client.DataClient.from_env(
        connection_id=connection_id,
        remote_fs_type=unicore_file_service.UnicoreFileService,
    )
    directory = uc_fs.copy_directory(source=source, target=target)
    click.echo(directory)


@cli.command("exists")
@click.argument("path", type=str, nargs=1, required=True)
@click.option(
    "--connection-id",
    type=uuid.UUID,
    default=None,
)
def exists(path: str, connection_id: uuid.UUID) -> None:
    unicore_file_service = _import_unicore_file_service()
    uc_fs = unicore_file_service.UnicoreFileService.from_env(
        connection_id=connection_id
    )
    _exists = uc_fs.exists(path=path)
    click.echo(_exists)


@cli.command("user")
@click.option(
    "--connection-id",
    type=uuid.UUID,
    default=None,
)
def user(connection_id: uuid.UUID) -> None:
    unicore_file_service = _import_unicore_file_service()
    uc_fs = data_client.DataClient.from_env(
        connection_id=connection_id,
        remote_fs_type=unicore_file_service.UnicoreFileService,
    )
    click.echo(uc_fs.user)


def _import_unicore_file_service():
    try:
        import mantik.remote_file_service.unicore_file_service as unicore_file_service  # noqa: E501
    except ModuleNotFoundError as e:
        raise RuntimeError(
            "Extras for UNICORE file service must be "
            'installed via `pip install "mantik[unicore]"`'
        ) from e
    else:
        return unicore_file_service
