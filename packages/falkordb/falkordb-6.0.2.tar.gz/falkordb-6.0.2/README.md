# falkor-py

The Python interface to the Redis key-value store.

[![CI](https://github.com/falkordb/falkordb-py/workflows/CI/badge.svg?branch=master)](https://github.com/falkordb/falkordb-py/actions?query=workflow%3ACI+branch%3Amaster)
[![docs](https://readthedocs.org/projects/falkordb/badge/?version=stable&style=flat)](https://falkordb-py.readthedocs.io/en/stable/)
[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![pypi](https://badge.fury.io/py/falkordb.svg)](https://pypi.org/project/falkordb/)
[![pre-release](https://img.shields.io/github/v/release/falkordb/falkor-py?include_prereleases&label=latest-prerelease)](https://github.com/falkordb/falkordb-py/releases)
[![codecov](https://codecov.io/gh/falkordb/falkordb-py/branch/master/graph/badge.svg?token=yenl5fzxxr)](https://codecov.io/gh/falkordb/falkordb-py)

[Installation](#installation) |  [Usage](#usage) | [Advanced Topics](#advanced-topics) | [Contributing](https://github.com/falkordb/falkordb-py/blob/master/CONTRIBUTING.md)

## How do I Redis?

[Try the FalkkorDB Cloud](https://cloud.falkordb.com)

[Dive in developer tutorials](https://docs.falkordb.com/)

[Join the FalkorDB community](https://www.falkordb.com/contact-us)

## Installation

Start a redis via docker:

``` bash
docker run -p 6379:6379 -it falkordb/falkordb:latest
```

To install falkordb-py, simply:

``` bash
$ pip install falkordb
```

For faster performance, install falkordb with hiredis support, this provides a compiled response parser, and *for most cases* requires zero code changes.
By default, if hiredis >= 1.0 is available, falkordb-py will attempt to use it for response parsing.

``` bash
$ pip install "falkordb[hiredis]"
```

## Usage

### Basic Example

``` python
>>> import falkordb
>>> r = falkordb.Redis(host='localhost', port=6379, db=0)
>>> r.set('foo', 'bar')
True
>>> r.get('foo')
b'bar'
```

The above code connects to localhost on port 6379, sets a value in Redis, and retrieves it. All responses are returned as bytes in Python, to receive decoded strings, set *decode_responses=True*.  For this, and more connection options, see [these examples](https://falkordb.readthedocs.io/en/stable/examples.html).


#### RESP3 Support

To enable support for RESP3, ensure you have at least version 5.0 of the client, and change your connection object to include *protocol=3*

``` python
>>> import falkordb
>>> r = falkordb.Redis(host='localhost', port=6379, db=0, protocol=3)
```

### Connection Pools

By default, falkordb-py uses a connection pool to manage connections. Each instance of a Redis class receives its own connection pool. You can however define your own [falkordb.ConnectionPool](https://falkordb.readthedocs.io/en/stable/connections.html#connection-pools).

``` python
>>> pool = falkordb.ConnectionPool(host='localhost', port=6379, db=0)
>>> r = falkordb.Redis(connection_pool=pool)
```

Alternatively, you might want to look at [Async connections](https://falkordb.readthedocs.io/en/stable/examples/asyncio_examples.html), or [Cluster connections](https://falkordb.readthedocs.io/en/stable/connections.html#cluster-client), or even [Async Cluster connections](https://falkordb.readthedocs.io/en/stable/connections.html#async-cluster-client).

### Redis Commands

There is built-in support for all of the [out-of-the-box Redis commands](https://redis.io/commands). They are exposed using the raw Redis command names (`HSET`, `HGETALL`, etc.) except where a word (i.e. del) is reserved by the language. The complete set of commands can be found [here](https://github.com/falkordb/falkor-py/tree/master/redis/commands), or [the documentation](https://falkordb.readthedocs.io/en/stable/commands.html).

## Advanced Topics

The [official Redis command documentation](https://redis.io/commands)
does a great job of explaining each command in detail. falkor-py attempts
to adhere to the official command syntax. There are a few exceptions:

-   **MULTI/EXEC**: These are implemented as part of the Pipeline class.
    The pipeline is wrapped with the MULTI and EXEC statements by
    default when it is executed, which can be disabled by specifying
    transaction=False. See more about Pipelines below.

-   **SUBSCRIBE/LISTEN**: Similar to pipelines, PubSub is implemented as
    a separate class as it places the underlying connection in a state
    where it can\'t execute non-pubsub commands. Calling the pubsub
    method from the Redis client will return a PubSub instance where you
    can subscribe to channels and listen for messages. You can only call
    PUBLISH from the Redis client (see [this comment on issue
    #151](https://github.com/falkordb/falkor-py/issues/151#issuecomment-1545015)
    for details).

For more details, please see the documentation on [advanced topics page](https://falkordb.readthedocs.io/en/stable/advanced_features.html).

### Pipelines

The following is a basic example of a [Redis pipeline](https://redis.io/docs/manual/pipelining/), a method to optimize round-trip calls, by batching Redis commands, and receiving their results as a list.


``` python
>>> pipe = r.pipeline()
>>> pipe.set('foo', 5)
>>> pipe.set('bar', 18.5)
>>> pipe.set('blee', "hello world!")
>>> pipe.execute()
[True, True, True]
```

### PubSub

The following example shows how to utilize [Redis Pub/Sub](https://redis.io/docs/manual/pubsub/) to subscribe to specific channels.

``` python
>>> r = falkordb.Redis(...)
>>> p = r.pubsub()
>>> p.subscribe('my-first-channel', 'my-second-channel', ...)
>>> p.get_message()
{'pattern': None, 'type': 'subscribe', 'channel': b'my-second-channel', 'data': 1}
```


--------------------------

### Author

falkor-py is developed and maintained by [FalkorDB Inc](https://www.falkordb.com). It can be found [here](
https://github.com/falkordb/falkor-py), or downloaded from [pypi](https://pypi.org/project/falkordb/).

Special thanks to:

-   Andy McCurdy (<sedrik@gmail.com>) the original author of falkor-py.
-   Ludovico Magnocavallo, author of the original Python Redis client,
    from which some of the socket code is still used.
-   Alexander Solovyov for ideas on the generic response callback
    system.
-   Paul Hubbard for initial packaging support.

[![Redis](./docs/logo-redis.png)](https://www.redis.com)
