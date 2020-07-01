import logging


logger = logging.getLogger(__name__)


class Site(object):
    __slots__ = ('id', 'name', 'display_name', 'description', 'etag', 'root', 'sharepoint_ids', 'site_collection', 'web_url', 'created_datetime', 'last_modified_datetime')

    def __init__(self, id, name, display_name, description, etag, root, sharepoint_ids, site_collection, web_url, created_datetime, last_modified_datetime):
        self.id = id
        self.name = name
        self.display_name = display_name
        self.description = description
        self.etag = etag
        self.root = root
        self.sharepoint_ids = sharepoint_ids
        self.site_collection = site_collection
        self.web_url = web_url
        self.created_datetime = created_datetime
        self.last_modified_datetime = last_modified_datetime

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<%s %s id=%r, name=%r, display_name=%r, created_datetime=%s>' % (self.__class__.__name__, id(self), self.id, self.name, self.display_name, self.created_datetime)

    def subsites(self, api, **kwargs):
        """
        Fetches the subsites of a given SharePoint site from the Microsoft Graph instance

        Parameters:
            api (msgraph.api.GraphAPI):  The endpoint from which to fetch data

        Keyword Arguments:
            page_size (int):  The number of items to include in each page, default: 100

        Returns:
            list: Site instances
        """
        uri = 'sites/%s/sites' % self.id
        params = {
            '$top': kwargs.get('page_size', 100)
        }
        cls = self.__class__
        data = api.request(uri, params=params)
        output = [cls.from_api(row) for row in data.get('value', [])]
        while data.get("@odata.nextLink"):
            uri = data.get("@odata.nextLink")
            data = api.request(uri)
            output += [cls.from_api(row) for row in data.get('value', [])]
        return output

    @classmethod
    def from_api(cls, data):
        id = data['id']
        name = data['name']
        display_name = data['displayName']
        description = data.get('description')
        etag = data.get('eTag')
        root = data.get('root')
        sharepoint_ids = data.get('sharepointIds')
        site_collection = data.get('siteCollection')
        web_url = data['webUrl']
        created_datetime = data['createdDateTime']
        last_modified_datetime = data['lastModifiedDateTime']
        return cls(id, name, display_name, description, etag, root, sharepoint_ids, site_collection, web_url, created_datetime, last_modified_datetime)

    @classmethod
    def get(cls, api, **kwargs):
        """
        Fetches a given Site by id of the site from the Microsoft Graph instance

        If a site id is not provided, the root SharePoint site within the tenant will be fetched

        Parameters:
            api (msgraph.api.GraphAPI):  The endpoint from which to fetch data

        Keyword Arguments:
            site (Site|str):  The number of items to include in each page, default: None
            page_size (int):  The number of items to include in each page, default: 100

        Returns:
            Site: instance of the requested site
        """
        site = kwargs.get('site')

        if site:
            uri = 'sites/%s' % site
        else:
            uri = 'sites/root'
        data = api.request(uri)
        return cls.from_api(data)

    @classmethod
    def by_group(cls, api, group):
        """
        Fetches the team SharePoint site for a given group from the Microsoft Graph instance

        Parameters:
            api (msgraph.api.GraphAPI):  The endpoint from which to fetch data
            group (Group|str): The group (or group ID) whose site is being fetched

        Returns:
            Site: team site for the given group
        """
        uri = 'groups/%s/sites/root' % group
        data = api.request(uri)
        return cls.from_api(data)

    @classmethod
    def by_relative_url(cls, api, host_name, path):
        """
        Fetches a Site instance by the server-relative URL of the site

        Parameters:
            api (msgraph.api.GraphAPI):  The endpoint from which to fetch data
            host_name (str): The host name of the site
            path (str):  The server-relative URL of the site

        Returns:
            Site: Site instance specified by the relative URL
        """
        uri = 'sites/%s:/%s' % (host_name, path)
        data = api.request(uri)
        return cls.from_api(data)

    @classmethod
    def search(cls, api, query, **kwargs):
        """
        Fetches SharePoint sites matching the provided search query from the Microsoft Graph instance

        Parameters:
            api (msgraph.api.GraphAPI):  The endpoint from which to fetch data
            query (str): A string to search for in the Site instance

        Keyword Arguments:
            page_size (int):  The number of items to include in each page, default: 100

        Returns:
            list: Site instances matching the provided query
        """
        params = {
            'search': query,
            '$top': kwargs.get('page_size', 100)
        }
        uri = 'sites'
        data = api.request(uri, params=params)
        output = [cls.from_api(row) for row in data.get('value', [])]
        while data.get("@odata.nextLink"):
            uri = data.get("@odata.nextLink")
            data = api.request(uri)
            output += [cls.from_api(row) for row in data.get('value', [])]
        return output


class SiteList(object):
    __slots__ = ('id', 'name', 'display_name', 'description', 'list_instance', 'parent_reference', 'web_url', 'created_datetime', 'created_by', 'last_modified_datetime', 'last_modified_by')

    def __init__(self, id, name, display_name, description, list_instance, parent_reference, web_url, created_datetime, created_by, last_modified_datetime, last_modified_by):
        self.id = id
        self.name = name
        self.display_name = display_name
        self.description = description
        self.list_instance = list_instance
        self.parent_reference = parent_reference
        self.web_url = web_url
        self.created_datetime = created_datetime
        self.created_by = created_by
        self.last_modified_datetime = last_modified_datetime
        self.last_modified_by = last_modified_by

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<%s %s id=%r, name=%r, display_name=%r, created_datetime=%s>' % (self.__class__.__name__, id(self), self.id, self.name, self.display_name, self.created_datetime)

    @classmethod
    def from_api(cls, data):
        id = data['id']
        name = data['name']
        display_name = data['displayName']
        description = data['description']
        list_instance = data['list']
        parent_reference = data['parentReference']
        web_url = data['webUrl']
        created_datetime = data['createdDateTime']
        created_by = data['createdBy']
        last_modified_datetime = data['lastModifiedDateTime']
        last_modified_by = data.get('lastModifiedBy')
        return cls(id, name, display_name, description, list_instance, parent_reference, web_url, created_datetime, created_by, last_modified_datetime, last_modified_by)

    @classmethod
    def get(cls, api, site, **kwargs):
        """
        Fetches lists for a given SharePoint site from the Microsoft Graph instance

        If a list_instance is provided, only that list will be fetched

        Parameters:
            api (msgraph.api.GraphAPI):  The endpoint from which to fetch data
            site (Site|str): The SharePoint site (or site ID of the Site) to fetch lists for

        Keyword Arguments:
            list_instance (List|str): A given SiteList (or list ID) to fetch
            page_size (int):  The number of items to include in each page, default: 100

        Returns:
            (SiteList|list): If a list_instance is provided, the single SiteList instance, list of all Site lists otherwise
        """
        list_instance = kwargs.pop('list_instance', None)
        uri = 'sites/%s/lists' % site
        if list_instance:
            uri += '/%s' % list_instance

        params = {
            '$top': kwargs.get('page_size', 100)
        }

        data = api.request(uri, params=params)
        if list_instance:
            return cls.from_api(data)
        output = [cls.from_api(row) for row in data.get('value', [])]
        while data.get("@odata.nextLink"):
            uri = data.get("@odata.nextLink")
            data = api.request(uri)
            output += [cls.from_api(row) for row in data.get('value', [])]
        return output

    @classmethod
    def create(cls, api, site, display_name, template, columns):
        """
        Creates a new list for a given site in the Microsoft Graph instance

        Parameters:
            api (msgraph.api.GraphAPI):  The endpoint from which to save data
            site (Site|str): The SharePoint site (or site ID of the Site) to associate the new list with
            display_name (str): The rendered name of the new list
            template (str): The name of the template used to create the list
            columns (iterable): column names to be stored in the ListItems in the list

        Returns:
            SiteList: newly created list instance
        """
        uri = 'sites/%s/lists'
        request_data = dict(displayName=display_name, list=dict(template=template), columns=columns)
        data = api.request(uri, json=request_data, method='POST')
        logger.info('Created new %s instance: %r', cls.__name__, display_name)
        return cls.from_api(data)


class ListItem(object):
    __slots__ = ('id', 'etag', 'content_type', 'parent_reference', 'name', 'description', 'fields', 'created_datetime', 'created_by', 'last_modified_datetime', 'last_modified_by', '_dirty_fields')

    def __init__(self, id, etag, content_type, parent_reference, name, description, fields, created_datetime, created_by, last_modified_datetime, last_modified_by):
        self.id = id
        self.etag = etag
        self.content_type = content_type
        self.parent_reference = parent_reference
        self.name = name
        self.description = description
        self.fields = fields
        self.created_datetime = created_datetime
        self.created_by = created_by
        self.last_modified_datetime = last_modified_datetime
        self.last_modified_by = last_modified_by
        self._dirty_fields = dict()

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<%s %s id=%r, createdAt=%s, lastModified=%s>' % (self.__class__.__name__, id(self), self.id, self.created_datetime, self.last_modified_datetime)

    def __setitem__(self, key, value):
        self.fields[key] = value
        self._dirty_fields[key] = value

    def __getitem__(self, key):
        return self.fields[key]

    def __contains__(self, item):
        return item in self.fields

    def keys(self):
        return self.fields.keys()

    def update(self, api, site, list_instance, **kwargs):
        """
        Updates the ListItem in the Microsoft Graph instance

        Parameters:
            api (msgraph.api.GraphAPI):  The endpoint from which to save data
            site (Site|str): The SharePoint site (or site ID of the Site) the ListItem is associated with
            list_instance (SiteList|str):  The SiteList (or list ID) the ListItem is associated with

        Keyword Arguments:
            readonly_fields (iterable):  Read-only fields in the ListItem fields dictionary

        Returns:
            None
        """

        uri = 'sites/%s/lists/%s/items/%s' % (site, list_instance, self.id)
        headers = dict()
        if kwargs.get('if_match', True):
            headers['if-match'] = self.etag
        data = dict(eTag=self.etag, name=self.name, description=self.description, parentReference=self.parent_reference)
        api.request(uri, json=data, headers=headers, method='PATCH')
        logger.info('Updated %s instance: %r', self.__class__.__name__, self.name)

    def update_fields(self, api, site, list_instance, **kwargs):
        """
        Updates the ListItem fields in the Microsoft Graph instance

        Parameters:
            api (msgraph.api.GraphAPI):  The endpoint from which to save data
            site (Site|str): The SharePoint site (or site ID of the Site) the ListItem is associated with
            list_instance (SiteList|str):  The SiteList (or list ID) the ListItem is associated with

        Returns:
            None
        """
        fields = kwargs.get('fields')
        if not fields:
            fields = self._dirty_fields
        uri = 'sites/%s/lists/%s/items/%s/fields' % (site, list_instance, self.id)
        data = api.request(uri, json=fields, method='PATCH')
        self.fields.update(data)
        self._dirty_fields = dict()
        logger.info('Updated %i fields of %r instance %r', len(fields), self.__class__.__name__, self.name)

    def delete(self, api, site, list_instance):
        """
        Deletes the ListItem fields from the Microsoft Graph instance

        Parameters:
            api (msgraph.api.GraphAPI):  The endpoint from which to delete the instance
            site (Site|str): The SharePoint site (or site ID of the Site) the ListItem is associated with
            list_instance (SiteList|str):  The SiteList (or list ID) the ListItem is associated with

        Returns:
            None
        """
        uri = 'sites/%s/lists/%s/items/%s' % (site, list_instance, self.id)
        api.request(uri, method='DELETE')
        logger.info('Deleted %s instance %s of from SiteList %r', self.__class__.__name__, self.name, list_instance)

    def versions(self, api, site, list_instance, **kwargs):
        """
        Fetches previous versions of the ListItem from the Microsoft Graph instance

        Parameters:
            api (msgraph.api.GraphAPI):  The endpoint from which to fetch data
            site (Site|str): The SharePoint site (or site ID of the Site) the ListItem is associated with
            list_instance (SiteList|str):  The SiteList (or list ID) the ListItem is associated with

        Returns:
            tuple: A sequentially ordered list of previous ListItem versions of the current ListItem
        """
        uri = 'sites/%s/lists/%s/items/%s/versions' % (site, list_instance, self.id)
        data = api.request(uri)
        instances = [self.__class__.from_api(item) for item in data.get('value', [])]
        sorted_instances = sorted(instances, key=lambda instance: instance.id)
        return tuple(sorted_instances)

    @classmethod
    def from_api(cls, data):
        id = data['id']
        etag = data.get('eTag')
        content_type = data.get('content_type')
        parent_reference = data.get('parentReference')
        name = data.get('name')
        description = data.get('description')
        fields = data['fields']
        created_datetime = data.get('createdDateTime')
        created_by = data.get('createdBy')
        last_modified_datetime = data.get('lastModifiedDateTime')
        last_modified_by = data.get('lastModifiedBy')
        return cls(id, etag, content_type, parent_reference, name, description, fields, created_datetime, created_by, last_modified_datetime, last_modified_by)

    @classmethod
    def get(cls, api, site, site_list, **kwargs):
        """
        Fetches ListItem instances from the Microsoft Graph instance

        Parameters:
            api (msgraph.api.GraphAPI):  The endpoint from which to fetch data
            site (Site|str): The SharePoint site (or site ID of the Site) the ListItems are associated with
            list_instance (SiteList|str):  The SiteList (or list ID) the ListItems are associated with

        Returns:
            list: The ListItem instances associated with the Site and List
        """
        uri = 'sites/%s/lists/%s/items' % (site, site_list)
        params = dict(expand='fields')
        data = api.request(uri, params=params)
        output = [cls.from_api(row) for row in data.get('value', [])]
        while data.get("@odata.nextLink"):
            uri = data.get("@odata.nextLink")
            data = api.request(uri)
            output += [cls.from_api(row) for row in data.get('value', [])]
        return output

    @classmethod
    def create(cls, api, site, list_instance, fields):
        """
        Creates a ListItem instance in the Microsoft Graph instance

        Parameters:
            api (msgraph.api.GraphAPI):  The endpoint at which to save data
            site (Site|str): The SharePoint site (or site ID of the Site) the ListItems are associated with
            list_instance (SiteList|str):  The SiteList (or list ID) the ListItems are associated with

        Keyword Arguments:
            fields (object): The fields to save in the ListItem instance

        Returns:
            ListItem: The newly created ListItem instance associated with the Site and List
        """
        uri = 'sites/%s/lists/%s/items' % (site, list_instance)
        request_data = dict(fields=fields)
        data = api.request(uri, json=request_data, method='POST')
        logger.info('Created new %s instance on SiteList %r', cls.__name__, list_instance)
        return cls.from_api(data)


class Analytics(object):
    __slots__ = ('all_time', 'last_seven_days')

    def __init__(self, all_time, last_seven_days):
        self.all_time = all_time
        self.last_seven_days = last_seven_days

    @classmethod
    def from_api(cls, data):
        all_time = data['allTime']
        last_seven_days = data['lastSevenDays']
        return cls(all_time, last_seven_days)

    @classmethod
    def by_site(cls, api, site, **kwargs):
        list_instance = kwargs.get('list_instance')
        item = kwargs.get('item')
        uri = 'sites/%s/analytics' % site
        if list_instance and item:
            uri = 'sites/%s/lists/%s/items/%s/analytics' % (site, list_instance, item)
        data = api.request(uri, method='GET')
        return cls.from_api(data)

    @classmethod
    def by_drive(cls, api, drive, item):
        uri = 'drives/%s/items/%s/analytics' % (drive, item)
        data = api.request(uri)
        return cls.from_api(data)
