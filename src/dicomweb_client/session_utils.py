import logging
import os
from typing import Optional, Any

import requests

logger = logging.getLogger(__name__)


def create_session_from_auth(
        auth: [requests.auth.AuthBase]) -> requests.Session:
    '''Creates a session from a gicen AuthBase object
    Parameters
    ----------
    auth: requests.auth.AuthBase, optional
        an implementation of `requests.auth.AuthBase` to be used for
        authentication with services

    Returns
    -------
    requests.Session
        authenticated session

    '''
    logger.debug('initialize HTTP session')
    session = requests.Session()
    session.auth = auth
    return session


def create_session_from_user_pass(username: [str],
                                  password: [str]) -> requests.Session:
    '''Creates a session from a given username and password
    Parameters
    ----------
    username: str,
        username for authentication with services
    password: str,
        password for authentication with services

    Returns
    -------
    requests.Session
        authenticated session

    '''
    logger.debug('initialize HTTP session')
    session = requests.Session()
    session.auth = (username, password)
    return session


def add_certs_to_session(session: [requests.Session],
                         ca_bundle: Optional[str] = None,
                         cert: Optional[str] = None) -> requests.Session:
    '''Adds ca_bundle and certificate to an existing session
    Parameters
    ----------
    session: requests.Session,
        input session
    ca_bundle: str, optional
        path to CA bundle file
    cert: str, optional
        path to client certificate file in Privacy Enhanced Mail (PEM) format

    Returns
    -------
    requests.Session
        verified session

    '''
    if ca_bundle is not None:
        ca_bundle = os.path.expanduser(os.path.expandvars(ca_bundle))
        if not os.path.exists(ca_bundle):
            raise OSError(
                'CA bundle file does not exist: {}'.format(ca_bundle)
            )
        logger.debug('use CA bundle file: {}'.format(ca_bundle))
        session.verify = ca_bundle
    if cert is not None:
        cert = os.path.expanduser(os.path.expandvars(cert))
        if not os.path.exists(cert):
            raise OSError(
                'Certificate file does not exist: {}'.format(cert)
            )
        logger.debug('use certificate file: {}'.format(cert))
        session.cert = cert
    return session


def create_session_from_gcp_credentials(
        google_credentials: [Any] = None) -> requests.Session:
    '''Creates a session for Google Cloud Platform
    Parameters
    ----------
    google_credentials: Any
        Google cloud credentials.
        (see https://cloud.google.com/docs/authentication/production
        for more information on Google cloud authentication).
        If not set, will be initialized to google.auth.default()

    Returns
    -------
    requests.Session
        Google cloud authorized session

    '''
    try:
        from google.auth.transport import requests as google_requests
        if google_credentials is None:
            import google.auth
            google_credentials, _ = google.auth.default(
                scopes=['https://www.googleapis.com/auth/cloud-platform'])
    except ImportError:
        raise ImportError(
            'The dicomweb-client package needs to be installed with the '
            '"gcp" extra requirements to support interaction with the '
            'Google Cloud Healthcare API: pip install dicomweb-client[gcp]'
        )
    logger.debug('initialize Google AuthorizedSession')
    return google_requests.AuthorizedSession(google_credentials)