import logging
import requests
from . import exception


logger = logging.getLogger(__name__)


class GraphAPI(object):
    """
    A wrapper for the Microsoft Graph API

    See https://github.com/Azure-Samples/data-lake-analytics-python-auth-options/blob/master/sample.py#L65-L82

    Attributes:
        resource_uri (str): The host of the API service

    Example:
        from msgraph import api
        authority = 'https://login.microsoftonline.com'
        tenant = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
        resource_uri = 'https://graph.microsoft.com'
        client_id = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
        client_thumbprint = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        client_certificate = '-----BEGIN RSA PRIVATE KEY-----...'

        client_credential = dict(thumbprint=client_thumbprint, private_key=client_certificate)
        app = msal.ConfidentialClientApplication(client_id, authority=authority_host_uri, client_credential=client_credential)

        access_token_data = app.acquire_token_for_client(scopes=scope)
        if 'access_token' not in access_token_data:
            raise ValueError(access_token_data['error_description'])
        instance = api.GraphAPI(resource_uri, access_token)
    """

    def __init__(self, resource_uri, access_token, **kwargs):
        self.resource_uri = resource_uri
        self._access_token = access_token
        self._session = requests.Session()

    def __repr__(self):
        return '<%s %s resource URI=%r>' % (self.__class__.__name__, id(self), self.resource_uri)

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
        version = kwargs.pop('version', 'v1.0')
        method = kwargs.pop('method', 'GET')
        if self.resource_uri not in uri:
            url = '%s/%s/%s' % (self.resource_uri, '%s' % version, uri)
        else:
            url = uri
        content_type = kwargs.pop('content_type', 'application/json')
        headers = {
            'Authorization': self._access_token,
            'Content-Type': content_type
        }
        method_specific_headers = kwargs.pop('headers', dict())
        headers.update(method_specific_headers)
        logger.info("Calling %s(%s)", url, method)
        try:
            response = self._session.request(method, url, headers=headers, **kwargs)
        except Exception as e:
            message = '%r %r request unsuccessful: %r' % (url, method, e)
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
