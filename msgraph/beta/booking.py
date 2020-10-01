import logging
from msgraph import base
from msgraph import calendar


logger = logging.getLogger(__name__)


class Appointment(base.Base):
    __slots__ = ('id', 'start', 'end', 'duration', 'customer_id', 'customer_name', 'customer_email_address', 'customer_location', 'customer_phone', 'customer_notes', 'service_id', 'service_name', 'service_location', 'service_notes', 'invoice_id', 'invoice_url', 'invoice_status', 'invoice_amount', 'invoice_date', 'prebuffer', 'postbuffer', 'price_type', 'price', 'price', 'price_type', 'reminders',  'staff_member_ids', 'opt_out_of_customer_email')

    def __init__(self, id, start, end, duration, customer_id, customer_name, customer_email_address, customer_location, customer_phone, customer_notes, service_id, service_name, service_location, service_notes, invoice_id, invoice_url, invoice_status, invoice_amount, invoice_date, prebuffer, postbuffer, price_type, price, reminders, staff_member_ids, opt_out_of_customer_email):
        self.id = id,
        self.start = start,
        self.end = end,
        self.duration = duration,
        self.customer_id = customer_id,
        self.customer_name = customer_name,
        self.customer_email_address = customer_email_address,
        self.customer_location = customer_location,
        self.customer_phone = customer_phone,
        self.customer_notes = customer_notes,
        self.service_id = service_id,
        self.service_name = service_name,
        self.service_location = service_location,
        self.service_notes = service_notes,
        self.invoice_id = invoice_id,
        self.invoice_url = invoice_url,
        self.invoice_status = invoice_status,
        self.invoice_amount = invoice_amount,
        self.invoice_date = invoice_date,
        self.prebuffer = prebuffer,
        self.postbuffer = postbuffer,
        self.price_type = price_type,
        self.price = price,
        self.reminders = reminders,
        self.staff_member_ids = staff_member_ids,
        self.opt_out_of_customer_email = opt_out_of_customer_email

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<%s %s id=%r, customer_name=%r, start=%r, end=%r>' % (self.__class__.__name__, id(self), self.id, self.customer_name, self.start, self.end)

    def cancel(self, api, business, cancellation_message):
        uri = 'bookingBusinesses/%s/appointments/%s/cancel' % (business, self.id)
        request_data = dict(cancellationMessage=cancellation_message)
        api.request(uri, json=request_data, method='POST')

    @classmethod
    def from_api(cls, data):
        id = data['id']
        start = data['start']
        if start:
            start = calendar.DateTime.from_api(start)

        end = data['end']
        if end:
            end = calendar.DateTime.from_api(end)
        duration = data['duration']
        customer_id = data['customerId']
        customer_name = data['customerName']
        customer_email_address = data['customerEmailAddress']
        customer_location = data['customerLocation']
        customer_phone = data['customerPhone']
        customer_notes = data['customerNotes']
        service_id = data['serviceId']
        service_name = data['serviceName']
        service_location = data['serviceLocation']
        service_notes = data['serviceNotes']
        invoice_id = data['invoiceId']
        invoice_url = data['invoiceUrl']
        invoice_status = data['invoiceStatus']
        invoice_amount = data['invoiceAmount']
        invoice_date = data['invoiceDate']
        prebuffer = data['preBuffer']
        postbuffer = data['postBuffer']
        price_type = data['priceType']
        price = data['price']
        reminders = data['reminders']
        staff_member_ids = data['staffMemberIds']
        opt_out_of_customer_email = data['optOutOfCustomerEmail']
        return cls(id, start, end, duration, customer_id, customer_name, customer_email_address, customer_location, customer_phone, customer_notes, service_id, service_name, service_location, service_notes, invoice_id, invoice_url, invoice_status, invoice_amount, invoice_date, prebuffer, postbuffer, price_type, price, reminders,  staff_member_ids, opt_out_of_customer_email)

    @classmethod
    def get(cls, api, business, **kwargs):
        appointment = kwargs.pop('appointment', None)
        if appointment:
            uri = 'bookingBusinesses/%s/appointments/%s' % (business, appointment)
            data = api.request(uri, version='beta')
            output = cls.from_api(data)
        else:
            uri = 'bookingBusinesses/%s/appointments' % business
            kwargs.setdefault('version', 'beta')
            data = api.request(uri, **kwargs)
            output = [cls.from_api(row) for row in data['value']]
        return output


class Business(base.Base):
    __slots__ = ('id', 'display_name', 'type', 'address', 'phone', 'email', 'is_published', 'business_hours', 'public_url', 'website_url', 'default_currency_iso', 'scheduling_policy')

    def __init__(self, id, display_name, type, address, phone, email, is_published, business_hours, public_url, website_url, default_currency_iso, scheduling_policy):
        self.id = id
        self.display_name = display_name
        self.type = type
        self.address = address
        self.phone = phone
        self.email = email
        self.is_published = is_published
        self.business_hours = business_hours
        self.public_url = public_url
        self.website_url = website_url
        self.default_currency_iso = default_currency_iso
        self.scheduling_policy = scheduling_policy

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<%s %s id=%r, display_name=%r>' % (self.__class__.__name__, id(self), self.id, self.display_name)

    def update(self, api, **kwargs):
        uri = 'bookingBusinesses/%s' % self.id
        kwargs.setdefault('version', 'beta')
        data = dict(displayName=self.display_name, businessType=self.type, email=self.email, phone=self.phone, address=self.address, webSiteUrl=self.website_url, businessHours=self.business_hours)
        api.request(uri, json=data, method='PATCH', **kwargs)

    def delete(self, api, **kwargs):
        uri = 'bookingBusinesses/%s' % self.id
        kwargs.setdefault('version', 'beta')
        api.request(uri, method='DELETE', **kwargs)

    def publish(self, api, **kwargs):
        uri = 'bookingBusinesses/%s/publish' % self.id
        kwargs.setdefault('version', 'beta')
        api.request(uri, method='POST', **kwargs)

    def unpublish(self, api, **kwargs):
        uri = 'bookingBusinesses/%s/unpublish' % self.id
        kwargs.setdefault('version', 'beta')
        api.request(uri, method='POST', **kwargs)

    @classmethod
    def from_api(cls, data):
        id = data['id']
        display_name = data['displayName']
        type = data.get('type')
        address = data.get('address')
        phone = data.get('phone')
        email = data.get('email')
        is_published = data.get('isPublished')
        business_hours = data.get('businessHours')
        public_url = data.get('publicUrl')
        website_url = data.get('websiteUrl')
        default_currency_iso = data.get('defaultCurrencyIso')
        scheduling_policy = data.get('schedulingPolicy')
        return cls(id, display_name, type, address, phone, email, is_published, business_hours, public_url, website_url, default_currency_iso, scheduling_policy)

    @classmethod
    def get(cls, api, **kwargs):
        kwargs.setdefault('version', 'beta')
        business = kwargs.pop('business', None)
        uri = 'bookingBusinesses'
        if business:
            uri = 'bookingBusinesses/%s' % business
            data = api.request(uri, **kwargs)
            output = cls.from_api(data)
        else:
            data = api.request(uri, **kwargs)
            output = [cls.from_api(item) for item in data.get('value', [])]
        return output


class Customer(base.Base):
    __slots__ = ('id', 'display_name', 'email_address')

    def __init__(self, id, display_name, email_address):
        self.id = id
        self.display_name = display_name
        self.email_address = email_address

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<%s %s id=%r, display_name=%r, email_address=%r>' % (self.__class__.__name__, id(self), self.id, self.display_name, self.email_address)

    def update(self, api, business, **kwargs):
        uri = 'bookingBusinesses/%s/customers/%r' % (business, self.id)
        request_data = dict(displayName=self.display_name, emailAddress=self.email_address)
        kwargs.setdefault('version', 'beta')
        data = api.request(uri, json=request_data, method='PATCH', **kwargs)
        instance = self.from_api(data)
        self.display_name = instance.display_name
        self.email_address = instance.email_address

    def delete(self, api, business, **kwargs):
        uri = 'bookingBusinesses/%s/customers/%r' % (business, self.id)
        kwargs.setdefault('version', 'beta')
        api.request(uri, method='DELETE', **kwargs)

    @classmethod
    def from_api(cls, data):
        id = data['id']
        display_name = data['displayName']
        email_address = data['emailAddress']
        return cls(id, display_name, email_address)

    @classmethod
    def get(cls, api, business, **kwargs):
        kwargs.setdefault('version', 'beta')
        customer = kwargs.pop('customer', None)
        if customer:
            uri = 'bookingBusinesses/%s/customers/%s' % (business, customer)
            data = api.request(uri, **kwargs)
            output = cls.from_api(data)
        else:
            uri = 'bookingBusinesses/%s/customers' % business
            params = dict(**kwargs)
            data = api.request(uri, params=params, **kwargs)
            output = [cls.from_api(row) for row in data['value']]
        return output

    @classmethod
    def create(cls, api, business, display_name, email_address, **kwargs):
        kwargs.setdefault('version', 'beta')
        uri = 'bookingBusinesses/%s/customers' % business
        request_data = dict(displayName=display_name, emailAddress=email_address)
        data = api.request(uri, json=request_data, method='POST', **kwargs)
        return cls.from_api(data)


class Service(base.Base):
    __slots__ = ('id', 'display_name', 'description', 'email_address', 'is_hidden_from_customers', 'notes', 'prebuffer', 'postbuffer', 'scheduling_policy', 'staff_member_ids', 'default_duration', 'default_location', 'default_price', 'default_price_type', 'default_reminders')

    def __init__(self, id, display_name, description, email_address, is_hidden_from_customers, notes, prebuffer, postbuffer, scheduling_policy, staff_member_ids, default_duration, default_location, default_price, default_price_type, default_reminders):
        self.id = id
        self.display_name = display_name
        self.description = description
        self.email_address = email_address
        self.is_hidden_from_customers = is_hidden_from_customers
        self.notes = notes
        self.prebuffer = prebuffer
        self.postbuffer = postbuffer
        self.scheduling_policy = scheduling_policy
        self.staff_member_ids = staff_member_ids
        self.default_duration = default_duration
        self.default_location = default_location
        self.default_price = default_price
        self.default_price_type = default_price_type
        self.default_reminders = default_reminders

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<%s %s id=%r, display_name=%r, email_address=%r, description=%r, is_hidden_from_customers=%r>' % (self.__class__.__name__, id(self), self.id, self.display_name, self.email_address, self.description, self.is_hidden_from_customers)

    def update(self, api, business, **kwargs):
        uri = 'bookingBusinesses/%s/services/%s' % (business, self.id)
        kwargs.setdefault('version', 'beta')
        data = dict(id=self.id, displayName=self.display_name, description=self.description, emailAddress=self.email_address, isHiddenFromCustomers=self.is_hidden_from_customers, notes=self.notes, preBuffer=self.prebufffer, postBuffer=self.postbuffer, schedulingPolicy=self.scheduling_policy, staffMemberIds=self.staff_member_ids, defaultDuration=self.default_duration, defaultLocation=self.default_location, defaultPrice=self.default_price, defaultPriceType=self.default_price_type, defaultReminders=self.default_reminders)
        api.request(uri, json=data, method='PATCH', **kwargs)

    def delete(self, api, business, **kwargs):
        uri = 'bookingBusinesses/%s/services/%s' % (business, self.id)
        kwargs.setdefault('version', 'beta')
        api.request(uri, method='DELETE', **kwargs)

    @classmethod
    def from_api(cls, data):
        print(data)
        id = data['id']
        display_name = data['displayName']
        description = data['description']
        email_address = data.get('emailAddress')
        is_hidden_from_customers = data['isHiddenFromCustomers']
        notes = data['notes']
        prebuffer = data['preBuffer']
        postbuffer = data['postBuffer']
        scheduling_policy = data['schedulingPolicy']
        staff_member_ids = data['staffMemberIds']
        default_duration = data['defaultDuration']
        default_location = data['defaultLocation']
        default_price = data['defaultPrice']
        default_price_type = data['defaultPriceType']
        default_reminders = data['defaultReminders']
        return cls(id, display_name, description, email_address, is_hidden_from_customers, notes, prebuffer, postbuffer, scheduling_policy, staff_member_ids, default_duration, default_location, default_price, default_price_type, default_reminders)

    @classmethod
    def get(cls, api, business, **kwargs):
        kwargs.setdefault('version', 'beta')
        service = kwargs.pop('service', None)
        if service:
            uri = 'bookingBusinesses/%s/services/%s' % (business, service)
            data = api.request(uri, **kwargs)
            output = cls.from_api(data)
        else:
            uri = 'bookingBusinesses/%s/services' % business
            params = dict(**kwargs)
            data = api.request(uri, params=params, **kwargs)
            output = [cls.from_api(row) for row in data['value']]
        return output


class StaffMember(base.Base):
    __slots__ = ('id', 'display_name', 'email_address', 'role', 'working_hours', 'use_business_hours', 'availability_is_affected_by_personal_calendar', 'color_index')

    def __init__(self, id, display_name, email_address, role, working_hours, use_business_hours, availability_is_affected_by_personal_calendar, color_index):
        self.id = id
        self.display_name = display_name
        self.email_address = email_address
        self.role = role
        self.working_hours = working_hours
        self.use_business_hours = use_business_hours
        self.availability_is_affected_by_personal_calendar = availability_is_affected_by_personal_calendar
        self.color_index = color_index

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<%s %s id=%r, display_name=%r, email_address=%r role=%r>' % (self.__class__.__name__, id(self), self.id, self.display_name, self.email_address, self.role)

    def update(self, api, business, **kwargs):
        uri = 'bookingBusinesses/%s/staffMembers/%s' % (business, self.id)
        kwargs.setdefault('version', 'beta')
        data = dict(displayName=self.display_name, role=self.role, emailAddress=self.email_address, workingHours=[item.to_dict() for item in self.working_hours], webSiteUrl=self.website_url, useBusinessHours=self.use_business_hours, colorIndex=self.color_index, availabilityIsAffectedByPersonalCalendar=self.availability_is_affected_by_personal_calendar)
        api.request(uri, json=data, method='PATCH', **kwargs)

    def delete(self, api, business, **kwargs):
        uri = 'bookingBusinesses/%s/staffMembers/%s' % (business, self.id)
        kwargs.setdefault('version', 'beta')
        api.request(uri, method='DELETE', **kwargs)

    @classmethod
    def from_api(cls, data):
        id = data['id']
        display_name = data['display_name']
        email_address = data['email_address']
        role = data['role']
        working_hours = [WorkingHours.from_api(item) for item in data['working_hours']]
        use_business_hours = data['use_business_hours']
        availability_is_affected_by_personal_calendar = data['availability_is_affected_by_personal_calendar']
        color_index = data['color_index']
        return cls(id, display_name, email_address, role, working_hours, use_business_hours, availability_is_affected_by_personal_calendar, color_index)

    @classmethod
    def get(cls, api, business, **kwargs):
        kwargs.setdefault('version', 'beta')
        staff_member = kwargs.pop('staff_member', None)
        if staff_member:
            uri = 'bookingBusinesses/%s/staffMembers/%s' % (business, staff_member)
            data = api.request(uri, **kwargs)
            output = cls.from_api(data)
        else:
            uri = 'bookingBusinesses/%s/staffMembers' % business
            params = dict(**kwargs)
            data = api.request(uri, params=params, **kwargs)
            output = [cls.from_api(row) for row in data['value']]
        return output

    @classmethod
    def create(cls, api, business, display_name, email_address, role, **kwargs):
        kwargs.setdefault('version', 'beta')
        uri = 'bookingBusinesses/%s/staffMembers' % business

        working_hours_list = []
        for working_hours in kwargs.get('working_hours', []):
            if isinstance(working_hours, WorkingHours):
                working_hours = working_hours.to_dict()
            working_hours_list.append(working_hours)
        request_data = dict(displayName=display_name, emailAddress=email_address, role=role, workingHours=working_hours_list)
        data = api.request(uri, json=request_data, method='POST', **kwargs)
        return cls.from_api(data)


class WorkingHours(base.Base):
    __slots__ = ('day', 'time_slots')

    def __init__(self, day, time_slots):
        self.day = day
        self.time_slots = time_slots

    def __repr__(self):
        return '<%s %s day=%r, time_slots=%r>' % (self.__class__.__name__, id(self), self.day, self.time_slots)

    def to_dict(self):
        time_slots = [item.to_dict() for item in self.time_slots]
        return dict(day=self.day, timeSlots=time_slots)

    @classmethod
    def from_api(cls, data):
        day = data['day']
        time_slots = [TimeSlot.from_api(item) for item in data['timeSlots']]
        return cls(day, time_slots)


class TimeSlot(base.Base):
    __slots__ = ('start', 'end')

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def to_dict(self):
        return dict(start=self.start.isoformat(), end=self.end.isoformat())

    @classmethod
    def from_api(cls, data):
        raw_start = data['start']
        start = cls.parse_date_time(raw_start)
        raw_end = data['end']
        end = cls.parse_date_time(raw_end)
        return cls(start, end)
