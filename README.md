# Microsoft Graph
`msgraph` is a Python wrapper of the [Microsoft Graph](https://developer.microsoft.com/en-us/graph) API.


## Installation
To install the `msgraph` library use the following command:
```python
python -m pip install git+ssh://git@code.wm.edu/IT/software-systems/eispippackages/msgraph.git  
```

## Usage

### Authenticating against the API
The library currently support connecting to the API using an SSL certificate:
```python
from msgraph import api

authority_host_uri = 'https://login.microsoftonline.com'
tenant = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
resource_uri = 'https://graph.microsoft.com'
client_id = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
client_thumbprint = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
client_certificate = ''
api_instance = api.GraphAPI.from_certificate(authority_host_uri, tenant, resource_uri, client_id, client_certificate, client_thumbprint)
```

**NOTE**:  When a `client_certificate` is changed, the `client_thumbprint` and `client_id` values must also be changed


### Using the API to fetch Users
You can use the `msgraph.user` module to interact with `User` instances.  `User` instanced can be fetched using the `msgraph.user.User` class:
```python
from msgraph import user
all_users = user.User.get(api_instance)
```

To fetch a specific user, you can also include the user's `User Principal Name`, which is the user's email address:
```python
dpfens_instance = user.User.get(api_instance, user='dpfens@wm.edu')
```

### Calendars & Events

#### Fetch a User's Calendars
Now let's fetch the `Calendar`s of a particular user.  To interact with  a `Calendar`, `Event`, calendar `Group`, or  calendar `Category` instance, we will use the `msgraph.calendar` module:
```python
from msgraph import calendar

dpfens_calendars = calendar.Calendar.get(api_instance, user=dpfens_instance)
```

#### Fetch a User's Events from a given Calendar
Now let's fetch the `Event` instances from the main calendar of `dpfens`:
```python
calendar_lookup = dict()
for calendar in dpfens_calendars:
    calendar_lookup[calendar.name] = calendar

primary_calendar = calendar_lookup['Calendar']
dpfens_events = calendar.Event.get(dpfens_instance, calendar=primary_calendar)
```

#### Update an Event
To update an `Event`, we can use the `Event.update` method:
```python
dpfens_event = dpfens_events[0]
dpfens_event.subject = 'Important meeting'
dpfens_event.update(api_instance)
```
Now the updates made to the `Event` object have been saved back to the `calendar` of `dpfens`.

#### Delete an Event from a Calendar
Let's try deleting an `Event` on a `Calendar` using the `Event.delete` method:
```python
dpfens_event = dpfens_events[0]
dpfens_event.delete(api_instance)
```
After calling the `delete` method, the `Event` has been removed from the `calendar` of `dpfens`.


### Sharepoint Sites & Lists

#### Search for a site
To fetch all sites matching a key phrase, use the `msgraph.sites.Site.search` method:
```python
from msgraph import sites

matching_sites = sites.Site.search(api_instance, 'software')
```

#### Fetching a specific site
Specific `msgraph.sites.Site` instances can be fetched using multiple methids:
*  `msgraph.sites.Site.get` method fetches sites by using the ID of the site
   ```python
   site_id = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
   site = sites.Site.get(api_instance, site=site_id)
   ```
*  `msgraph.sites.Site.by_relative_url` method to fetch by the host name and relative url of the SharePoint site
   ```python
   host_name = ''
   relative_url = ''
   site = sites.Site.by_relative_url(api_instance, host_name, relative_url)
   ```
*  `msgraph.sites.Site.by_group` method fetches the team site of a given group
    ```python
    group_id = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
    site = sites.Site.by_group(api_instance, group=group_id)
    ```

#### Traversing hierarchy of sites
SharePoint sites can have sub-sites within them.  To get the subsites of a Sharepoint site, use the `msgraph.sites.Site.subsites` method:
```python
subsites = site.subsites(api_instance)
```

To traverse the hierarchy of `msgraph.sites.Site` instances:
```python
def breadth_first(api, root):
    queue = [root]
    while queue:
        site = queue.pop(0)
        subsites = site.subsites(api)
        queue += subsites
    return queue


breadth_first_hierarchy = breadth_first(api_instance, site)


def depth_first(api, root):
    queue = [root]
    while queue:
        site = queue.pop()
        subsites = site.subsites(api)
        queue += subsites
    return queue


depth_first_hierarchy = breadth_first(api_instance, site)
```

#### Fetching Lists
`msgraph.sites.SiteList` instances can be fetched using the `msgraph.sites.SiteList.get` method:
```python
site_lists = sites.SiteList.get(api_instance, site)
```

Or, if you have the ID of the `msgraph.sites.SiteList`, you can specify it as a `list_instance` keyword argument to fetch the specific `msgraph.sites.SiteList` instance:
```python
list_id = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
site_list = sites.SiteList.get(api_instance, site, list_instance=list_id)
```

**NOTE**:  All `site` method parameters can be substituted with their IDs in the examples above.  So the code below would be valid:
```python
site_list = sites.SiteList.get(api_instance, site_id, list_instance=list_id)
```


#### Fetching ListItems for SiteLists
To fetch the `msgraph.sites.ListItem` instances for a `msgraph.sites.SiteList`, use the `msgraph.sites.ListItem.get` method:
```python
list_items = sites.ListItem.get(api_instance, site, site_list)
```

#### Fetching previous versions of ListItems
`msgraph.sites.ListItem` instances can be updated in Microsoft Graph.  To fetch the previous versions, use the `msgraph.sites.ListItem.versions` method:
```python
for item in list_items:
    previous_versions = item.versions(api_instance, site, site_list)
```

**NOTE**:  All `site` and `site_list` method parameters can be substituted with their IDs.  So the code below would be valid:
```python
list_items = sites.ListItem.get(api_instance, site_id, list_id)
for item in list_items:
    previous_versions = item.versions(api_instance, site_id, list_id)
```

#### Creating a ListItem
To create a new `msgraph.sites.ListItem` use the `msgraph.sites.ListItem.create` method:
```python
new_list_item_fields = dict(Title='Programmer')
new_list_item = sites.ListItem.create(api_instance, site, list, new_list_item_fields)
```

#### Updating a ListItem
To update the properties of a `msgraph.sites.ListItem` instance, use the `msgraph.sites.ListItem.update` method:
```python
for index, item in enumerate(list_items):
    item.name = '%s #%i' % (item.name, index)
    item.update(api_instance, site, site_list)
```

To update the fields of a `msgraph.sites.ListItem` instance, use the `msgraph.sites.ListItem.update_fields` method:
```python
for index, item in enumerate(list_items):
    item['Title'] = 'Assistant Executive ' + item['Title']
    item.update_fields(api_instance, site, site_list)
```

or alternatively:
```python
for index, item in enumerate(list_items):
    fields = dict(Title='Assistant Executive ' + item['Title'])
    item.update_fields(api_instance, site, site_list, fields=fields)
```

**NOTE**:  All `site` and `site_list` method parameters can be substituted with their IDs.  So the code below would be valid:
```python
for item in list_items:
    item['Title'] = 'Assistant Executive ' + item['Title']
    item.update_fields(api_instance, site_id, list_id)
```

#### Deleting a ListItem
To delete an existing `msgraph.sites.ListItem` instance, use the `msgraph.sites.ListItem.delete` method:
```python
new_list_item.delete(api_instance, site, site_list)
```

## Logging
The following modules have their own loggers:
*  `msgraph.api` - Used for logging error messages from the `API` and logging raw `HTTP` response content
*  `msgraph.calendar` - Used for logging the creation/update/deletes of `msgraph.calendar.Calendar`/`msgraph.calendar.Event`/`msgraph.calendar.msgraph.calendar.Group`/`msgraph.calendar.Category` instances
* `msgraph.group` - Used for logging the creation/update/deletes of `msgraph.group.Group` instances
* `msgraph.site` - Used for logging the creation/update/deletes of `msgraph.sites.Site` instances, `msgraph.sites.SiteList` instances, and `msgraph.sites.ListItem` instances
* `msgraph.user` - Used for logging the creation/update/deletes of `msgraph.user.User` instances
