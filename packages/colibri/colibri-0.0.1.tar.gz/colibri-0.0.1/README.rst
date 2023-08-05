colibri - asyncio-based AMQP client
===================================


Usage example
-------------

```python
from asyncio import get_event_loop, coroutine
from colibri import Connection, BasicMessage


@coroutine
def go():
    c = Connection()
    msg = BasicMessage('test message')
    with (yield from c):
        channel = c.channel()
        with (yield from channel):
            yield from channel.exchange_declare('otherex', type='direct')
            yield from channel.queue_declare('otherqueue')
            yield from channel.queue_bind('otherqueue', 'otherex', 'route')
            yield from channel.basic_publish(msg, 'otherex', 'route')
            res = yield from channel.basic_get('otherqueue')
            print("this is the result: ", res.body)

get_event_loop().run_until_complete(go())
```


Installation
------------

Using pip:

```bash
$ pip install colibri
```

From the source (requires virtualenv or root):

```bash
$ setup.py install
```
