import logging
import pathlib
import typing as t

import mantik.unicore._import as _import


logger = logging.getLogger(__name__)


class File:
    """A file in a working directory of a `Job`.

    Wrapper class around pyunicore.client.PathFile.

    """

    # NOTE (fabian.emmerich): The type hint was removed
    # since this module will be deprecated soon.
    def __init__(self, pyunicore_path_file):
        """Initiate the file

        Parameters
        ----------
        pyunicore_path_file : pyunicore.client.PathFile
            Client to the UNICORE API.

        """
        self._file = pyunicore_path_file

    @property
    def content(self) -> str:
        """Return the file's content."""
        return self._file.raw().read()

    def download(self, local_path: pathlib.Path = pathlib.Path("")):
        """Download the file.

        Parameters
        ----------
        local_path : pathlib.Path, defaults to "."
            Local path where to save the files.
            By default, the files will be saved to current
            directory.

        """
        _download_file(self._file, local_path=local_path)


class Directory:
    """A sub working directory of a `Job`.

    Wrapper class around pyunicore.client.PathDir.

    """

    # NOTE (fabian.emmerich): The type hint was removed
    # since this module will be deprecated soon.
    def __init__(self, pyunicore_path_dir):
        """Initiate the directory.

        Parameters
        ----------
        pyunicore_path_dir : pyunicore.client.PathDir
            Client to the UNICORE API.

        """
        self._directory = pyunicore_path_dir

    @property
    def path(self) -> str:
        return self._directory.name

    def download(self, local_path: pathlib.Path = pathlib.Path("")) -> None:
        """Download the directory to the local file system.

        Parameters
        ----------
        local_path : pathlib.Path, defaults to "."
            Local path where to save the files.
            By default, the files will be saved to current
            directory.

        """
        logger.debug("Downloading directory %s", self.path)
        _download_directory(self._directory, local_path=local_path)


# NOTE (fabian.emmerich): The type hint was removed
# since this module will be deprecated soon.
def _download_directory(directory, local_path: pathlib.Path) -> None:
    """Download a directory.

    Parameters
    -------
    directory : pyunicore.client.PathDir
        The directory to download.
    local_path : pathlib.Path
        The local path where to store the directory.

    """
    content = directory.storage.listdir(base=directory.name)
    logger.debug(f"Directory {directory.name} content: {content}")
    _download_directory_content(content, local_path=local_path)


def _download_directory_content(
    content: dict, local_path: pathlib.Path
) -> None:
    for obj in content.values():
        if _is_directory(obj):
            _download_directory(obj, local_path=local_path)
        else:
            _download_file(obj, local_path=local_path)


def _is_directory(obj: t.Any) -> bool:
    pyunicore = _import.import_pyunicore_client()
    return isinstance(obj, pyunicore.PathDir)


def _download_file(obj, local_path: pathlib.Path) -> None:
    """Download a file.

    Parameters
    -------
    obj : pyunicore.client.PathFile

    """
    name = local_path / obj.name
    local_path.mkdir(parents=True, exist_ok=True)
    logger.debug("Saving file %s to %s", obj.name, name)
    obj.download(name)


class WorkingDirectory:
    """A working directory of a `Job`,
    wrapper class around pyunicore.client.Storage"""

    # NOTE (fabian.emmerich): The type hint was removed
    # since this module will be deprecated soon.
    def __init__(self, storage):
        """Initiate the storage.

        Parameters
        ----------
        storage : pyunicore.client.Storage
            UNICORE storage.

        """
        self._storage = storage

    def get_directory_or_file(
        self, path: pathlib.Path
    ) -> t.Union[Directory, File]:
        pyunicore = _import.import_pyunicore_client()
        pyunicore_file_or_dir = self._open_path(path)
        if isinstance(pyunicore_file_or_dir, pyunicore.PathDir):
            return Directory(pyunicore_file_or_dir)
        elif isinstance(pyunicore_file_or_dir, pyunicore.PathFile):
            return File(pyunicore_file_or_dir)
        raise RuntimeError(f"{pyunicore_file_or_dir} not a valid path")

    # NOTE (fabian.emmerich): The type hint was removed
    # since this module will be deprecated soon.
    def _open_path(self, path: pathlib.Path):
        """Open a given path.

        Returns
        -------
        pyunicore.client.PathFile or pyunicore.client.PathDir

        """
        path_str = path.as_posix()
        try:
            pyunicore_object = self._storage.stat(path_str)
        except Exception as e:  # noqa: B902
            raise FileNotFoundError(f"{path} does not exist") from e
        return pyunicore_object

    # NOTE (fabian.emmerich): The type hint was removed
    # since this module will be deprecated soon.
    def get_entire_storage(
        self,
    ):
        """Get list pyunicore.client.PathFile or pyunicore.client.PathDir
        of all files and dir in the pyunicore.client.Storage at path "/"

        Returns
        -------
        pyunicore.client.PathFile or pyunicore.client.PathDir

        """
        yield from self._storage.listdir().values()
