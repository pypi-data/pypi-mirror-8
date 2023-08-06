# PyKronos

## Introduction

The contents of this file can be found in `demo.py` and are compiled
into `README.md`, so you can consume the readme while running the
Python script to understand how it works.

## Importing PyKronos And Some Useful Utilities

Check out `pykronos.client` and `pykronos.common.time` for some useful
utility functions.  PyKronos has a bunch of utilities to deal with
`datetime` objects.
```python
from pykronos.client import ID_FIELD
from pykronos.client import TIMESTAMP_FIELD
from pykronos.client import KronosClient
from pykronos.client import ResultOrder
from pykronos.common.time import datetime_to_kronos_time
from datetime import datetime
from datetime import timedelta
from dateutil.tz import tzutc
```
## Creating A Client

Create a Kronos client with the URL of a running server.  Optionally
provide a `namespace` to explicitly work with events in a particular
namespace.
```python
kc = KronosClient('http://localhost:8151', namespace='kronos')
start = datetime.now(tz=tzutc())
```
### A Non-blocking Client

Pass a `blocking=False` to the KronosClient constructor for a client
that won't block on the Kronos server when you insert data.  A
background thread will batch up data and send it to the server.  This
is useful for logging/metrics collection on machines that can't wait
for a write acknowledgement.  An optional `sleep_block` argument,
defaulting to `0.1` specifies how many seconds to wait between batches
to the server.  If the process running the client crashes before
flushing events, those events will be lost.
```python
nonblocking = KronosClient('http://localhost:8151', namespace='kronos',
                           blocking=False)
```
## Inserting Events

Insert events with the `put` command.  The argument is a dictionary of
stream names (e.g., `yourproduct.website.pageviews`) to a list of
JSON-encodable dictionaries to insert to each stream.
```python
kc.put(
  {'yourproduct.website.pageviews': [
      {'source': 'http://test.com',
       'browser': {'name': 'Firefox', 'version': 26},
       'pages': ['page1.html', 'page2.html']}],
   'yourproduct.website.clicks': [
      {'user': 40, 'num_clicks': 7},
      {'user': 42, 'num_clicks': 2}]
   })
```
### Optionally Add A Timestamp

By default, each event will be timestamped on the client.  If you add
a `TIMESTAMP_FIELD` argument, you can specify the time at which each
event ocurred.
```python
optional_time = datetime_to_kronos_time(start + timedelta(seconds=5))
kc.put({'yourproduct.website.clicks': [
  {'user': 35, 'num_clicks': 10, TIMESTAMP_FIELD: optional_time}]})

```
## Retrieving Events

Retrieving events requires a stream name, a start datetime, and an end
datetime.  Note that an `ID_FIELD` and `@TIMESTAMP_FIELD` field are
attached to each event.  The `ID_FIELD` is a UUID1-style identifier
with its time bits derived from the timestamp.  This allows event IDs
to be roughly sortable by the time that they happened while providing
a deterministic tiebreaker when two events happened at the same time.
```python
events = kc.get('yourproduct.website.clicks',
                start,
                start + timedelta(minutes=10))
for event in events:
  print 'Received event', event
  last_event_id = event[ID_FIELD]
```
### Event Order

By default, events are returned in ascending order of their
`ID_FIELD`.  Pass in an`order=ResultOrder.DESCENDING` argument to
change this behavior to be in descending order of `ID_FIELD`.
```python
events = kc.get('yourproduct.website.clicks',
                start,
                start + timedelta(minutes=10),
                order=ResultOrder.DESCENDING)
for event in events:
  print 'Reverse event', event
  last_event_id = event[ID_FIELD]
```
### Limiting Events

If you only want to retrieve a limited number of events, use the
`limit` argument.
```python
events = kc.get('yourproduct.website.clicks',
                start,
                start + timedelta(minutes=10),
                order=ResultOrder.DESCENDING,
                limit=1)
for event in events:
  print 'Limited event', event
  last_event_id = event[ID_FIELD]
```
## Getting A List Of Streams

To see all streams available in this namespace, use `get_streams`.
```python
for stream in kc.get_streams():
  print 'Found stream', stream
```
## Inferred Schema

You can retrieve a schema for a stream. The schema is inferred from the
structure of the individual events. The schema protocol is based on JSON Schema
v4.
```python
response = kc.infer_schema('yourproduct.website.clicks')
print response['schema']
```
## Deleting Events

Sometimes, we make an oopsie and need to delete some events.  The
`delete` function takes similar arguments for the start and end
timestamps to delete.

Note: The most common Kronos use cases are for write-mostly systems
with high-throughput reads.  As such, you can imagine that most
backends will not be delete-optimized.  There's nothing in the Kronos
API that inherently makes deletes not performant, but we imagine some
backends will make tradeoffs to optimize their write and read paths at
the expense of fast deletes.
```python
kc.delete('yourproduct.website.clicks',
          start + timedelta(seconds=5),
          start + timedelta(minutes=10))

events = kc.get('yourproduct.website.clicks',
                start,
                start + timedelta(minutes=10))
for event in events:
  print 'Received event', event
```
