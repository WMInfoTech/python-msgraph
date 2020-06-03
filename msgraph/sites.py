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
        return '<%s %s id=%s, name=%r, display_name=%r, created_datetime=%s>' % (self.__class__.__name__, id(self), self.id, self.name, self.display_name, self.created_datetime)

    def subsites(self, api, **kwargs):
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
        site_id = kwargs.get('id')

        if site_id:
            uri = 'sites/%s' % site_id
        else:
            uri = 'sites/root'
        data = api.request(uri)
        return cls.from_api(data)

    @classmethod
    def by_group(cls, api, group):
        uri = 'groups/%s/sites/root' % group
        data = api.request(uri)
        return cls.from_api(data)

    @classmethod
    def search(cls, api, query):
        params = {
            '$search': query
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
        list_id = kwargs.pop('id', None)
        uri = 'sites/%s/lists' % site
        if list_id:
            uri += '/%s' % list_id

        params = {
            '$top': kwargs.get('page_size', 100)
        }

        data = api.request(uri, params=params)
        if list_id:
            return cls.from_api(data)
        output = [cls.from_api(row) for row in data.get('value', [])]
        while data.get("@odata.nextLink"):
            uri = data.get("@odata.nextLink")
            data = api.request(uri)
            output += [cls.from_api(row) for row in data.get('value', [])]
        return output

    @classmethod
    def create(cls, api, site, display_name, template, columns):
        request_data = dict(displayName=display_name, list=dict(template=template), columns=columns)
        uri = 'sites/%s/lists'
        data = api.request(uri, json=request_data, method='POST')
        return cls.from_api(data)


class ListItem(object):
    __slots__ = ('id', 'etag', 'content_type', 'parent_reference', 'name', 'description', 'fields', 'created_datetime', 'created_by', 'last_modified_datetime', 'last_modified_by')

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

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<%s %s id=%r, createdAt=%s, lastModified=%r>' % (self.__class__.__name__, id(self), self.id, self.created_datetime, self.last_modified_datetime)

    def __setitem__(self, key, value):
        self.fields[key] = value

    def __getitem__(self, key):
        return self.fields[key]

    def keys(self):
        return self.fields.keys()

    def update(self, api, site, list_instance):
        uri = 'sites/%s/lists/%s/items/%s' % (site, list_instance, self.id)
        api.request(uri, json=self.fields, method='PATCH')

    def delete(self, api, site, list_instance):
        uri = 'sites/%s/lists/%s/items/%s' % (site, list_instance, self.id)
        api.request(uri, method='DELETE')

    def versions(self, api, site, list_instance, **kwargs):
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
    def create(cls, api, site, list_instance, **kwargs):
        uri = 'sites/%s/lists/%s/items' % (site, list_instance)
        request_data = dict(fields=kwargs)
        data = api.request(uri, json=request_data, method='POST')
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
