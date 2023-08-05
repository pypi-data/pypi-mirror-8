Python utils
************

Tested in Python2.7, Python3.4.

callit
======

You can do::

    from __future__ import print_function

    print('x', 'y', sep=',')

But I can not do::

    from __future__ import print_function

    parameters = ('x', 'y', sep=',')
    print(parameters)

With callit, I can do similar thing::

    from __future__ import print_function
    from yxpy.callit import CallIt

    parameters = CallIt('x', 'y', sep=',')
    parameters(print)

Sometimes, you may use Parameters(similar to CallIt)::

    from __future__ import print_function
    from yxpy.callit import Parameters

    parameters = Parameters('x', 'y', sep=',')
    parameters(format)

dotit
=====

Usually, dictionary can be used like this::

    d = dict(a=1)
    d['b'] = 2
    x = d['a'] + d['b']

The members in dictionary can only be accessed by `[]`, But in some other
languages(eg. javascript), they can be access by `.`::

    d.b = 2
    x = d.a + d.b

With dotit, you can do same thing in similar manner, dotit provide thress
class to do it.

DotDict::

    from dotit import DotDict
    d = DotDict(a=1)
    d.b = 2
    x = d.a + d.b

DotOrderedDict, inherit from collections.OrderedDict::

	...	# similar to DotDict

DotIt, if you already have a dict like object, you can wrapper with DotIt::

    d = dict(a=1, b=2)
    ...
    d = DotDit(d)
    x = d.a + d.b 


loadit
======

Load or reload python object

import module::

    import loadit

load moudule::

    mod = loadit.load_it('mymodule')

load function::

    func = loadit.load_it('mymodule.func')

load class::

    MyClass = loadit.load_it('mymodule.MyClass')

reload module::

    new_mod = loadit.reload_it(mod)

reload function::

    new_func = loadit.reload_it(func)

reload class::

    NewMyClass = loadit.reload_it(MyClass)

yamlfile
========

load config from YAML file, add a include tag.

main.yaml::

    a: !include a.yaml

a.yaml::

    name: a

usage::

    from yxpy import yamlfile

    yamlfile.load('main.yaml')

logginghandlers
===============

- SocketHandler(host, port)
- DatagramHandler(host, port)
- RedisListHandler(list_name, list_maxsize=1024, host='localhost', port=6379, password=None)
- RedisPublishHandler(self, channel, host='localhost', port=6379, password=None)

SocketHandler & DatagramHandler
-------------------------------

logging package provide many Handlers, include `SocketHandler` and
`DatagramHandler`, but the data transmit to server is packed as binary, this
module privide simular handler to transmit plain text to server.

example::

    socket_handler = SocketHandler(host, port)
    ...
    datagram_handler = DatagramHandler(host, port)
    ...

RedisListHandler & RedisPublishHandler 
--------------------------------------

use Redis as log server, the two handler is just privide a singleway to redis
server. to keep simple, the handlers does check the response of redis.

example:

    handler = RedisListHandler(list_name='logtest', list_maxsize=100, password='test')
    ...
    handler = RedisPublishHandler(channel='logtest', password='test')
    ...
