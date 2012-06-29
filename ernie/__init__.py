
"""BERT-ERNIE Library"""

__version__ = "0.0.1"

from ernie import ThreadedErnie, Ernie


def mod(name):
    return Ernie.mod(name)


def start(daemon=False, host='', port=50007):
    '''
        Starts a Ernie server on given interface and port.
        If daemon is True the server will start on a separate thread
        and return immediately, otherwise it will never return
        until killed.
    '''
    server = ThreadedErnie()
    server.start(daemon=daemon, host=host, port=port)
