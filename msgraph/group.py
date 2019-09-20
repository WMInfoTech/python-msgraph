import logging
from datetime import datetime


logger = logging.getLogger(__name__)
date_format = '%Y-%m-dT%H:%M:%SZ'


class Group(object):
    """
    Azure Active Directory (Azure AD) group.  Represents an Azure Active Directory (Azure AD) group, which can be an Office 365 group, or a security group.

    Attributes:
        id (str): The unique identifier for the group.
        deleted_datetime (datetime):  When the group was deleted
        classification (str):  Describes a classification for the group (such as low, medium or high business impact). Valid values for this property are defined by creating a ClassificationList setting value, based on the template definition.
        created_datetime (datetime):  Timestamp of when the group was created.
        creation_options (str):
        description (str):  An optional description for the group.
        display_name (str):  The display name for the group
        group_types (list):  Specifies the group type and its membership.
        email_address (str):
        mail_enabled (bool):  Specifies whether the group is mail-enabled.
        mail_nickname (str):  The mail alias for the group, unique in the organization
        on_premises_last_sync_datetime (datetime):  Indicates the last time at which the group was synced with the on-premises directory.
        on_premises_security_identifier (str):  Contains the on-premises security identifier (SID) for the group that was synchronized from on-premises to the cloud.
        on_premises_sync_enabled (bool):  Indicated if om premise sync is enabled
        preferred_data_location (str):  The preferred data location for the group. For more information, see OneDrive Online Multi-Geo.
        proxy_addresses (list):  Email addresses for the group that direct to the same group mailbox.
        renewed_date_time (str):  Timestamp of when the group was last renewed
        resource_behavior_options (str):
        resource_provisioning_options (str):
        security_enabled (bool):  	Specifies whether the group is a security group.
        visibility (str):  	Specifies the visibility of an Office 365 group
        on_premises_provisioning_errors (str):  Errors when using Microsoft synchronization product during provisioning.
    """
    __slots__ = ('id', 'deleted_datetime', 'classification', 'created_datetime', 'creation_options', 'description', 'display_name', 'group_types', 'email_address', 'mail_enabled', 'mail_nickname', 'on_premises_last_sync_datetime', 'on_premises_security_identifier', 'on_premises_sync_enabled', 'preferred_data_location', 'proxy_addresses', 'renewed_date_time', 'resource_behavior_options', 'resource_provisioning_options', 'security_enabled', 'visibility', 'on_premises_provisioning_errors')

    def __init__(self, id, deleted_datetime, classification, created_datetime, creation_options, description, display_name, group_types, email_address, mail_enabled, mail_nickname, on_premises_last_sync_datetime, on_premises_security_identifier, on_premises_sync_enabled, preferred_data_location, proxy_addresses, renewed_date_time, resource_behavior_options, resource_provisioning_options, security_enabled, visibility, on_premises_provisioning_errors):
        self.id = id
        self.deleted_datetime = deleted_datetime
        self.classification = classification
        self.created_datetime = created_datetime
        self.creation_options = creation_options
        self.description = description
        self.display_name = display_name
        self.group_types = group_types
        self.email_address = email_address
        self.mail_enabled = mail_enabled
        self.mail_nickname = mail_nickname
        self.on_premises_last_sync_datetime = on_premises_last_sync_datetime
        self.on_premises_security_identifier = on_premises_security_identifier
        self.on_premises_sync_enabled = on_premises_sync_enabled
        self.preferred_data_location = preferred_data_location
        self.proxy_addresses = proxy_addresses
        self.renewed_date_time = renewed_date_time
        self.resource_behavior_options = resource_behavior_options
        self.resource_provisioning_options = resource_provisioning_options
        self.security_enabled = security_enabled
        self.visibility = visibility
        self.on_premises_provisioning_errors = on_premises_provisioning_errors

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<%s %s id=%s display_name=%r, email_address=%r>' % (self.__class__.__name__, id(self), self.display_name, self.email_address)

    def update(self, api):
        """
        Update the Group at the API endpoint

        Parameters:
            api (msgraph.api.GraphAPI):  The endpoint at which to update the Category instance
        """
        uri = 'groups/%s' % self.id
        data = {
            'description': self.description,
            'displayName': self.display_name,
            'groupTypes': self.group_types,
            'mailEnabled': self.mail_enabled,
            'mailNickname': self.mail_nickname,
            'securityEnabled': self.security_enabled,
            'visibility': self.visibility
        }
        api.request(uri, json=data, method='PATCH')
        logger.debug('Updated %r in %r', self, api)

    def delete(self, api):
        """
        Deletes the Group instance from the API endpoint

        Parameters:
            api (msgraph.api.GraphAPI):  The endpoint from which to fetch data
        """
        uri = 'groups/%s' % self.id
        api.request(uri, method='DELETE')
        logger.debug('Deleted %r in %r', self, api)

    @classmethod
    def from_api(cls, data):
        id = data['id']
        raw_deleted_datetime = data['deletedDateTime']
        if raw_deleted_datetime:
            deleted_datetime = datetime.strptime(deleted_datetime, datetime_format)
        else:
            deleted_datetime = None
        classification = data['classification']
        raw_created_datetime = data['createdDateTime']
        if raw_created_datetime:
            created_datetime = datetime.strptime(raw_created_datetime, datetime_format)
        else:
            created_datetime = None
        creation_options = data['creationOptions']
        description = data['description']
        display_name = data['display_name']
        group_types = data['group_types']
        email_address = data['email_address']
        mail_enabled = data['mail_enabled']
        mail_nickname = data['mail_nickname']
        on_premises_last_sync_datetime = data['on_premises_last_sync_datetime']
        on_premises_security_identifier = data['on_premises_security_identifier']
        on_premises_sync_enabled = data['on_premises_sync_enabled']
        preferred_data_location = data['preferred_data_location']
        proxy_addresses = data['proxy_addresses']
        raw_renewed_date_time = data['renewed_date_time']
        if raw_renewed_date_time:
            renewed_date_time = datetime.strptime(raw_renewed_date_time, datetime_format)
        else:
            renewed_date_time = None
        resource_behavior_options = data['resource_behavior_options']
        resource_provisioning_options = data['resource_provisioning_options']
        security_enabled = data['security_enabled']
        visibility = data['visibility']
        on_premises_provisioning_errors = data['on_premises_provisioning_errors']
        return cls(id, deleted_datetime, classification, created_datetime, creation_options, description, display_name, group_types, email_address, mail_enabled, mail_nickname, on_premises_last_sync_datetime, on_premises_security_identifier, on_premises_sync_enabled, preferred_data_location, proxy_addresses, renewed_date_time, resource_behavior_options, resource_provisioning_options, security_enabled, visibility, on_premises_provisioning_errors)

    @classmethod
    def get(cls, api, **kwargs):
        """
        Fetches Group instances from the API endpoint

        Parameters:
            api (msgraph.api.GraphAPI):  The endpoint from which to fetch data

        Keyword Arguments:
            page_size (int):  The number of items to include in each page, default: 100

        Returns:
            (list):  Group instances
        """
        uri = 'groups'

        params = {
            '$top': kwargs.get('page_size', 100)
        }
        data = api.request(uri, params=params)
        output = [cls.from_api(row) for row in data.get('value', [])]
        while data.get("@odata.nextLink"):
            uri = data.get("@odata.nextLink")
            data = api.request(uri)
            output += [cls.from_api(row) for row in data.get('value', [])]
        return output

    @classmethod
    def create(cls, api, display_name, mail_enabled, mail_nickname, security_enabled, **kwargs):
        """
        Fetches User instances from the API endpoint that were created from a certain point forward

        If a uri is not specified, will return a list users created since the beginning of time.
        The process will return a list of User instances along with a deltaLink.  The deltaLink
        should be used during the next execution to fetch all User instances that were created/updated
        since the previous execution when the deltaLink was obtained.

        For more information see: https://docs.microsoft.com/en-us/graph/delta-query-users

        Parameters:
            api (msgraph.api.GraphAPI):  The endpoint in which to create the Group
            display_name (str):  The name to use for the Group
            mail_enabled (bool):  Enable mail for the Group
            mail_nickname (str):  Mail alias for the Group
            security_enabled (bool):  Enable security for the Group

        Keyword Arguments:
            owners (list): owners for the group at creation time
            members (list): members for the group at creation time

        Returns:
            (Group):  created Group instance
        """
        owners = kwargs.get('owners', [])
        members = kwargs.get('members', [])

        data = {
            'displayName': self.display_name,
            'mailEnabled': self.mail_enabled,
            'mailNickname': self.mail_nickname,
            'securityEnabled': self.security_enabled,
            'owners': owners,
            'members': members
        }
        uri = 'groups'
        results = api.request(uri, json=data, method='POST')
        instance = cls.from_api(results)
        logger.debug('Created %r in %r', instance, api)
        return instance
