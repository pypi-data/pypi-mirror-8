# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""
The :class:`~openstack.transport.Transport` is a subclass of
``requests.Session`` that adds some features that are common in OpenStack
APIs or can be globally controlled by an application.  Its use is incredibly
similar to ``requests.Session`` such that we only will cover the differences
in detail here.

The common OpenStack functionality added include:

* Log all requests and responses at debug level.
* Support json encoding in the request() method.
* Set the default user_agent at Transport creation.  If it is set to None to
  skip the header.
* Set the default verify at Transport creation.

Examples
--------

Basic HTTP GET
~~~~~~~~~~~~~~

Making a basic HTTP GET call is very simple::

    from openstack import transport
    trans = transport.Transport()
    versions = trans.get('http://cloud.example.com:5000').json()

will retrieve the version data served by the Identity API into a Python dict.

HTTP POST
~~~~~~~~~

Creating a new object in an OpenStack service is similarly simple::

    from openstack import transport
    trans = transport.Transport()
    new_record = {'name': 'The White Albumn', 'artist': 'The Beatles'}
    resp = trans.post('http://cloud.example.com:4999/record', json=new_record)

Passing in the new_record dict with the ``json`` keyword argument performs the
``json.dumps()`` prior to the request being sent.  This is an addition to
the capabilities of ``requests.Session``.

Additional HTTP Methods
~~~~~~~~~~~~~~~~~~~~~~~

Just as in ``requests.Session``, all of the HTTP verbs have corresponding
methods in the :class:`~openstack.transport.Transport` object.

SSL/TLS and Certificates
~~~~~~~~~~~~~~~~~~~~~~~~

The ``verify`` argument to ``Transport.request()`` can now be set when the
Transport object is created.  It can still be overwritten during any
individual call to ``request()`` or the HTTP verb methods.

To set the default hostname verification for the Transport to use a custom
CA certificate file::

    from openstack import transport
    trans = transport.Transport(verify='/etc/tls/local-ca-certs.crt')

The same usage from ``requests`` is still available.  To use the default CA
certificate file for a single request::

    versions = trans.get('https://cloud.example.com:5000', verify=True)

Or hit on a host with a self-signed certificate::

    versions = trans.get('https://cloud.example.com:5000', verify=None)

Redirection
~~~~~~~~~~~

Redirection handling differs from ``requests`` by default as this module is
expected to be primarily used for querying REST API servers.  The redirection
model differs in that ``requests`` follows some browser patterns where it
will redirect POSTs as GETs for certain statuses which is not want we want
for an API.

See: https://en.wikipedia.org/wiki/Post/Redirect/Get

User Agent
~~~~~~~~~~

The ``User-Agent`` header may be set when the Transport object is created in
addition to the existing per-request mode.  The determination of how to set
the ``User-Agent`` header is as follows:

* If the ``user_agent`` argument is included in the ``request()`` call use it
* Else if ``User-Agent`` is set in the headers dict use it
* Else if ``user_agent`` argument is included in the
  :class:`~openstack.transport.Transport` construction use it
* Else use ``transport.DEFAULT_USER_AGENT``
"""

import json
import logging

import requests
import six
from six.moves import urllib

import openstack
from openstack import exceptions


DEFAULT_USER_AGENT = 'python-OpenStackSDK/' + openstack.__version__

_logger = logging.getLogger(__name__)
JSON = 'application/json'


class Transport(requests.Session):

    _user_agent = DEFAULT_USER_AGENT

    REDIRECT_STATUSES = (301, 302, 303, 305, 307)
    DEFAULT_REDIRECT_LIMIT = 30

    def __init__(
            self,
            user_agent=None,
            verify=True,
            redirect=DEFAULT_REDIRECT_LIMIT,
            accept=JSON,
    ):
        """Create a new :class:`~openstack.transport.Transport` object.

        In addition to those listed below, all arguments available to
        ``requests.Session`` are available here:

        :param string user_agent: Set the default ``User-Agent`` header;
                                  Header is omitted if ``None`` and no value
                                  is supplied in the ``request()`` call.
        :param boolean/string verify: If ``True``, the SSL cert will be
                                      verified. A CA_BUNDLE path can also be
                                      provided.
        :param boolean/integer redirect: (integer) The maximum number of
                                         redirections followed in a request.
                                         (boolean) No redirections if False,
                                         requests.Session handles redirection
                                         if True. (optional)
        :param string accept: Type of output to accept

        User agent handling is as follows:

        * if user_agent arg is included in the request() call, use it
        * else if 'User-Agent' is set in the headers dict, use it
        * else if user_agent arg is included in the __init__() call, use it
        * else use DEFAULT_USER_AGENT

        """

        super(Transport, self).__init__()
        if user_agent:
            self._user_agent = user_agent
        self.verify = verify
        self._redirect = redirect
        self._accept = accept

    def request(self, method, url, redirect=None, **kwargs):
        """Send a request

        Perform an HTTP request. The following arguments differ from
        ``requests.Session``:

        :param string method: Request HTTP method
        :param string url: Request URL
        :param boolean/integer redirect: (integer) The maximum number of
                                         redirections followed in a request.
                                         (boolean) No redirections if False,
                                         requests.Session handles redirection
                                         if True. (optional)

        The following additional kw args are supported:

        :param object json: Request body to be encoded as JSON
                            Overwrites ``data`` argument if present
        :param string accept: Set the ``Accept`` header; overwrites
                                  any value that may be in the headers dict.
                                  Header is omitted if ``None``.
        :param string user_agent: Set the ``User-Agent`` header; overwrites
                                  any value that may be in the headers dict.
                                  Header is omitted if ``None``.

        Remaining kw args from requests.Session.request() supported

        """

        headers = kwargs.setdefault('headers', {})

        # JSON-encode the data in json arg if present
        # Overwrites any existing 'data' value
        json_data = kwargs.pop('json', None)
        if json_data is not None:
            kwargs['data'] = json.dumps(json_data)
            headers['Content-Type'] = JSON

        # Set User-Agent header if user_agent arg included, or
        # fall through the default chain as described above
        if 'user_agent' in kwargs:
            headers['User-Agent'] = kwargs.pop('user_agent')
        elif self._user_agent:
            headers.setdefault('User-Agent', self._user_agent)
        else:
            headers.setdefault('User-Agent', DEFAULT_USER_AGENT)

        if redirect is None:
            redirect = self._redirect

        if isinstance(redirect, bool) and redirect:
            # Fall back to requests redirect handling
            kwargs['allow_redirects'] = True
        else:
            # Force disable requests redirect handling, we will manage
            # redirections below
            kwargs['allow_redirects'] = False
        if 'accept' in kwargs:
            accept = kwargs.pop('accept')
        else:
            accept = self._accept
        if accept:
            headers.setdefault('Accept', accept)

        self._log_request(method, url, **kwargs)

        resp = self._send_request(method, url, redirect, **kwargs)

        self._log_response(resp)

        try:
            resp.raise_for_status()
        except requests.RequestException as e:
            raise exceptions.HttpException(six.text_type(e), details=resp.text)
        if accept == JSON:
            try:
                resp.body = resp.json()
            except ValueError as e:
                # this may be simplejson.decode.JSONDecodeError
                # Re-raise into our own exception
                raise exceptions.InvalidResponse(response=resp.text)

        return resp

    def _send_request(self, method, url, redirect, **kwargs):
        # NOTE(jamielennox): We handle redirection manually because the
        # requests lib follows some browser patterns where it will redirect
        # POSTs as GETs for certain statuses which is not want we want for an
        # API. See: https://en.wikipedia.org/wiki/Post/Redirect/Get

        resp = super(Transport, self).request(method, url, **kwargs)

        self._log_response(resp)

        if resp.status_code in self.REDIRECT_STATUSES:
            # Be careful here in python True == 1 and False == 0
            if isinstance(redirect, bool):
                redirect_allowed = redirect
            else:
                redirect -= 1
                redirect_allowed = redirect >= 0

            if redirect_allowed:
                try:
                    location = resp.headers['location']
                except KeyError:
                    _logger.warn(
                        "Redirection from %s failed, no location provided",
                        resp.url,
                    )
                else:
                    new_resp = self._send_request(
                        method,
                        location,
                        redirect,
                        **kwargs
                    )

                    new_resp.history = list(new_resp.history)
                    new_resp.history.insert(0, resp)
                    resp = new_resp

        return resp

    def _log_request(self, method, url, **kwargs):
        if not _logger.isEnabledFor(logging.DEBUG):
            return

        if 'params' in kwargs and kwargs['params']:
            url += '?' + urllib.parse.urlencode(kwargs['params'])

        string_parts = [
            "curl -i",
            "-X '%s'" % method,
            "'%s'" % url,
        ]

        # kwargs overrides the default
        if (('verify' in kwargs and kwargs['verify'] is False) or
                not self.verify):
            string_parts.append('--insecure')

        for element in kwargs['headers'].items():
            header = " -H '%s: %s'" % element
            string_parts.append(header)

        if 'data' in kwargs and kwargs['data'] is not None:
            string_parts.append("--data '")
            string_parts.append(kwargs['data'])
            string_parts.append("'")
        _logger.debug("REQ: %s" % " ".join(string_parts))

    def _log_response(self, response):
        _logger.debug(
            "RESP: [%s] %r" % (
                response.status_code,
                response.headers,
            ),
        )
        if response._content_consumed:
            _logger.debug(
                "RESP BODY: %s",
                response.text,
            )
        _logger.debug(
            "encoding: %s",
            response.encoding,
        )
