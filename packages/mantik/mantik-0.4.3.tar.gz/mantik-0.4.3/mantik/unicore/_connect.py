import base64
import logging

import mantik.unicore._import as _import
import mantik.unicore.exceptions as exceptions

logger = logging.getLogger(__name__)


# NOTE (fabian.emmerich): The type hint was removed
# since this module will be deprecated soon.
def create_unicore_api_connection(
    api_url: str,
    user: str,
    password: str,
):
    """Create a connection to a cluster of a UNICORE API.

    Parameters
    ----------
    api_url : str
        REST API URL to the cluster's UNICORE server.
    user : str
        JUDOOR user name.
    password : str
        Corresponding JUDOOR user password.

    Raises
    ------
    AuthenticationFailedException
        Authentication on the cluster failed.

    Returns
    -------
    pyunicore.client.Client

    """
    logger.info("Attempting to connect to %s", api_url)
    connection = _connect_to_cluster(
        api_url=api_url,
        user=user,
        password=password,
    )
    if _authentication_failed(connection):
        raise exceptions.AuthenticationFailedException(
            f"Failed to connect to {api_url} -- "
            "check if user and password are correct"
        )
    logger.info("Successfully connected to %s", api_url)
    return connection


# NOTE (fabian.emmerich): The type hint was removed
# since this module will be deprecated soon.
def _connect_to_cluster(
    api_url: str,
    user: str,
    password: str,
):
    """Start a UNICORE job.

    Parameters
    ----------
    api_url : str
        UNICORE API URL.
    user : str
        UNICORE username.
    password : str
        User password.

    Returns
    -------
    pyunicore.client.Client

    """
    transport = _create_transport(user=user, password=password)
    try:
        client = _create_client(transport=transport, api_url=api_url)
    # In the current version of pyunicore a base Exception is raised
    # when a client is instantiated when the Auth fails.
    # In newer versions it should be possible
    # to catch a pyunicore.credentials.AuthenticationFailedException.
    except Exception:
        raise exceptions.AuthenticationFailedException(
            f"Failed to connect to {api_url} -- "
            "check if user and password are correct"
        )
    logger.debug("Connection properties: %s", client.properties)
    return client


# NOTE (fabian.emmerich): The type hint was removed
# since this module will be deprecated soon.
def _create_transport(user: str, password: str):
    """Create a UNICORE transport with user credentials.

    Parameters
    ----------
    user : str
        UNICORE username.
    password : str
        User password.

    Returns
    -------
    pyunicore.client.Transport

    """
    pyunicore = _import.import_pyunicore_client()
    logger.debug("Creating transport for user %s", user)
    token = _create_token(user=user, password=password)
    return pyunicore.Transport(credential=token, oidc=False)


def _create_token(user: str, password: str) -> str:
    token = f"{user}:{password}".encode()
    return base64.b64encode(token).decode("ascii")


# NOTE (fabian.emmerich): The type hint was removed
# since this module will be deprecated soon.
def _create_client(transport, api_url: str):
    """Create the UNICORE client.

    Parameters
    ----------
    transport : pyunicore.client.Transport
        UNICORE transport.
    api_url : str
        UNICORE API URL.

    Returns
    -------
    pyunicore.client.Client

    """
    pyunicore = _import.import_pyunicore_client()
    logger.debug("Creating client connection using REST API URL %s", api_url)
    return pyunicore.Client(transport=transport, site_url=api_url)


# NOTE (fabian.emmerich): The type hint was removed
# since this module will be deprecated soon.
def _authentication_failed(client) -> bool:
    """Check if authentication has failed.

    Parameters
    ----------
    client : pyunicore.client.Client
        UNICORE client.

    Returns
    -------
    bool

    """
    logger.debug(
        "Connection login information: %s",
        client.properties["client"]["xlogin"],
    )
    return False if client.properties["client"]["xlogin"] else True
