import logging
from datetime import datetime


logger = logging.getLogger(__name__)

date_format = '%Y-%m-%d'
datetime_format = date_format + 'T%H:%M:%S'
full_datetime_format = date_format + 'T%H:%M:%S.%f'


class User(object):
    """
    Represents a User in Microsoft Graph

    for detailed information see https://docs.microsoft.com/en-us/graph/api/resources/users?view=graph-rest-1.0

    Attributes:
        id (str):  The unique indentifier of the user
        display_name (str):  The displayed name of the user
        email_address (str):  The email address of the user
        preferred_language (str):  The language preferred by the user
        user_principal_name (str):  The principal name of the user
        office_location (str):  The location of the user's office
        job_title (str):  The job title of the user
        given_name (str): The given_name of the user
        surname (str):  The surname of the user
        mobile_phone (str): The mobile phone number of the user
        business_phones (list):  The business phone numbers of the user
        mail_nickname (str):  The mail alias for the user
        account_enabled (bool): Indicates if the User account is enabled
        password_profile (dict): The password profile for the user
        removed (dict|None):  Used in delta API calls, denoted if a user is new/changed
    """
    __slots__ = ('id', 'display_name', 'email_address', 'preferred_language', 'user_principal_name', 'office_location', 'job_title', 'given_name', 'surname', 'mobile_phone', 'business_phones', 'mail_nickname', 'account_enabled', 'password_profile', 'created_at', 'removed')

    def __init__(self, id, display_name, email_address, preferred_language, user_principal_name, office_location, job_title, given_name, surname, mobile_phone, business_phones, mail_nickname, account_enabled, password_profile, created_at, removed):
        self.id = id
        self.display_name = display_name
        self.email_address = email_address
        self.preferred_language = preferred_language
        self.user_principal_name = user_principal_name
        self.office_location = office_location
        self.job_title = job_title
        self.given_name = given_name
        self.surname = surname
        self.mobile_phone = mobile_phone
        self.business_phones = business_phones
        self.mail_nickname = mail_nickname
        self.account_enabled = account_enabled
        self.password_profile = password_profile
        self.created_at = created_at
        self.removed = removed

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<%s %s id=%r, display_name=%r, email_address=%r, user_principal_name=%r, given_name=%r, surname=%r>' % (self.__class__.__name__, id(self), self.id, self.display_name, self.email_address, self.user_principal_name, self.given_name, self.surname)

    def update(self, api):
        """
        Updates the User in the given API endpoint

        Parameters:
            api (msgraph.api.GraphAPI):  The endpoint at which to save the User
        """
        uri = 'users/%s' % self.id
        data = dict(displayName=self.display_name, mail=self.mail, preferredLanguage=self.preferred_language, officeLocation=self.office_location, jobTitle=self.job_title, givenName=self.given_name, surname=self.surname, mobilePhone=self.mobile_phone, businessPhones=self.business_phones)
        api.request(uri, json=data, method='PATCH')

    @classmethod
    def from_api(cls, data):
        """
        Builds a User instance from data returned from an API endpoint

        Parameters:
            data (dict):  raw data returned from the API

        Returns:
            User: the User instance built from the provided data
        """
        id = data.get('id')
        display_name = data.get('displayName')
        email_address = data.get('mail')
        preferred_language = data.get('preferredLanguage')
        user_principal_name = data.get('userPrincipalName')
        office_location = data.get('officeLocation')
        job_title = data.get('jobTitle')
        given_name = data.get('givenName')
        surname = data.get('surname')
        mobile_phone = data.get('mobilePhone')
        business_phones = data.get('businessPhones')
        mail_nickname = data.get('mailNickname')
        account_enabled = data.get('accountEnabled')
        password_profile = data.get('passwordProfile')
        created_at = data.get('createdDateTime')
        if created_at:
            created_at = datetime.strptime(created_at[:-1], datetime_format)
        removed = data.get('@removed')
        return cls(id, display_name, email_address, preferred_language, user_principal_name, office_location, job_title, given_name, surname, mobile_phone, business_phones, mail_nickname, account_enabled, password_profile, created_at, removed)

    @classmethod
    def me(cls, api):
        """
        Fetches the User instance of the user currently logged in

        Parameters:
            api (msgraph.api.GraphAPI):  The endpoint from which to fetch data

        Returns:
            User: the User instance of the user currently logged in
        """
        uri = 'users/me'
        data = api.request(uri)
        return cls.from_api(data)

    @classmethod
    def delta(cls, api, uri=None, **kwargs):
        """
        Fetches User instances from the API endpoint that were created from a certain point forward

        If a uri is not specified, will return a list users created since the beginning of time.
        The process will return a list of User instances along with a deltaLink.  The deltaLink
        should be used during the next execution to fetch all User instances that were created/updated
        since the previous execution when the deltaLink was obtained.

        For more information see: https://docs.microsoft.com/en-us/graph/delta-query-users

        Parameters:
            api (msgraph.api.GraphAPI):  The endpoint from which to fetch data
            uri (str, optional):  The delta link previously used

        Returns:
            (tuple):  list of User instances created/updated since the uri was last received, and the delta URL

        Example:
            from msgraph import user

            users, delta_link = user.User.delta(api_instance)
            ...
            # at some point in the future, fetch Users created/updated since the delta method was last executed
            new_updated_users, delta_link = user.User.delta(api_instance, delta_link)
        """
        fields = kwargs.get('fields', ['id', 'displayName', 'mail', 'preferredLanguage', 'userPrincipalName', 'officeLocation', 'jobTitle', 'givenName', 'surname', 'mobilePhone', 'businessPhones', 'mailNickname', 'accountEnabled', 'passwordProfile', 'createdDateTime'])
        if uri:
            data = api.request(uri)
        else:
            uri = 'users/delta'
            params = {
                '$select': ','.join(fields)
            }
            data = api.request(uri, params=params)

        output = [cls.from_api(row) for row in data.get('value', [])]
        while data.get("@odata.nextLink"):
            uri = data.get("@odata.nextLink")
            data = api.request(uri)
            output += [cls.from_api(row) for row in data.get('value', [])]
        delta_link = data['@odata.deltaLink']
        return output, delta_link

    @classmethod
    def get(cls, api, user=None, **kwargs):
        """
        Fetches User instances from the API endpoint

        Parameters:
            api (msgraph.api.GraphAPI):  The endpoint from which to fetch data
            user (str, optional):  The User Principal Name for which to fetch data

        Keyword Arguments:
            page_size (int):  The number of User instances to include in each page, default: 100

        Returns:
            (list|User):  If a user specified, the requested User instance, otherwise a list of User instances
        """
        fields = kwargs.get('fields', ['id', 'displayName', 'mail', 'preferredLanguage', 'userPrincipalName', 'officeLocation', 'jobTitle', 'givenName', 'surname', 'mobilePhone', 'businessPhones', 'mailNickname', 'accountEnabled', 'passwordProfile', 'createdDateTime'])
        if user:
            uri = 'users/%s' % user
        else:
            uri = 'users'

        params = {
            '$top': kwargs.get('page_size', 100),
            '$select': ','.join(fields)
        }
        data = api.request(uri, params=params)
        if user:
            output = cls.from_api(data)
        else:
            output = []
            while data.get("@odata.nextLink"):
                uri = data.get("@odata.nextLink")
                data = api.request(uri)
                output += [cls.from_api(row) for row in data.get('value', [])]
        return output

    @classmethod
    def create(cls, api, display_name, user_principal_name, mail_nickname, password_profile, **kwargs):
        """
        Create a User in the specified API endpoint

        For detailed information on the password_profile, see https://docs.microsoft.com/en-us/graph/api/resources/passwordprofile?view=graph-rest-1.0

        Parameters:
            api (msgraph.api.GraphAPI):  The endpoint in which to create the User instance
            display_name (str):  The display name for the User instance
            user_principal_name (str):  The email-address of the User
            mail_nickname (str): The mail alias for the user
            password_profile (dict):  A password Profile for the User

        Keyword Arguments:
            account_enabled (bool):  Indicates if the User account should be enabled, defaults to True
            on_premises_immutable_id (str): ID used when using a federated domain for the user's userPrincipalName, defaults to None

        Returns:
            User: created User instance
        """
        account_enabled = kwargs.get('account_enabled', True)
        data = dict(displayName=display_name, userPrincipalName=user_principal_name, mailNickname=mail_nickname, passwordProfile=password_profile, accountEnabled=account_enabled)
        on_premises_immutable_id = kwargs.get('on_premises_immutable_id')
        if on_premises_immutable_id:
            data['onPremiseImmutableId'] = on_premises_immutable_id
        uri = 'users'
        results = api.request(uri, json=data, method='POST')
        instance = cls.from_api(results)
        logger.debug('Created %r with %r', instance, api)
        return instance
