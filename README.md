Python-Ernie
=====
Original Ruby port by Ken Robertson (ken@invalidlogic.com)
Threaded/forking version implemented by Miguel Paolino (miguel@paolino.com.uy).

python-ernie is a (now a sync and async) port of the Ruby-based Ernie server by Tom Preston-Werner. Python-Ernie is the Python server implementation for the BERT-RPC specification. The default request serving method is sync and secuential, this version also gives the possibility to serve requests in a async (parallel) fashion using threads or forks.

See the full BERT-RPC specification at [bert-rpc.org](http://bert-rpc.org).


Installation
------------

To install python-ernie, you can use pip or traditional setup.py:

    $ pip install git+git://github.com/mpaolino/python-ernie 

pip will install all the dependencies for you which you have to do by yourself when using setup.py directly. This means you need to install the Python port of BERT serializers and Erlastic.

    $ git clone git://github.com/samuel/python-erlastic.git
    $ sudo python python-erlastic/setup.py install
    
    $ git clone git://github.com/samuel/python-bert.git
    $ sudo python python-bert/setup.py install

To install python-ernie itself, run:

    $ sudo ./setup.py install


Example Handler
---------------
There is more than one way to use ernie, the non-blocking and the blocking way. The non-blocking way will start the BERT-RPC server and return the program control to subsequent lines of code, it will be the responsability of the user to keep the program using the library running. This comes in handy when you need to do other stuff besides serving BERT-RPC.
Calling the start() method of the service/library on a non-blocking manner and do nothing will fail to keep the server running
since the main process will finish and with it the child RPC server thread/process.

Non blocking server example
---------------------------


    from ernie import mod, start
    
    def calc_add(a, b):
        return a + b
    mod('calc').fun('add', calc_add)
    
    if __name__ == "__main__":
        start(daemon=True)
        while True:
            time.sleep(100)

Blocking server example 
----------------------


    from ernie import mod, start
    
    def calc_add(a, b):
        return a + b
    mod('calc').fun('add', calc_add)
    
    if __name__ == "__main__":
        start()

async
-----
To serve request asynchronously you can choose to use threads or forking processes. Forking has the advantage of using all the underlying available CPUs of the system. Threads will use all the CPUs but will compete por the GIL making the computation time similar -if not worst- to serial execution time for CPU-bound tasks. You are not exempt from doing your share of thinking, functions that execute in parallel on threads or processes will have to be designed to do so. Also, beware of libraries that are not thread-safe, those will not work with ernie threads.

To use the async mode you pass several arguments to the start function.


    start(daemon=False, host='', port=50007, async=False, forking=False)

    Parameters:
    
    daemon  - Blocking/non-blocking ernie server. Defaults to False, blocking mode.
    host    - Host (IP) to bind. Empty string means all IPs, defaults to all IPs.
    port    - TCP port to bind to.
    async   - Run in async mode. Defaults to False, meaning sync mode.
    forking - Use forks for async. Defaults to False, meaning threads.


Contribute
----------

If you'd like to hack on python-ernie, start by forking my repo on GitHub:

http://github.com/mpaolino/python-ernie

Just create your own fork, hack on it, and then send me a pull request once done.


Todo
---------

1. Better separate library functionality (transport agnostic) from implemented service.
1. Update exception handling to return traceback
1. Ensure correct handling around read operations
1. See if I can clean up the way you define your modules
1. Test

Credits
---------

* [@krobertson](https://github.com/krobertson) for original Ruby port and authoring python-ernie
* [@mojombo](https://github.com/mojombo) for BERT/Ernie
* [@samuel](https://github.com/samuel) for python-bert
* [@dergraf](https://github.com/dergraf) for pip compatibility

License
---------

Copyright (c) 2012 Miguel Paolino

Copyright (c) 2009 Ken Robertson

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
