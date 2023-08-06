import sys
import logging
import contextlib
from collections import OrderedDict

from six import iteritems, StringIO
from six.moves.urllib.parse import urlsplit, urlunsplit
from devpi.main import main as devpi
from twitter.common.contextutil import mutable_sys, temporary_dir


logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("devpi").setLevel(logging.WARNING)


class DevpiClientError(Exception):
    """
    Exception thrown whenever a client command fails
    """
    pass


@contextlib.contextmanager
def DevpiClient(url, user=None, password=None):
    """
    Yields a light wrapper object around the devpi client.
    """
    with temporary_dir() as client_dir:
        wrapper = DevpiCommandWrapper(url, client_dir)

        if user and password is not None:
            wrapper.login(user, password)

        yield wrapper


class DevpiCommandWrapper(object):

    def __init__(self, url, client_dir):
        self._url = url
        self._server_url = self._extract_server_url(url)
        self._client_dir = client_dir
        self._execute('use', url)

    def _extract_server_url(self, url):
        parts = urlsplit(url)
        return urlunsplit((parts.scheme, parts.netloc, '', '', ''))

    def _execute(self, *args, **kwargs):
        kwargs = OrderedDict(kwargs)
        kwargs.update({'--clientdir': self._client_dir})

        args = ['devpi'] + list(args) + ['{}={}'.format(k, v) for k,v in iteritems(kwargs)]

        with mutable_sys():
            sys.stdout = sys.stderr = output = StringIO()
            try:
                devpi(args)
                return output.getvalue()
            except SystemExit:
                raise DevpiClientError(output.getvalue())

    def use(self, *args):
        url = '/'.join([self._server_url] + list(args))
        result = self._execute('use', url)
        self._url = url # to be exception save, only updated now
        return result

    def login(self, user, password):
        return self._execute('login', user, '--password', password)

    def logoff(self):
        return self._execute('logoff')

    def create_user(self, user, *args, **kwargs):
        return self._execute('user', '--create', user, *args, **kwargs)

    def create_index(self, index, *args, **kwargs):
        return self._execute('index', '--create', index, *args, **kwargs)

    def modify_user(self, user, *args, **kwargs):
        return self._execute('user', '--modify', user, *args, **kwargs)

    def modify_index(self, index, *args, **kwargs):
        return self._execute('index', index, *args, **kwargs)

    def upload(self, path, directory=False):
        if directory:
            return self._execute("upload", "--from-dir", path)
        else:
            return self._execute("upload", path)

    def list(self, *args):
        try:
            return self._execute('list', *args).splitlines()
        except DevpiClientError as e:
            if '404 Not Found' in str(e):
                return []
            else:
                raise e

    @property
    def server_url(self):
        return self._server_url

    @property
    def url(self):
        return self._url
