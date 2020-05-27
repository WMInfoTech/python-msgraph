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

### Fetch a User's Calendars
Now let's fetch the `Calendar`s of a particular user.  To interact with  a `Calendar`, `Event`, calendar `Group`, or  calendar `Category` instance, we will use the `msgraph.calendar` module:
```python
from msgraph import calendar

dpfens_calendars = calendar.Calendar.get(api_instance, user=dpfens_instance)
```

### Fetch a User's Events from a given Calendar
Now let's fetch the `Event` instances from the main calendar of `dpfens`:
```python
calendar_lookup = dict()
for calendar in dpfens_calendars:
    calendar_lookup[calendar.name] = calendar

primary_calendar = calendar_lookup['Calendar']
dpfens_events = calendar.Event.get(dpfens_instance, calendar=primary_calendar)
```

### Update an Event
To update an `Event`, we can use the `Event.update` method:
```python
dpfens_event = dpfens_events[0]
dpfens_event.subject = 'Important meeting'
dpfens_event.update(api_instance)
```
Now the updates made to the `Event` object have been saved back to the `calendar` of `dpfens`.

### Delete an Event from a Calendar
Let's try deleting an `Event` on a `Calendar` using the `Event.delete` method:
```python
dpfens_event = dpfens_events[0]
dpfens_event.delete(api_instance)
```
After calling the `delete` method, the `Event` has been removed from the `calendar` of `dpfens`.


## Logging
The following modules have their own loggers:
*  `msgraph.api` - Used for logging error messages from the `API` and logging raw `HTTP` response content
*  `msgraph.calendar` - Used for logging the creation/update/deletes of `msgraph.calendar.Calendar`/`msgraph.calendar.Event`/`msgraph.calendar.msgraph.calendar.Group`/`msgraph.calendar.Category` instances
* `msgraph.group` - Used for logging the creation/update/deletes of `msgraph.group.Group` instances
* `msgraph.user` - Used for logging the creation/update/deletes of `msgraph.sites.Site` instances, `msgraph.sites.SiteList` instances, and `msgraph.sites.ListItem` instances
* `msgraph.user` - Used for logging the creation/update/deletes of `msgraph.user.User` instances
