import logging
from datetime import datetime


logger = logging.getLogger(__name__)

date_format = '%Y-%m-%d'
datetime_format = date_format + 'T%H:%M:%S'
full_datetime_format = date_format + 'T%H:%M:%S.%f'
extended_datetime_format = date_format + 'T%H:%M:%S.%fZ'


def parse_date_times(text):
    instance = None
    for format in [extended_datetime_format, full_datetime_format, datetime_format, date_format]:
        try:
            instance = datetime.strptime(text, format)
        except Exception:
            pass
        else:
            break
    return instance


class Calendar(object):
    __slots__ = ('id', 'name', 'owner', 'color', 'can_edit', 'can_share', 'can_view_private_items', 'change_key')

    def __init__(self, id, name, owner, color, can_edit, can_share, can_view_private_items, change_key):
        self.id = id
        self.name = name
        self.owner = owner
        self.color = color
        self.can_edit = can_edit
        self.can_share = can_share
        self.can_view_private_items = can_view_private_items
        self.change_key = change_key

    def __hash__(self):
        return hash((self.id))

    def __eq__(self, other):
        return isinstance(other, Calendar) and self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(self, other)

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<%s %s id=%r, name=%r, owner=%r, can_share=%r, can_edit=%r, can_view_private_items=%r>' % (self.__class__.__name__, id(self), self.id, self.name, self.owner, self.can_share, self.can_edit, self.can_view_private_items)

    def update(self, api, user=None):
        """
        Update the Calendar instance using the API endpoint

        Parameters:
            api (msgraph.api.GraphAPI):  The endpoint from which to fetch data
            uri (str, optional):  The delta link previously used
        """
        if user:
            uri = 'users/%s/calendars/%s' % self.id
        else:
            uri = 'me/calendars/%s' % self.id
        data = dict(name=self.name, color=self.color)
        data = api.request(uri, json=data, method='PATCH')
        logger.debug('Updated %r in %r', self, api)

    def delete(self, api, **kwargs):
        """
        Deletes the Calendar instance from the API endpoint

        Parameters:
            api (msgraph.api.GraphAPI):  The endpoint from which to fetch data

        Keyword Arguments:
            user (msgraph.user.User):  The User instance to delete the calendar from
        """
        user = kwargs.get('user')
        if user:
            uri = 'users/%s/calendarGroups/calendars/%s' % (user, self.id)
        else:
            uri = 'me/calendarGroups/calendars/%s' % self.id
        api.request(uri, method='DELETE')
        logger.debug('Deleted %r from %r', self, api)

    @classmethod
    def from_api(cls, data):
        id = data['id']
        name = data['name']
        owner = data['owner']
        color = data['color']
        can_edit = data['canEdit']
        can_share = data['canShare']
        can_view_private_items = data['canViewPrivateItems']
        change_key = data['changeKey']
        return cls(id, name, owner, color, can_edit, can_share, can_view_private_items, change_key)

    @classmethod
    def get(cls, api, **kwargs):
        """
        Fetch Calendar instances from the API endpoint

        Parameters:
            api (msgraph.api.GraphAPI):  The endpoint from which to fetch Calendar instances

        Keyword Arguments:
            user (msgraph.user.User):  The User instance to fetch the Calendar for
            group (Group):  The group for which to fetch the Calendar for
            page_size (int):  The number of items to include in each page, default: 100

        Returns:
            list: Calendar instances
        """
        user = kwargs.get('user')
        group = kwargs.get('group')
        if user:
            uri = 'users/%s/' % user
        else:
            uri = 'me/'

        if group:
            uri += 'calendarGroup/%s/calendars' % group
        else:
            uri += 'calendars'

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


class Location(object):
    __slots__ = ('display_name', 'location_type', 'unique_id', 'unique_id_type')

    def __init__(self, display_name, location_type, unique_id, unique_id_type):
        self.display_name = display_name
        self.location_type = location_type
        self.unique_id = unique_id
        self.unique_id_type = unique_id_type

    def __repr__(self):
        return '<%s %s display_name=%r, location_type=%r, unique_id_type=%r>' % (self.__class__.__name__, id(self), self.display_name, self.location_type, self.unique_id_type)

    def to_dict(self):
        return dict(displayName=self.display_name, locationType=self.location_type)

    @classmethod
    def from_api(cls, data):
        display_name = data['displayName']
        location_type = data['locationType']
        unique_id = data.get('uniqueId')
        unique_id_type = data['uniqueIdType']
        return cls(display_name, location_type, unique_id, unique_id_type)


class Attendee(object):
    __slots__ = ('name', 'email_address', 'type', 'status', 'response_time')

    def __init__(self, name, email_address, type, status, response_time):
        self.name = name
        self.email_address = email_address
        self.type = type
        self.status = status
        self.response_time = response_time

    def __repr__(self):
        return '<%s %s name=%r, email_address=%r, type=%r, status=%s, response_time=%s>' % (self.__class__.__name__, id(self), self.name, self.email_address, self.type, self.status, self.response_time)

    def to_dict(self):
        email_address = dict(name=self.name, emailAddress=self.address)
        status = dict(response=self.status, time=self.response_time)
        return dict(emailAddress=email_address, status=status, type=self.type)

    @classmethod
    def from_api(cls, data):
        email_data = data['emailAddress']
        name = email_data['name']
        email_address = email_data['address']
        type = data.get('type')
        status_data = data.get('status', dict())
        status = status_data.get('response')
        response_time = status_data.get('time')
        if response_time:
            response_time = parse_date_times(response_time)
        return cls(name, email_address, type, status, response_time)


class Category(object):
    __slots__ = ('id', 'display_name', 'color')

    def __init__(self, id, display_name, color):
        self.id = id
        self.display_name = display_name
        self.color = color

    def __hash__(self):
        return hash((self.id))

    def __eq__(self, other):
        return isinstance(other, Category) and self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(self, other)

    def __repr__(self):
        return '<%s %s id=%r, display_name=%r, color=%r' % (self.__class__.__name__, id(self), self.id, self.display_name, self.color)

    def update(self, api, user=None):
        """
        Update the Category at the API endpoint

        Parameters:
            api (msgraph.api.GraphAPI):  The endpoint at which to update the Category instance

        Keyword Parameters:
            user (msgraph.user.User):  The User instance for which to update the Category
        """
        if user:
            uri = 'users/%s/outlook/masterCategories/%s' % (user, self.id)
        else:
            uri = 'me/outlook/masterCategories/%s' % self.id
        data = dict(color=self.color)
        api.request(uri, json=data, method='PATCH')
        logger.debug('Updated %r in %r', self, api)

    def delete(self, api, user=None):
        """
        Delete the Category from the API endpoint

        Parameters:
            api (msgraph.api.GraphAPI):  The endpoint in which to delete the Category instance

        Keyword Parameters:
            user (msgraph.user.User):  The User instance from which to delete the Event from
        """
        if user:
            uri = 'users/%s/outlook/masterCategories/%s' % (user, self.id)
        else:
            uri = 'me/outlook/masterCategories/%s' % self.id
        api.request(uri, method='DELETE')
        logger.debug('Deleted %r from %r', self, api)

    @classmethod
    def from_api(cls, data):
        id = data['id']
        display_name = data['displayName']
        color = data['color']
        return cls(id, display_name, color)

    @classmethod
    def get(cls, api, user=None, **kwargs):
        """
        Fetch the Categories from the API endpoint

        Parameters:
            api (msgraph.api.GraphAPI):  The endpoint from which to fetch Category instances from
            user (msgraph.user.User):  The User instance to fetch the Category from

        Keyword Arguments:
            page_size (int):  The number of items to include in each page, default: 100

        Returns:
            list: Category instances
        """
        if user:
            uri = 'users/%s/output/masterCategories'
        else:
            uri = 'me/outlook/masterCategories'

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
    def create(cls, api, display_name, color, **kwargs):
        """
        Create a Category in the specified API endpoint

        Parameters:
            api (msgraph.api.GraphAPI):  The endpoint in which to create the Category instance
            display_name (str):  The display name for the Category instance
            color (str): The color to assign to the Category

        Keyword Arguments:
            user (msgraph.user.User):  The User instance to create the Category for

        Returns:
            Category: created Category instance
        """
        user = kwargs.get('user')
        if user:
            uri = 'users/%s/outlook/masterCategories'
        else:
            uri = 'me/outlook/masterCategories'
        data = dict(displayName=display_name, color=color)
        data = api.request(uri, data=data, method='POST')
        instance = cls.from_api(data)
        logger.debug('Created %r with %r', instance, api)
        return instance


class Range(object):
    __slots__ = ('type', 'start_date', 'end_date')

    def __init__(self, type, start_date, end_date):
        self.type = type
        self.start_date = start_date
        self.end_date = end_date

    def __repr__(self):
        return '<%s %s type=%r start_date=%r, end_date=%r>' % (self.__class__.__name__, id(self), self.type, self.start_date, self.end_date)

    def to_dict(self):
        start_date = self.start_date.strftime(date_format)
        end_date = self.end_date.strftime(date_format)
        return dict(type=type, startDate=start_date, endDate=end_date)

    @classmethod
    def from_api(cls, data):
        type = data['type']
        start_date = parse_date_times(data['startDate'])
        end_date = parse_date_times(data['endDate'])
        return cls(type, start_date, end_date)


class DateTime(object):
    __slots__ = ('date_time', 'time_zone')

    def __init__(self, date_time, time_zone):
        self.date_time = date_time
        self.time_zone = time_zone

    def __repr__(self):
        return '<%s %s date_time=%r, time_zone=%r>' % (self.__class__.__name__, id(self), self.date_time, self.time_zone)

    def to_dict(self):
        date_time = self.date_time.strftime(datetime_format)
        time_zone = self.time_zone
        return dict(dateTime=date_time, timeZone=time_zone)

    @classmethod
    def from_api(cls, data):
        date_time = data['dateTime']
        date_time = parse_date_times(date_time[:26])
        time_zone = data['timeZone']
        return cls(date_time, time_zone)


class Event(object):
    __slots__ = ('id', 'ical_uid', 'series_master_id', 'type', 'categories', 'subject', 'body', 'body_preview', 'attendees', 'locations', 'location', 'start', 'original_start', 'original_start_time_zone', 'end', 'original_end', 'original_end_time_zone', 'is_all_day', 'is_cancelled', 'is_reminder_on', 'is_organizer', 'organizer', 'importance', 'sensitivity', 'recurrence', 'response_requested', 'response_status', 'reminder_minutes_before_start', 'show_as', 'online_meeting_url', 'web_link', 'has_attachments', 'attachments', 'calendar', 'extensions', 'instances', 'multi_value_extended_properties', 'single_value_extended_properties', 'created_at', 'last_modified', 'removed')

    def __init__(self, id, ical_uid, series_master_id, type, categories, subject, body, body_preview, attendees, locations, location, start, original_start, original_start_time_zone, end, original_end, original_end_time_zone, is_all_day, is_cancelled, is_reminder_on, is_organizer, organizer, importance, sensitivity, recurrence, response_requested, response_status, reminder_minutes_before_start, show_as, online_meeting_url, web_link, has_attachments, attachments, calendar, extensions, instances, multi_value_extended_properties, single_value_extended_properties, created_at, last_modified, removed):
        self.id = id
        self.ical_uid = ical_uid
        self.series_master_id = series_master_id
        self.type = type
        self.categories = categories
        self.subject = subject
        self.body = body
        self.body_preview = body_preview
        self.attendees = attendees
        self.locations = locations
        self.location = location
        self.start = start
        self.original_start = original_start
        self.original_start_time_zone = original_start_time_zone
        self.end = end
        self.original_end = original_end
        self.original_end_time_zone = original_end_time_zone
        self.is_all_day = is_all_day
        self.is_cancelled = is_cancelled
        self.is_reminder_on = is_reminder_on
        self.is_organizer = is_organizer
        self.organizer = organizer
        self.importance = importance
        self.sensitivity = sensitivity
        self.recurrence = recurrence
        self.response_requested = response_requested
        self.response_status = response_status
        self.reminder_minutes_before_start = reminder_minutes_before_start
        self.show_as = show_as
        self.online_meeting_url = online_meeting_url
        self.web_link = web_link
        self.has_attachments = has_attachments
        self.attachments = attachments
        self.calendar = calendar
        self.extensions = extensions
        self.instances = instances
        self.multi_value_extended_properties = multi_value_extended_properties
        self.single_value_extended_properties = single_value_extended_properties
        self.created_at = created_at
        self.last_modified = last_modified
        self.removed = removed

    def __hash__(self):
        return hash((self.id))

    def __eq__(self, other):
        return isinstance(other, Event) and self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(self, other)

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<%s %s id=%r, subject=%r, body_preview=%r, start=%r, end=%r>' % (self.__class__.__name__, id(self), self.id, self.subject, self.body_preview, self.start, self.end)

    def update(self, api, **kwargs):
        """
        Update the Event at the API endpoint

        Parameters:
            api (msgraph.api.GraphAPI):  The endpoint in which to create the Event instance

        Keyword Parameters:
            user (msgraph.user.User):  The User instance from which to delete the Event from
            group (Group):  The Group from which to delete the Event from
            calendar (Calendar):  The Calendar from which delete the Event from
            me (bool):  Update the logged in user not, defaults to False
        """
        calendar = kwargs.get('calendar')
        user = kwargs.get('user')
        group = kwargs.get('group')
        me = kwargs.get('me', False)
        if group and not user and not me:
            uri = 'group/%s/events/%s' % (group, self.id)
        elif user and not me:
            if group:
                uri = 'users/%s/calendargroups/%s/events/%s' % (user, group, self.id)
            elif not group and calendar:
                uri = 'users/%s/calendars/%s/events/%s' % (user, calendar, self.id)
            elif group and calendar:
                uri = 'users/%s/calendargroups/%s/calendars/%s/events/%s' % (user, group, calendar, self.id)
            else:
                uri = 'users/%s/events/%s' % (user, self.id)
        else:
            if calendar and not group:
                uri = 'me/calendars/%s/events/%s' % (calendar, self.id)
            elif calendar and group:
                uri = 'me/calendargroup/%scalendars/%s/events/%s' % (group, calendar, self.id)
            else:
                uri = 'me/events/%s' % self.id

        locations = [location.to_dict() for location in self.locations]
        attendees = [attendee.to_dict() for attendee in self.attendees]
        start = self.start.to_dict()
        end = self.end.to_dict()
        data = dict(body=self.body, categories=self.categories, end=end, importance=self.importance, isAllDay=self.is_all_day, isReminderOn=self.is_reminder_on, location=self.location.to_dict(), locations=locations, reminderMinutesBeforeStart=self.reminder_minutes_before_start, responseRequested=self.response_requested, sensitivity=self.sensitivity, showAs=self.show_as, start=start, subject=self.subject, attendees=attendees)
        if self.recurrence:
            recurrence = dict(**self.recurrence)
            recurrence['range'] = recurrence['range'].to_dict()
            data['recurrence'] = recurrence
        api.request(uri, json=data, method='PATCH')
        logger.debug('Updated %r in %r', self, api)

    def delete(self, api, **kwargs):
        """
        Delete the Event from the API endpoint

        Parameters:
            api (msgraph.api.GraphAPI):  The endpoint in which to create the Event instance

        Keyword Parameters:
            user (msgraph.user.User):  The User instance from which to delete the Event from
            group (Group):  The Group from which to delete the Event from
            calendar (Calendar):  The Calendar from which delete the Event from
            me (bool):  Delete the Event from the current user, defaults to False
        """
        calendar = kwargs.get('calendar')
        user = kwargs.get('user')
        group = kwargs.get('group')
        me = kwargs.get('me', False)
        if group and not user and not me:
            uri = 'group/%s/events/%s' % (group, self.id)
        elif user and not me:
            if group:
                uri = 'users/%s/calendargroups/%s/events/%s' % (user, group, self.id)
            elif not group and calendar:
                uri = 'users/%s/calendars/%s/events/%s' % (user, calendar, self.id)
            elif group and calendar:
                uri = 'users/%s/calendargroups/%s/calendars/%s/events/%s' % (user, group, calendar, self.id)
        else:
            if calendar and not group:
                uri = 'me/calendars/%s/events/%s' % (calendar, self.id)
            elif calendar and group:
                uri = 'me/calendargroup/%scalendars/%s/events/%s' % (group, calendar, self.id)
            else:
                uri = 'me/events/%s' % self.id

        api.request(uri, method='DELETE')
        logger.debug('Deleted %r from %r', self, api)

    @classmethod
    def from_api(cls, data):
        id = data['id']
        ical_uid = data.get('ical_uid')
        series_master_id = data['seriesMasterId']
        type = data['type']
        categories = data.get('categories', [])
        subject = data['subject']
        body = data['body']
        body_preview = data['bodyPreview']
        attendees = [Attendee.from_api(row) for row in data['attendees']]
        locations = [Location.from_api(row) for row in data['locations']]
        location = Location.from_api(data['location'])
        start = DateTime.from_api(data['start'])
        original_start = data.get('originalStart')
        if original_start:
            original_start = parse_date_times(original_start[:26])
        original_start_time_zone = data.get('originalStartTimeZone')
        end = DateTime.from_api(data['end'])
        original_end = data.get('originalEnd')
        if original_end:
            original_end = parse_date_times(original_end[:26])
        original_end_time_zone = data.get('originalEndTimeZone')
        is_all_day = data['isAllDay']
        is_cancelled = data['isCancelled']
        is_reminder_on = data['isReminderOn']
        is_organizer = data['isOrganizer']
        organizer = Attendee.from_api(data['organizer'])
        importance = data['importance']
        sensitivity = data['sensitivity']
        recurrence = data['recurrence']
        if recurrence:
            recurrence_range = Range.from_api(recurrence['range'])
            recurrence['range'] = recurrence_range
        response_requested = data['responseRequested']
        response_status = data['responseStatus']
        reminder_minutes_before_start = data['reminderMinutesBeforeStart']
        show_as = data['showAs']
        online_meeting_url = data['onlineMeetingUrl']
        web_link = data['webLink']
        has_attachments = data['hasAttachments']
        attachments = data.get('attachments', [])
        calendar = data.get('calendar')
        extensions = data.get('extensions', [])
        instances = data.get('instances', [])
        multi_value_extended_properties = data.get('multiValueEextendedProperties', [])
        single_value_extended_properties = data.get('singleValueExtendedProperties', [])
        created_at = parse_date_times(data['createdDateTime'][:26])
        last_modified = parse_date_times(data['lastModifiedDateTime'][:26])
        removed = data.get('@removed')
        return cls(id, ical_uid, series_master_id, type, categories, subject, body, body_preview, attendees, locations, location, start, original_start, original_start_time_zone, end, original_end, original_end_time_zone, is_all_day, is_cancelled, is_reminder_on, is_organizer, organizer, importance, sensitivity, recurrence, response_requested, response_status, reminder_minutes_before_start, show_as, online_meeting_url, web_link, has_attachments, attachments, calendar, extensions, instances, multi_value_extended_properties, single_value_extended_properties, created_at, last_modified, removed)

    @classmethod
    def delta(cls, api, start, end, **kwargs):
        """
        Fetch the Events from the API endpoint

        Parameters:
            api (msgraph.api.GraphAPI):  The endpoint in which to create the Group instance
            start (datetime):  The lower bound of the datetime range
            end (datetime):  The upper bound of the datetime range

        Keyword Parameters:
            user (msgraph.user.User):  The User instance for which to fetch Events for
            group (Group):  The Group for which to fetch Events for
            calendar (Calendar):  The Calendar for which to fetch Events for
            page_size (int):  The number of items to include in each page, default: 100

        Returns:
            list: Event instances
        """
        fields = kwargs.get('fields', ['id', 'seriesMasterId', 'type', 'categories', 'subject', 'body', 'bodyPreview', 'attendees', 'locations', 'location', 'start', 'end', 'isAllDay', 'isCancelled', 'isReminderOn', 'isOrganizer', 'originalStart', 'originalStartTimeZone', 'originalEndTimeZone', 'organizer', 'importance', 'sensitivity', 'recurrence', 'responseRequested', 'responseStatus', 'reminderMinutesBeforeStart', 'showAs', 'onlineMeetingUrl', 'webLink', 'hasAttachments', 'attachments', 'calendar', 'extensions', 'instances', 'createdDateTime', 'lastModifiedDateTime'])
        user = kwargs.get('user')
        start_formatted = start.strftime(datetime_format)
        end_formatted = end.strftime(datetime_format)
        if user:
            uri = 'users/%s/calendarView/delta' % user
        else:
            uri = 'me/calendarView/delta'
        params = dict(startDateTime=start_formatted, endDateTime=end_formatted)
        params['$select'] = ','.join(fields)

        data = api.request(uri, params=params)

        output = [cls.from_api(row) for row in data.get('value', [])]
        while data.get("@odata.nextLink"):
            uri = data.get("@odata.nextLink")
            data = api.request(uri)
            output += [cls.from_api(row) for row in data.get('value', [])]
        delta_link = data['@odata.deltaLink']
        return output, delta_link

    @classmethod
    def get(cls, api, **kwargs):
        """
        Fetch the Events from the API endpoint

        Parameters:
            api (msgraph.api.GraphAPI):  The endpoint in which to create the Group instance

        Keyword Parameters:
            user (msgraph.user.User):  The User instance for which to fetch Events for
            group (Group):  The Group for which to fetch Events for
            calendar (Calendar):  The Calendar for which to fetch Events for
            page_size (int):  The number of items to include in each page, default: 100

        Returns:
            list: Event instances
        """
        fields = kwargs.get('fields', ['id', 'seriesMasterId', 'type', 'categories', 'subject', 'body', 'bodyPreview', 'attendees', 'locations', 'location', 'start', 'end', 'isAllDay', 'isCancelled', 'isReminderOn', 'isOrganizer', 'originalStart', 'originalStartTimeZone', 'originalEndTimeZone', 'organizer', 'importance', 'sensitivity', 'recurrence', 'responseRequested', 'responseStatus', 'reminderMinutesBeforeStart', 'showAs', 'onlineMeetingUrl', 'webLink', 'hasAttachments', 'attachments', 'calendar', 'extensions', 'instances', 'createdDateTime', 'lastModifiedDateTime'])
        raw_filters = kwargs.get('raw_filters', [])
        user = kwargs.get('user')
        group = kwargs.get('group')
        calendar = kwargs.get('calendar')

        start = kwargs.get('start')
        end = kwargs.get('end')

        if user:
            uri = 'users/%s/' % user
        else:
            uri = 'me/'

        if group:
            uri += 'calendargroups/%s/' % group

        if calendar:
            uri += 'calendars/%s/' % calendar
        uri += 'events'

        parameters = dict()
        parameters['$top'] = kwargs.get('page_size', 100)
        if start:
            parameters['startDateTime'] = start.isoformat()
        if end:
            parameters['endDateTime'] = end.isoformat()
        if raw_filters:
            parameters['$filter'] = ' and '.join(raw_filters)
        if fields:
            parameters['$select'] = ','.join(fields)

        data = api.request(uri, params=parameters)
        output = [cls.from_api(row) for row in data.get('value', [])]
        while data.get("@odata.nextLink"):
            uri = data.get("@odata.nextLink")
            data = api.request(uri)
            output += [cls.from_api(row) for row in data.get('value', [])]
        return output

    @classmethod
    def create(cls, api, subject, body, **kwargs):
        """
        Creates a new Event instance

        If a User is not specified, will create Event for the current User.

        Parameters:
            api (msgraph.api.GraphAPI): The API endpoint to create the new Event in
            subject (str): The subject of the new Event
            body (str):  The text body of the new Event

        Keyword Arguments:
            user (msgraph.user.User|str): The user instance or user ID to create the Event for
            calendar (Calendar):  The calendar to save the new Event to
            body_preview (str): Preview of the body contents
            attendees (list): Attendees of the Event
            locations (list)
            location (Location):
            start (DateTime): when the Event starts
            original_start (datetime):  Original start time of the Event
            original_start_time_zone (str):  Timezone of the original start time
            end (DateTime): When the Event ends
            original_end (datetime):  original end time
            original_end_time_zone (str):  Timezone of the original end time
            is_all_day (bool):  indicates if Event lasts full day
            is_cancelled (bool): indicates if Event is cancelled
            is_reminder_on (bool): indicates if Event has reminders
            is_organizer (bool): indicates if the User is the organizer
            organizer (Attendee):  The organizer of the meetings
            importance (str):  Indicates how important the Event is
            sensitivity (str):  Sensitivity of the Event.  Possible values are: normal, personal, private, confidential
            recurrence (dict): The recurrence pattern for the Event
            response_requested (bool):  Indicates if potential attendees need to respond
            response_status (object): Indicates the type of response sent in response to an event message.
            reminder_minutes_before_start (int): The number of minutes before the event start time that the reminder alert occurs.
            show_as (str):  The status to show for the User during the Event
        """
        user = kwargs.pop('user', None)
        calendar = kwargs.pop('calendar', None)
        data = dict()

        kwargs.setdefault('isReminderOn', False)
        kwargs.setdefault('isCancelled', False)
        kwargs.setdefault('importance', 'normal')
        location = kwargs.pop('location', None)
        locations = kwargs.pop('locations', [])
        attendees = kwargs.pop('attendees', [])
        start = kwargs.pop('start', None)

        if start:
            if isinstance(start, DateTime):
                start = start.to_dict()
            data['start'] = start
        end = kwargs.pop('end', None)
        if end:
            if isinstance(end, DateTime):
                end = end.to_dict()
            data['end'] = end
        data.update(kwargs)
        if location:
            data['location'] = location.to_dict()
        data['locations'] = [location.to_dict() for location in locations]
        data['attendees'] = [attendee.to_dict() for attendee in attendees]
        data['subject'] = subject
        data['body'] = body
        if user:
            if calendar:
                uri = 'users/%s/calendar/%s/events' % (user, calendar)
            else:
                uri = 'users/%s/events' % user
        if not user:
            if calendar:
                uri += '/calendars/%s/events' % calendar
            else:
                uri = 'me/events'
        data = api.request(uri, json=data, method='POST')
        instance = cls.from_api(data)
        logger.debug('Creates %r in %r', instance, api)
        return instance


class Group(object):
    __slots__ = ('id', 'name', 'class_id', 'change_key')

    def __init__(self, id, name, class_id, change_key):
        self.id = id
        self.name = name
        self.class_id = class_id
        self.change_key

    def __hash__(self):
        return hash((self.id))

    def __eq__(self, other):
        return isinstance(other, Group) and self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(self, other)

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<%s %s id=%r, name=%r, class_id=%r, change_key=%r>' % (self.__class__.__name__, id(self), self.id, self.name, self.class_id, self.change_key)

    def update(self, api, **kwargs):
        """
        Update the Group at the API endpoint

        Parameters:
            api (msgraph.api.GraphAPI):  The endpoint in which to create the Group instance

        Keyword Parameters:
            user (msgraph.user.User):  The User instance to create the Group for
        """
        user = kwargs.get('user')
        if user:
            uri = '/users/%s/calendarGroups/%s' % (user, self.id)
        else:
            uri = 'me/calendarGroups/%s' % self.id
        api.request(uri, method='PATCH')
        logger.debug('Updated %r in %r', self, api)

    def delete(self, api, **kwargs):
        """
        Delete the Group from the API endpoint

        Parameters:
            api (msgraph.api.GraphAPI):  The endpoint in which to create the Group instance

        Keyword Parameters:
            user (msgraph.user.User):  The User instance to create the Group for
        """
        user = kwargs.get('user')
        if user:
            uri = '/users/%s/calendarGroups/%s' % (user, self.id)
        else:
            uri = 'me/calendarGroups/%s' % self.id
        api.request(uri, method='DELETE')
        logger.debug('Deleted %r in %r', self, api)

    @classmethod
    def get(cls, api, user=None, **kwargs):
        """
        Fetch the Groups from the API endpoint

        Parameters:
            api (msgraph.api.GraphAPI):  The endpoint in which to create the Group instance
            user (msgraph.user.User):  The User instance to create the Group for

        Keyword Arguments:
            page_size (int):  The number of items to include in each page, default: 100

        Returns:
            list:  Group instances
        """
        if user:
            uri = 'users/%s/calendarGroups' % user
        else:
            uri = 'me/calendarGroups'

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
    def create(cls, api, name, class_id, change_key, **kwargs):
        """
        Create a Group in the specified API endpoint

        Parameters:
            api (msgraph.api.GraphAPI):  The endpoint in which to create the Group instance
            name (str):  The name of the Group
            class_id (str): The class identifier
            change_key (str): Identifies the version of the calendar group.

        Keyword Arguments:
            user (msgraph.user.User):  The User instance to create the Group for

        Returns:
            Group: created Group instance
        """
        user = kwargs.get('user')
        if user:
            uri = '/users/%r/calendarGroups'
        else:
            uri = 'me/calendarGroups'
        data = api.request(uri)
        instance = cls.from_api(data)
        logger.debug('Created %r in %r', instance, api)
        return instance


class Attachment(object):
    """
    Attachment instance representing a file attachment to an Event

    Attributes:
        id (str):  The unique identifier of the attachment
        name (str):  The name of the attachment
        is_inline (bool): Indicates if the file is inline the event  body
        size (int):  The size in bytes of the attachment
        content_id (str):  The ID of the attachment in the Exchange store.
        content_type (str): The content type of the attachment
        content_bytes (str):  The content of the attachment
        last_modified_datetime (datetime): When the attachment was last modified
    """
    __slots__ = ('id', 'name', 'is_inline', 'size', 'last_modified_datetime')

    def __init__(self, id, name, is_inline, size, last_modified_datetime):
        self.id = id
        self.name = name
        self.is_inline = is_inline
        self.size = size
        self.last_modified_datetime = last_modified_datetime

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<%s %s id=%r, name=%r, is_inline=%s, size=%r, last_modified_datetime=%r>' % (self.__class__.__name__, id(self), self.id, self.name, self.is_inline, self.size, self.last_modified_datetime)

    @classmethod
    def from_api(self, data):
        id = data['id']
        name = data['name']
        is_inline = data['isInline']
        size = data['size']
        raw_last_modified_datetime = data['lastModifiedDateTime']
        if raw_last_modified_datetime:
            last_modified_datetime = datetime.strptime(raw_last_modified_datetime[:-1], datetime_format)
        return cls(id, name, is_inline, size, content_id, content_type, content_location, content_bytes, last_modified_datetime)

    @classmethod
    def get(cls, api, event, **kwargs):
        """
        Fetch the Attachments for an Event

        Parameters:
            api (msgraph.api.GraphAPI):  The endpoint in which to create the Group instance
            event (Event):  The Event instance to fetch Attachments for

        Keyword Arguments:
            user (msgraph.user.User):  The User instance to fetch the Attachment for
            page_size (int):  The number of items to include in each page, default: 100

        Returns:
            list:  Attachments instances
        """
        user = kwargs.get('user')
        if user:
            uri = 'users/%s/events/%s/attachments' % (user, event)
        else:
            uri = 'me/events/%s/attachments' % event
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
    def create(cls, api, event, name, content, type, **kwargs):
        """
        Create an Attachment attached to an Event

        Parameters:
            api (msgraph.api.GraphAPI):  The endpoint in which to create the Attachment instance
            event (Event):   The Event to attach the Attachment to
            name (str):  The name of the Attachment
            content (str): The content of tha Attachment

        Keyword Arguments:
            user (msgraph.user.User):  The User instance to create the Attachment for
            group (Group): The Group instance to create the Attachment for
            calendar (Calendar): The Calendar instance to create the Attachment for

        Returns:
            Attachment: created Attachment instance
        """
        user = kwargs.get('user')
        group = kwargs.get('group')
        calendar = kwargs.get('calendar')

        if user:
            uri = 'users/%s/' % user
        else:
            uri = 'me/'

        if group:
            uri += 'calendargroups/%s/' % group

        if calendar:
            uri += 'calendars/%s/' % calendar

        uri += 'events/%s/attachments' % event
        data = {
            "@odata.type": type,
            "name": name,
            "contentBytes": content
        }
        results = api.request(uri, json=data, method='POST')
        instance = cls.from_api(results)
        logger.debug('Created %r in %r', instance, api)
        return instance


class FileAttachment(Attachment):
    __slots__ = ('id', 'name', 'is_inline', 'size', 'content_id', 'content_type', 'content_location', 'content_bytes', 'last_modified_datetime')

    def __init__(self, id, name, is_inline, size, content_id, content_type, content_location, content_bytes, last_modified_datetime):
        self.id = id
        self.name = name
        self.is_inline = is_inline
        self.size = size
        self.content_id = content_id
        self.content_type = content_type
        self.content_location = content_location
        self.content_bytes = content_bytes
        self.last_modified_datetime = last_modified_datetime

    def __repr__(self):
        return '<%s %s id=%r, name=%r, is_inline=%s, size=%r, content_id=%r, content_type=%r, last_modified_datetime=%r>' % (self.__class__.__name__, id(self), self.id, self.name, self.is_inline, self.size, self.content_id, self.content_type, self.last_modified_datetime)

    @classmethod
    def from_api(cls, data):
        id = data['id']
        name = data['name']
        is_inline = data['isInline']
        size = data['size']
        raw_last_modified_datetime = data['lastModifiedDateTime']
        content_id = data['contentId']
        content_type = data['contentType']
        content_location = data['contentLocation']
        content_bytes = data['contentBytes']
        if raw_last_modified_datetime:
            last_modified_datetime = datetime.strptime(raw_last_modified_datetime[:-1], datetime_format)
        return cls(id, name, is_inline, size, content_id, content_type, content_location, content_bytes, last_modified_datetime)

    @classmethod
    def create(cls, api, event, name, content, **kwargs):
        """
        Create the FileAttachment attached to an Event

        Parameters:
            api (msgraph.api.GraphAPI):  The endpoint in which to create the FileAttachment instance
            event (Event):   The Event to attach the FileAttachment to
            name (str):  The name of the FileAttachment
            content (str): The content of tha FileAttachment

        Keyword Arguments:
            user (msgraph.user.User):  The User instance to create the FileAttachment for
            group (Group): The Group instance to create the FileAttachment for
            calendar (Calendar): The Calendar instance to create the FileAttachment for

        Returns:
            FileAttachment: created FileAttachment instance
        """
        data_type = "#microsoft.graph.fileAttachment"
        instance = super(FileAttachment, cls).create(api, event, name, content, data_type, **kwargs)
        return instance
