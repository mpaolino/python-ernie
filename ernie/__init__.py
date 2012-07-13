
"""BERT-ERNIE Library"""

__version__ = "0.0.1"

from ernie import ErnieServer, Ernie


def mod(name):
    return Ernie.mod(name)


def start(daemon=False, host='', port=50007, forking=False, async=False):
    '''
        Starts a Ernie server on given interface and port.
        If daemon is True the server will start on a separate thread
        and return immediately, otherwise it will never return
        until killed.
    '''
    server = ErnieServer(daemon=daemon, host=host, port=port, forking=forking,
                         async=async)
    server.start()
