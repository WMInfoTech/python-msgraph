import logging


logger = logging.getLogger(__name__)


class Drive(object):
    __slots__ = ('id', 'name', 'description', 'drive_type', 'root', 'owner', 'quote', 'sharepoint_ids', 'special', 'items', 'following', 'created_at', 'created_by', 'last_modified_at', 'last_modified_by')

    def __init__(self, id, name, description, drive_type, root, owner, quote, sharepoint_ids, special, items, following, created_at, created_by, last_modified_at, last_modified_by):
        self.id = id
        self.name = name
        self.description = description
        self.drive_type = drive_type
        self.root = root
        self.owner = owner
        self.quote = quote
        self.sharepoint_ids = sharepoint_ids
        self.special = special
        self.items = items
        self.following = following
        self.created_at = created_at
        self.created_by = created_by
        self.last_modified_at = last_modified_at
        self.last_modified_by = last_modified_by

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<%s %s id=%r, name=%r, drive_type=%r, description=%r>' % (self.__class__.__name__, id(self), self.id, self.name, self.drive_type, self.description)

    @classmethod
    def from_api(cls, data):
        id = data['id']
        name = data['name']
        description = data['description']
        drive_type = data['driveType']
        root = data.get('root')
        owner = data['owner']
        quote = data.get('quote')
        sharepoint_ids = data.get('sharepointIds', [])
        special = data.get('special')
        items = data.get('items')
        following = data.get('following')
        created_at = data.get('createdDateTime')
        created_by = data.get('createdBy')
        last_modified_at = data.get('lastModifiedDateTime')
        last_modified_by = data.get('lastModifiedBy')
        return cls(id, name, description, drive_type, root, owner, quote, sharepoint_ids, special, items, following, created_at, created_by, last_modified_at, last_modified_by)

    @classmethod
    def by_user(cls, api, **kwargs):
        user = kwargs.get('user')
        if user:
            uri = 'users/%s/drive' % user
        else:
            uri = 'me/drive'
        data = api.request(uri)
        return cls.from_api(data)

    @classmethod
    def by_site(cls, api, site):
        uri = 'sites/%s/drive' % site
        data = api.request(uri)
        return cls.from_api(data)

    @classmethod
    def get(cls, api, **kwargs):
        group = kwargs.get('group')
        site = kwargs.get('site')
        drive = kwargs.get('drive')
        user = kwargs.get('user')
        if drive:
            uri = 'drives/%s' % drive
        elif group:
            uri = 'groups/%s/drive' % group
        elif site:
            uri = 'sites/%s/drive' % site
        elif user:
            uri = 'users/%s/drive' % user
        else:
            uri = 'me/drive'
        data = api.request(uri)
        return cls.from_api(data)

        output = [cls.from_api(row) for row in data.get('value', [])]
        while data.get("@odata.nextLink"):
            uri = data.get("@odata.nextLink")
            data = api.request(uri)
            output += [cls.from_api(row) for row in data.get('value', [])]
        return output

    @classmethod
    def accessible(cls, api, **kwargs):
        """
        Drives accessible to a User, Site, or Group
        """
        group = kwargs.get('group')
        site = kwargs.get('site')
        drive = kwargs.get('drive')
        user = kwargs.get('user')
        if drive:
            uri = 'drives/%s' % drive
        elif group:
            uri = 'groups/%s/drives' % group
        elif site:
            uri = 'sites/%s/drives' % site
        elif user:
            uri = 'users/%s/drives' % user
        else:
            uri = 'me/drives'
        data = api.request(uri)
        output = [cls.from_api(row) for row in data.get('value', [])]
        while data.get("@odata.nextLink"):
            uri = data.get("@odata.nextLink")
            data = api.request(uri)
            output += [cls.from_api(row) for row in data.get('value', [])]
        return output


class DriveItem(object):
    __slots__ = ('id', 'name', 'description', 'etag', 'ctag', 'parent_reference', 'root', 'web_url', 'audio', 'content', 'file', 'file_system_info', 'folder', 'image', 'location', 'package', 'photo', 'publication', 'remote_item', 'search_result', 'shared', 'sharepoint_ids', 'size', 'special_folder', 'video', 'web_dav_url', 'activity', 'analytics', 'children', 'permissions', 'subscriptions', 'thumbnails', 'versions', 'created_by_user', 'last_modified_user', 'created_at', 'created_by', 'last_modified_at', 'last_modified_by')

    def __init__(self, id, name, description, etag, ctag, parent_reference, root, web_url, audio, content, file, file_system_info, folder, image, location, package, photo, publication, remote_item, search_result, shared, sharepoint_ids, size, special_folder, video, web_dav_url, activity, analytics, children, permissions, subscriptions, thumbnails, versions, created_by_user, last_modified_user, created_at, created_by, last_modified_at, last_modified_by):
        self.id = id
        self.name = name
        self.description = description
        self.etag = etag
        self.ctag = ctag
        self.parent_reference = parent_reference
        self.root = root
        self.web_url = web_url
        self.audio = audio
        self.content = content
        self.file = file
        self.file_system_info = file_system_info
        self.folder = folder
        self.image = image
        self.location = location
        self.package = package
        self.photo = photo
        self.publication = publication
        self.remote_item = remote_item
        self.search_result = search_result
        self.shared = shared
        self.sharepoint_ids = sharepoint_ids
        self.size = size
        self.special_folder = special_folder
        self.video = video
        self.web_dav_url = web_dav_url
        self.activity = activity
        self.analytics = analytics
        self.children = children
        self.permissions = permissions
        self.subscriptions = subscriptions
        self.thumbnails = thumbnails
        self.versions = versions
        self.created_by_user = created_by_user
        self.last_modified_user = last_modified_user
        self.created_at = created_at
        self.created_by = created_by
        self.last_modified_at = last_modified_at
        self.last_modified_by = last_modified_by

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<%s %s id=%r, name=%r, size=%s bytes>' % (self.__class__.__name__, id(self), self.id, self.name, self.size)

    def move(self, api, new_name, **kwargs):
        group = kwargs.get('group')
        site = kwargs.get('site')
        drive = kwargs.get('drive')
        user = kwargs.get('user')

        if drive:
            uri = 'drives/%s/items' % drive
        elif group:
            uri = 'groups/%s/drive/items' % group
        elif site:
            uri = 'sites/%s/drive/items' % site
        elif user:
            uri = 'users/%s/drive/items' % drive
        else:
            uri = 'me/drive/items'
        uri += '/%s' % self.id

        new_folder = kwargs.get('folder')
        patch_data = dict(name=new_name)
        if new_folder:
            new_folder_id = str(new_folder)
            patch_data['parentReference'] = dict(id=new_folder_id)
        else:
            patch_data['parentReference'] = self.parent_reference
        data = api.request(uri, json=patch_data, method='PATCH')
        logger.info('Moved file %r to %r as %r', self.name, patch_data['parentReference'], new_name)
        self.id = data['id']
        self.parent_reference = data['parentReference']
        self.name = data['name']

    def check_in(self, api, **kwargs):
        group = kwargs.get('group')
        site = kwargs.get('site')
        drive = kwargs.get('drive')
        user = kwargs.get('user')

        if drive:
            uri = 'drives/%s/items' % drive
        elif group:
            uri = 'groups/%s/drives/items' % group
        elif site:
            uri = 'sites/%s/drive/items' % site
        elif user:
            uri = 'users/%s/drive/items' % drive
        else:
            uri = 'me/drive/items'
        uri += '/%s/checkin' % self.id
        api.request(uri, method='POST')
        logger.info('Checked in %r', self.name)

    def check_out(self, api, **kwargs):
        group = kwargs.get('group')
        site = kwargs.get('site')
        drive = kwargs.get('drive')
        user = kwargs.get('user')

        if drive:
            uri = 'drives/%s/items' % drive
        elif group:
            uri = 'groups/%s/drives/items' % group
        elif site:
            uri = 'sites/%s/drive/items' % site
        elif user:
            uri = 'users/%s/drive/items' % user
        else:
            uri = 'me/drive/items'
        uri += '/%s/checkout' % self.id
        api.request(uri, method='POST')
        logger.info('Checked out %r', self.name)

    def all_children(self, api, **kwargs):
        group = kwargs.get('group')
        site = kwargs.get('site')
        drive = kwargs.get('drive')
        user = kwargs.get('user')

        if drive:
            uri = 'drives/%s' % drive
        elif group:
            uri = 'groups/%s/drive' % group
        elif site:
            uri = 'sites/%s/drive' % site
        elif user:
            uri = 'users/%s/drive' % user
        else:
            uri = 'me/drive'
        uri += '/items/%s/children' % self.id
        data = api.request(uri)

        output = [self.__class__.from_api(row) for row in data.get('value', [])]
        while data.get("@odata.nextLink"):
            uri = data.get("@odata.nextLink")
            data = api.request(uri)
            output += [self.__class__.from_api(row) for row in data.get('value', [])]
        return output

    def update(self, api, **kwargs):
        group = kwargs.get('group')
        site = kwargs.get('site')
        drive = kwargs.get('drive')
        user = kwargs.get('user')

        if drive:
            uri = 'drives/%s' % drive
        elif group:
            uri = 'groups/%s/drive' % group
        elif site:
            uri = 'sites/%s/drive' % site
        elif user:
            uri = 'users/%s/drive' % user
        else:
            uri = 'me/drive'
        uri += '/items/%s' % self.id
        data = dict(name=self.name, description=self.description, parentReference=self.parent_reference, webDavUrl=self.web_dav_url, fileSystemInfo=self.file_system_info)
        api.request(uri, json=data, method='PATCH')
        logger.info('Updated file %r', self.name)

    def delete(self, api, **kwargs):
        group = kwargs.get('group')
        site = kwargs.get('site')
        drive = kwargs.get('drive')
        user = kwargs.get('user')

        if drive:
            uri = 'drives/%s' % drive
        elif group:
            uri = 'groups/%s/drive' % group
        elif site:
            uri = 'sites/%s/drive' % site
        elif user:
            uri = 'users/%s/drive' % user
        else:
            uri = 'me/drive'
        uri += '/items/%s' % self.id
        api.request(uri, method='DELETE')
        logger.info('Deleted file %r from %r', self.name, uri)

    @classmethod
    def from_api(cls, data):
        id = data['id']
        name = data['name']
        description = data.get('description')
        etag = data.get('etag')
        ctag = data.get('cTag')
        parent_reference = data.get('parentReference')
        root = data.get('root')
        web_url = data.get('webUrl')
        audio = data.get('audio')
        content = data.get('content')
        file = data.get('file')
        file_system_info = data.get('fileSystemInfo')
        folder = data.get('folder')
        image = data.get('image')
        location = data.get('location')
        package = data.get('package')
        photo = data.get('photo')
        publication = data.get('publication')
        remote_item = data.get('remoteItem')
        search_result = data.get('searchResult')
        shared = data.get('shared')
        sharepoint_ids = data.get('sharepointIds')
        size = data['size']
        special_folder = data.get('specialFolder')
        video = data.get('video')
        web_dav_url = data.get('webDavUrl')
        activity = data.get('activity')
        analytics = data.get('analytics')
        children = data.get('children')
        permissions = data.get('permissions')
        subscriptions = data.get('subscriptions')
        thumbnails = data.get('thumbnails')
        versions = data.get('versions')
        created_by_user = data.get('createdByUser')
        last_modified_user = data.get('lastModifiedUser')
        created_at = data.get('createdDateTime')
        created_by = data.get('createdBy')
        last_modified_at = data.get('lastModifiedDateTime')
        last_modified_by = data.get('lastModifiedBy')
        return cls(id, name, description, etag, ctag, parent_reference, root, web_url, audio, content, file, file_system_info, folder, image, location, package, photo, publication, remote_item, search_result, shared, sharepoint_ids, size, special_folder, video, web_dav_url, activity, analytics, children, permissions, subscriptions, thumbnails, versions, created_by_user, last_modified_user, created_at, created_by, last_modified_at, last_modified_by)

    @classmethod
    def create_folder(cls, api, name, parent, **kwargs):
        group = kwargs.get('group')
        site = kwargs.get('site')
        drive = kwargs.get('drive')
        user = kwargs.get('user')

        if drive:
            uri = 'drives/%s' % drive
        elif group:
            uri = 'groups/%s/drive' % group
        elif site:
            uri = 'sites/%s/drive' % site
        elif user:
            uri = 'users/%s/drive' % user
        else:
            uri = 'me/drive'
        uri += '/items/%s/children' % parent
        post_data = {
            'name': name,
            'folder': dict(),
            '@microsoft.graph.conflictBehavior': kwargs.get('conflict_behavior', 'fail')
        }
        data = api.request(uri, json=post_data, method='POST')
        logger.info('Created new folder %r under', name, parent)
        return cls.from_api(data)

    @classmethod
    def upload(cls, api, content, **kwargs):
        group = kwargs.get('group')
        site = kwargs.get('site')
        drive = kwargs.get('drive')
        user = kwargs.get('user')

        replace = kwargs.get('replace')
        if drive:
            uri = 'drives/%s' % drive
        elif group:
            uri = 'groups/%s/drives' % group
        elif site:
            uri = 'sites/%s/drives' % site
        elif user:
            uri = 'users/%s/drives' % user
        else:
            uri = 'me/drive'

        if replace:
            item = kwargs.get('item')
            uri += '/items/%s/content' % item
        else:
            parent = kwargs.get('parent')
            file_name = kwargs.get('file_name')
            uri += '/items/%s:/%s:/content' % (parent, file_name)
        data = api.request(uri, data=content, content_type='text/plain', method='PUT')
        return cls.from_api(data)

    @classmethod
    def search(cls, api, query, **kwargs):
        """
        Searches the full hierarchy of items for items matching the query
        """
        group = kwargs.get('group')
        site = kwargs.get('site')
        drive = kwargs.get('drive')
        user = kwargs.get('user')

        if drive:
            uri = 'drives/%s' % drive
        elif group:
            uri = 'groups/%s/drive' % group
        elif site:
            uri = 'sites/%s/drive' % site
        elif user:
            uri = 'users/%s/drive' % user
        else:
            uri = 'me/drive'

        uri += "/root/search(q='%s')" % query
        data = api.request(uri)

        output = [cls.from_api(row) for row in data.get('value', [])]
        while data.get("@odata.nextLink"):
            uri = data.get("@odata.nextLink")
            data = api.request(uri)
            output += [cls.from_api(row) for row in data.get('value', [])]
        return output

    @classmethod
    def get_children(cls, api, **kwargs):
        group = kwargs.get('group')
        site = kwargs.get('site')
        drive = kwargs.get('drive')
        user = kwargs.get('user')

        if drive:
            uri = 'drives/%s' % drive
        elif group:
            uri = 'groups/%s/drive' % group
        elif site:
            uri = 'sites/%s/drive' % site
        elif user:
            uri = 'users/%s/drive' % user
        else:
            uri = 'me/drive'

        parent = kwargs.get('parent')
        path = kwargs.get('path')
        if parent:
            uri += '/items/%s/children' % parent
        elif path:
            uri += '/root:/%s:/children' % path
        else:
            uri += '/root/children'
        data = api.request(uri)
        output = [cls.from_api(row) for row in data.get('value', [])]
        while data.get("@odata.nextLink"):
            uri = data.get("@odata.nextLink")
            data = api.request(uri)
            output += [cls.from_api(row) for row in data.get('value', [])]
        return output

    @classmethod
    def root_folder(cls, api, **kwargs):
        group = kwargs.get('group')
        site = kwargs.get('site')
        drive = kwargs.get('drive')
        user = kwargs.get('user')

        if drive:
            uri = 'drives/%s' % drive
        elif group:
            uri = 'groups/%s/drive' % group
        elif site:
            uri = 'sites/%s/drive' % site
        elif user:
            uri = 'users/%s/drive' % user
        else:
            uri = 'me/drive'
        uri += '/root'
        data = api.request(uri)
        return cls.from_api(data)
