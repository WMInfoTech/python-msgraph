## Beta
Any `msgraph.beta` module is subject to change.  According to the Microsoft Graph website:

> APIs under the `/beta` version in Microsoft Graph are subject to change. Use of these APIs in production applications is not supported.


### Booking
**Last updated**: 2020-10-01

The [Microsoft Bookings API](https://docs.microsoft.com/en-us/graph/api/resources/booking-api-overview?view=graph-rest-beta) currently requires user authentication to get access to a business's appointments, customers, services, or staff members.  For a working example, see [Azure-Samples/ms-identity-python-webapp](https://github.com/Azure-Samples/ms-identity-python-webapp).

#### Fetching businesses
To fetch all businesses using `msgraph`, use the `bookings ` module's `Business` class:

```python
from msgraph import api
from msgraph.beta import booking

# authenticate and create API instance here
resource_uri = 'https://graph.microsoft.com'
access_token = ''
api_instance = api.GraphAPI(resource_uri, access_token)

businesses = booking.Business.get(api_instance)
```

or to fetch a specific `msgraph.beta.Business` instance, provide the `business` ID as the `business` keyword argument:

```python
business = booking.Business.get(api_instance, business='MyBusiness@johndoe.onmicrosoft.com')
```

#### Fetching Appointment
**Last updated**: 2020-10-01
To fetch all appointments using `msgraph`, use the `bookings ` module's `Appointment` class:

```python
from msgraph.beta import booking

business = booking.Business.get(api_instance, business='MyBusiness@johndoe.onmicrosoft.com')
customers = booking.Appointment.get(api_instance, business)
```

or to fetch a specific `msgraph.beta.Appointment` instance, provide the `appointment` ID as the `appointment` keyword argument:

```python
appointment = booking.Customer.get(api_instance, business, appointment='myappointmentid')
```


#### Fetching Customers
**Last updated**: 2020-10-01
To fetch all services using `msgraph`, use the `bookings ` module's `Customer` class:

```python
from msgraph.beta import booking

business = booking.Business.get(api_instance, business='MyBusiness@johndoe.onmicrosoft.com')
customers = booking.Customer.get(api_instance, business)
```

or to fetch a specific `msgraph.beta.Customer` instance, provide the `customer` ID as the `customer` keyword argument:

```python
customer = booking.Customer.get(api_instance, business, customer='myservice')
```


#### Fetching Services
**Last updated**: 2020-10-01
To fetch all services using `msgraph`, use the `bookings ` module's `Service` class:

```python
from msgraph.beta import booking

business = booking.Business.get(api_instance, business='MyBusiness@johndoe.onmicrosoft.com')
services = booking.Service.get(api_instance, business)
```

or to fetch a specific `msgraph.beta.Service` instance, provide the `service` ID as the `service` keyword argument:

```python
service = booking.Service.get(api_instance, business, service='myservice')
```


#### Fetching Staff Members
**Last updated**: 2020-10-01
To fetch all services using `msgraph`, use the `bookings ` module's `StaffMember` class:

```python
from msgraph.beta import booking

business = booking.Business.get(api_instance, business='MyBusiness@johndoe.onmicrosoft.com')
staff_members = booking.StaffMember.get(api_instance, business)
```

or to fetch a specific `msgraph.beta.Service` instance, provide the `StaffMember` ID as the `staff_member` keyword argument:

```python
staff_member = booking.StaffMember.get(api_instance, business, staff_member='mystaffmemberid')
```
