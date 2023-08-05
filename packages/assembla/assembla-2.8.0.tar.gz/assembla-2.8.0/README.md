Python wrapper for the Assembla API
===================================

An easy to use wrapper around the [Assembla API](http://api-doc.assembla.com/).

- [Installation](#installation)
- [Basic example](#basic-example)
- [User guide](#user-guide)
- [Filtering objects with keyword arguments](#filtering-objects-with-keyword-arguments)
- [Custom fields](#custom-fields)
- [Caching](#caching)


Installation
------------

Install assembla with pip:

```
$ pip install assembla
```

Connecting to Assembla's API requires your user account's authentication key and secret,
which are accessible from https://www.assembla.com/user/edit/manage_clients.


Basic example
-------------

The following example connects to Assembla, retrieves a list of tickets for a
space and then outputs information about each.

```python
from assembla import API

assembla = API(
    key='8a71541e5fb2e4741120',
    secret='a260dc4448c81c907fc7c85ad09d31306c425417',
    # Use your API key/secret from https://www.assembla.com/user/edit/manage_clients
)

my_space = assembla.spaces(name='My Space')[0]

for ticket in my_space.tickets():
    print '#{0} - {1}'.format(ticket['number'], ticket['summary'])

# >>> #1 - My first ticket
# >>> #2 - My second ticket
# ...
```


User guide
----------

The Assembla API wrapper uses a number of Python classes to represent
the objects retrieved from Assembla, some of which possess the following
methods and properties:

- [API](#api)
    - [stream()](#apistream)
    - [spaces()](#apispaces)
- [Space](#space)
    - [tickets()](#spacetickets)
    - [milestones()](#spacemilestones)
    - [components()](#spacecomponents)
    - [tools()](#spacetools)
    - [users()](#spaceusers)
- [Milestone](#milestone)
    - [tickets()](#milestonetickets)
- [Ticket](#ticket)
    - [milestone()](#ticketmilestone)
    - [user()](#ticketuser)
    - [component()](#ticketcomponent)
    - [comments()](#ticketcomments)
    - [write()](#ticketwrite)
    - [delete()](#ticketdelete)
- [User](#user)
    - [tickets()](#usertickets)
- [Component](#component)
- [Space tool](#space-tool)
- [Wiki Page](#wiki-page)
    - [write()](#wikipagewrite)
    - [delete()](#wikipagedelete)
- [Event](#event)


API
---

API instances are the primary facet of the Assembla API wrapper and are
the starting point for interactions with the API. APIs are instantiated
with authentication details (available from
https://www.assembla.com/user/edit/manage_clients) and offer two methods
of navigating Assembla's data:

###API.stream()
Returns a list of [Event](#event) instances indicating the
activity stream you have access to. Keyword arguments can be provided
to [filter](#filtering-objects-with-keyword-arguments) the results.


###API.spaces()
Returns a list of [Space](#space) instances which represent
all the spaces that you have access to. Keyword arguments can be provided
to [filter](#filtering-objects-with-keyword-arguments) the results.

Here's an example which prints a list of the spaces available:
```python
from assembla import API

assembla = API(
    key='8a71541e5fb2e4741120',
    secret='a260dc4448c81c907fc7c85ad09d31306c425417',
    # Use your API key/secret from https://www.assembla.com/user/edit/manage_clients
)

for space in assembla.spaces():
	print space['name']
```


Space
-----

See the [Space object field reference](http://api-doc.assembla.com/content/ref/space_fields.html#fields)
for field names and explanations.

Spaces possess the following methods:

###Space.tickets()
Returns a list of all [Ticket](#ticket) instances inside the Space.
Keyword arguments can be provided to [filter](#filtering-objects-with-keyword-arguments) the results.
###Space.milestones()
Returns a list of all [Milestone](#milestone) instances inside the Space.
Keyword arguments can be provided to [filter](#filtering-objects-with-keyword-arguments) the results.
###Space.components()
Returns a list of all [Component](#component) instances inside the Space.
Keyword arguments can be provided to [filter](#filtering-objects-with-keyword-arguments) the results.
###Space.tools()
Returns a list of all [SpaceTool](#space-tool) instances inside the Space.
Keyword arguments can be provided to [filter](#filtering-objects-with-keyword-arguments) the results.
###Space.users()
Returns a list of all [User](#user) instances with access to the Space.
Keyword arguments can be provided to [filter](#filtering-objects-with-keyword-arguments) the results.
###Space.tags()
Returns a list of all [Tag](#tag) instances inside the Space.
Keyword arguments can be provided to [filter](#filtering-objects-with-keyword-arguments) the results.

Here is an example which prints a report of all the tickets in a
Space which have the status 'New' and belong to a milestone called 'Alpha Release':
```python
space = assembla.spaces(name='My Space')[0]

milestone = space.milestones(title='Alpha Release')[0]

tickets = space.tickets(
	milestone_id=milestone['id'],
	status='New'
)

print 'New tickets in "{0}".format(milestone['title'])
for ticket in tickets:
    print '#{0} - {1}'.format(ticket['number'], ticket['summary'])

# >>> New tickets in "Alpha Release"
# >>> #1 - My first ticket
# >>> #2 - My second ticket
# ...
```


Milestone
---------

See the [Milestone object field reference](http://api-doc.assembla.com/content/ref/milestones_fields.html#fields)
for field names and explanations.

Milestone instances possess the following method:

###Milestone.tickets()
Returns a list of all [Ticket](#ticket) instances which are connected to the Milestone.
Keyword arguments can be provided to [filter](#filtering-objects-with-keyword-arguments) the results.

Here is an example which prints a report of all the tickets in a
milestone:
```python
milestone = space.milestones()[0]

for ticket in milestone.tickets():
    print '#{0} - {1}'.format(ticket['number'], ticket['summary'])

# >>> #1 - My first ticket
# >>> #2 - My second ticket
# ...
```


Ticket
------

See the [Ticket object field reference](http://api-doc.assembla.com/content/ref/ticket_fields.html#fields)
for field names and explanations.

Ticket instances possess the following methods:

###Ticket.milestone()
Returns an instance of the [Milestone](#milestone) that the Ticket belongs to.

###Ticket.user()
Returns an instance of the [User](#user) that the Ticket is assigned to.

###Ticket.component()
An instance of the [Component](#component) that the Ticket is assigned to.

###Ticket.comments()
Returns a list of the [Ticket Comment](#ticket-comment) instances relating to the Ticket.

###Ticket.write()
Calling Ticket.write() sends the ticket back to Assembla. The ticket object must have a `space` attribute
set to the corresponding [Space](#space) object.

If the Ticket object has a 'number' key (i.e. if it already exists), the corresponding Ticket on Assembla is _updated_ 
(using an HTTP PUT request), otherwise a new ticket is _created_ in the space (using HTTP POST).

`Ticket.write()` returns the instance of the ticket. If a new ticket was created, the returned instance will have the `number`, `id`, and other
server-generated fields populated.

###Ticket.delete()
Calling Ticket.delete() deletes the ticket from Assembla. The ticket object must have a `space` attribute
set to the corresponding [Space](#space) object.


Ticket Comment
--------------

See the [Ticket Comment object field reference](http://api-doc.assembla.com/content/ref/ticket_comments_fields.html#fields)
for field names and explanations.


User
----

See the [User object field reference](http://api-doc.assembla.com/content/ref/user_fields.html#fields)
for field names and explanations.

User instances possess the following method:

###User.tickets()
Returns a list of all [Ticket](#ticket) instances which are assigned to the User.
Keyword arguments can be provided to [filter](#filtering-objects-with-keyword-arguments) the results.

Here is an example which prints a report of all the tickets assigned
to a user named 'John Smith':
```python
user = space.users(name='John Smith')[0]

for ticket in user.tickets():
    print '#{0} - {1}'.format(ticket['number'], ticket['summary'])

# >>> #1 - John's first ticket
# >>> #2 - John's second ticket
# ...
```


Component
---------

See the [Ticket Component object field reference](http://api-doc.assembla.com/content/ref/ticket_components_fields.html)
for field names and explanations.


Space tool
----------

See the [Space tool object field reference](http://api-doc.assembla.com/content/ref/space_tool_fields.html)
for field names and explanations.


Wiki Page
---------

See the [Wiki Page object field reference](http://api-doc.assembla.com/content/ref/wiki_page_fields.html)
for field names and explanations.

Wiki Page instances possess the following methods:

###WikiPage.write()
Calling WikiPage.write() sends the page back to Assembla. The WikiPage object must have a `space` attribute
set to the corresponding [Space](#space) object.

If the WikiPage object has a 'id' key (i.e. if it already exists), the corresponding WikiPage on Assembla is _updated_
(using an HTTP PUT request), otherwise a new ticket is _created_ in the space (using HTTP POST).

`WikiPage.write()` returns the instance of the ticket. If a new ticket was created, the returned instance will have the
`id` and other server-generated fields populated.

###WikiPage.delete()
Calling WikiPage.delete() deletes the ticket from Assembla. The WikiPage object must have a `space` attribute
set to the corresponding [Space](#space) object.


Tag
---

See the [Tag object field reference](http://api-doc.assembla.com/content/ref/tag_fields.html#fields)
for field names and explanations.


Event
-----

See the [Event object field reference](http://api-doc.assembla.com/content/ref/event_fields.html#fields)
for field names and explanations.


Filtering objects with keyword arguments
----------------------------------------

Most data retrieval methods allow for filtering of the objects based on
the data returned by Assembla. The keyword arguments to use correlate to
the field names returned by Assembla, for example [Tickets](#ticket) can
be filtered with keyword arguments similar to field names specified in
[Assembla's Ticket Fields documentation](http://api-doc.assembla.com/content/ref/ticket_fields.html)

Using [Space.tickets](#spacetickets) as an example of filtering with keyword
arguments:
- `space.tickets(number=100)` will return the ticket with the number 100.
- `space.tickets(status='New', assigned_to_id=100)` will return new tickets assigned to a user with the id 100

Normal keyword filtering will only act on the data that Assembla returns. If
you wish to take advantage of the pre-filtering that Assembla's API offers, an
`extra_params` keyword argument can be provided. The argument should be a
dictionary that contains extra parameters which will be passed along when
the GET request is sent.

For example, to filter Stream events from a certain period:
```python
assembla.stream(extra_params={
    'from': '2014-01-19 09:20'
})
```


Custom fields
-------------

An object's custom fields are retrieved similarly to most fields, the only difference
is that they are nested within a dictionary named `custom_fields`.

Here's an example to get a custom field 'billing_code' from a ticket:
```python
billing_code = ticket['custom_fields']['billing_code']
```


Caching
-------

The API wrapper has an optional response caching system which is deactivated
by default. Turning the caching system on will reduce the overhead on repeated
requests, but can cause stale data to perpetuate for long-running processes.
Turning the cache on is done by setting an [API](#api) instance's `cache_responses`
variable to `True`. The cache can be turned off by setting `cache_responses`
to `False`.

Here is an example of how to instantiate the wrapper and activate the cache.
```python
from assembla import API

assembla = API(
	# Auth details...
)

assembla.cache_responses = True
```


Colophon
--------

[List of contributors](https://github.com/markfinger/assembla/graphs/contributors) is available on Github.

This project is licensed under [The MIT License (MIT)](http://opensource.org/licenses/MIT). Copyright (c) 2014, Mark Finger.

For more information about the license for this particular project [read the LICENSE.md file](LICENSE.md).