import importlib


def import_pyunicore_client():
    """Attempt to import the pyunicore.client module.

    Returns
    -------
    pyunicore.client

    Raises
    ------
    RuntimeError
        pyunicore not installed.

    """

    try:
        return importlib.import_module("pyunicore.client")
    except ModuleNotFoundError as e:
        raise RuntimeError(
            "pyunicore not available, install via "
            '`pip install "mantik[unicore]"`'
        ) from e
