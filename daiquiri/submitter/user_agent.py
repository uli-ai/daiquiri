# =============================================================================
# IMPORTS
# =============================================================================
import abc
import os

# =============================================================================
# MODULE CLASSES
# =============================================================================

class UserAgentBase(abc.ABC):
    """ Base class for user agent.

    Methods
    -------
    upload
    download
    """
    def __init__(self, *args, **kwargs):
        super(UserAgentBase, self).__init__()

    @abc.abstractmethod
    def upload(self, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def download(self, *args, **kwargs):
        raise NotImplementedError

class SocketUserAgent(UserAgentBase):
    """ User agent with `socket` package.

    """
    def __init__(self, sock):
        super(SocketUserAgent, self).__init__()

        # local imports
        import socket
        self.sock = sock

    def upload(self, path, buffer_size=1024):
        """ Upload file using socket.

        """
        assert os.path.isfile(path), 'Path does not exist.'

        # send size
        sock.send('size' + str(
            os.path.getsize(path)))

        with open(path, 'rb') as f_handle:
            # get data
            data = f.read(buffer_size)
            
            # send data
            self.sock.send(data)

        self.sock.close()

    def download(self, path, buffer_size=1024):
        """ Download file using socket.

        """
        # get size
        # TODO: is this hard-coded `4` right?
        size = int(self.sock.recv(buffer_size)[4:])

        # TODO:
        # this is not consistent with your original implemtation,
        # the file name argument should be speicifed, right?
        with open(path, 'wb') as f_handle:
            # initial receive
            data = sock.recv(buffer_size)

            # get total receive
            total_recv = len(data)

            # write to file
            f_handle.write(data)

            while total_recv < size:
                data = sock.recv(buffer_size)
                total_recv += len(data)
                f_handle.write(data)








