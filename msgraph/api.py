import logging
import adal
import requests
import os
from . import exception


logger = logging.getLogger(__name__)


class Token(object):
    """
    Wraps the authenticated API token

    Attributes:
        expires_in (str):  The time from when the token was created until when it expires
        expires_on (datetime):  The datetime of when the token expires
        resource (str):  The resource for which a token is valid
        token_type (str):  The specific type of token
        access_token (str):  The actual token string used to interface with the API endpoint
    """
    __slots__ = ('expires_in', 'expires_on', 'resource', 'token_type', 'access_token')

    def __init__(self, expires_in, expires_on, resource, token_type, access_token):
        self.expires_in = expires_in
        self.expires_on = expires_on
        self.resource = resource
        self.token_type = token_type
        self.access_token = access_token

    def __str__(self):
        return '%s %s' % (self.token_type, self.access_token)

    def __repr__(self):
        return '<%s %s resource=%r, token_type=%r, access_token=%r, expires_on=%r>' % (self.__class__.__name__, id(self), self.resource, self.token_type, self.access_token, self.expires_on)

    @classmethod
    def from_api(cls, data):
        """
        Constructs a Token instance from an API response

        Parameters:
            data (dict):  The data returned from API response

        Returns:
            Token: The Token instance
        """
        expires_in = data['expiresIn']
        expires_on = data['expiresOn']
        resource = data['resource']
        token_type = data['tokenType']
        access_token = data['accessToken']
        return cls(expires_in, expires_on, resource, token_type, access_token)


class GraphAPI(object):
    """
    A wrapper for the Microsoft Graph API

    See https://github.com/Azure-Samples/data-lake-analytics-python-auth-options/blob/master/sample.py#L65-L82

    Attributes:
        authority_host_uri (str):  The service to login through
        tenant (str): The tenant ID of the instance
        resource_uri (str): The host of the API service
        client_id (str):  The client ID
        client_certificate (str): The contents of the authenticating SSL certificate
        client_thumbprint (str): The thumbprint corresponding to the client_certificate

    Example:
        import api
        authority_host_uri = 'https://login.microsoftonline.com'
        tenant = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
        resource_uri = 'https://graph.microsoft.com'
        client_id = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
        client_thumbprint = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        client_certificate = '-----BEGIN RSA PRIVATE KEY-----...'

        endpoint = api.GraphAPI.from_certificate(authority_host_uri, tenant, resource_uri, client_id, client_certificate, client_thumbprint)
    """

    def __init__(self, authority_host_uri, tenant, resource_uri, client_id, access_token, **kwargs):
        self.authority_host_uri = authority_host_uri
        self.tenant = tenant
        self.resource_uri = resource_uri
        self.client_id = client_id
        self._access_token = access_token
        self.client_certificate = kwargs.get('client_certificate')
        self.certificate_footprint = kwargs.get('certificate_footprint')
        self._session = requests.Session()

    def __repr__(self):
        return '<%s %s authority_host_uri=%r, tenant ID=%r, resource URI=%r, client ID=%r>' % (self.__class__.__name__, id(self), self.authority_host_uri, self.tenant, self.resource_uri, self.client_id)

    def request(self, uri, **kwargs):
        """
        Makes a requested to the API endpoint

        Parameters:
            uri (str):  The specific endpoint which to send/receive data from

        Keyword Arguments:
            version (str):  The version of the API to use
            data (object):  The payload to send to the API endpoint
            json (obj):  The JSON payload to send the API endpoint
            method (str):  The type of HTTP Method to call the API endpoint with

        Returns:
            object: The JSON response from the API

        Raises:
            MicrosoftException: The API call was not completed successsfully
        """
        version = kwargs.get('version', '1.0')
        method = kwargs.pop('method', 'GET')
        if self.resource_uri not in uri:
            url = os.path.join(self.resource_uri, 'v%s' % version, uri)
        else:
            url = uri
        token = str(self._access_token)
        content_type = kwargs.pop('content_type', 'application/json')
        headers = {
            'Authorization': token,
            'Content-Type': content_type
        }
        method_specific_headers = kwargs.pop('headers', dict())
        headers.update(method_specific_headers)
        logger.info("Calling %s(%s)", url, method)
        try:
            response = self._session.request(method, url, headers=headers, **kwargs)
        except Exception as e:
            message = '%r %r request unsuccessful: %r' % (url, method, e.message)
            logger.error(message, exc_info=1)
            code = getattr(e, 'code', None)
            raise exception.MicrosoftException(code, message)
        else:
            try:
                data = response.json()
            except Exception:
                return response.content
            logger.debug('%s - %r: %r', method, url, data)
        if 'error' in data:
            error = data['error']
            code = error['code']
            message = error['message']
            logger.error(error)
            raise exception.MicrosoftException(code, message)
        return data

    @staticmethod
    def _authenticate_via_certificate(authority_host_uri, tenant, resource_uri, client_id, client_certificate, certificate_thumbprint):
        authority_uri = os.path.join(authority_host_uri, tenant)
        try:
            context = adal.AuthenticationContext(authority_uri, api_version=None)
            data = context.acquire_token_with_client_certificate(resource_uri, client_id, client_certificate, certificate_thumbprint)
        except Exception as e:
            message = "Failed to authenticate with %r:%" % (resource_uri, e)
            logger.error('%r: %r', message, e.message, exc_info=1)
            raise exception.MicrosoftAuthenticationException(e.code, e.message)
        else:
            access_token = Token.from_api(data)
            return access_token

    @classmethod
    def from_certificate(cls, authority_host_uri, tenant, resource_uri, client_id, client_certificate, certificate_thumbprint):
        """
        Creates an authenticated instance using an SSL certificate

        Parameters:
            authority_host_uri (str):  The service to login through
            tenant (str): The tenant ID of the instance
            resource_uri (str): The host of the API service
            client_id (str):  The client ID
            client_certificate (str): The contents of the authenticating SSL certificate
            client_thumbprint (str): The thumbprint corresponding to the client_certificate

        Returns:
            GraphAPI:  The authenticated API instance
        """
        access_token = cls._authenticate_via_certificate(authority_host_uri, tenant, resource_uri, client_id, client_certificate, certificate_thumbprint)
        return cls(authority_host_uri, tenant, resource_uri, client_id, access_token, client_certificate=client_certificate, certificate_thumbprint=certificate_thumbprint)

