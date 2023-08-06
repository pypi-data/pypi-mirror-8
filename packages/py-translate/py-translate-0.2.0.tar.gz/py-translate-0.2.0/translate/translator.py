# -*- coding: utf-8 -*-
"""
translator
~~~~~~~~~~

Defines the interaction with the translation service.
Since the program interfaces with the google web service, this
module deals with the client side logic of pushing the translation request
to the the server.
"""

import sys
import json

from multiprocessing.dummy import Pool as ThreadPool
from functools import wraps, partial

try:
    from urllib.request import urlopen, Request, quote
    from urllib.parse import urlencode
    from queue import Queue
except ImportError:
    from urllib2 import urlopen, Request, quote
    from urllib import urlencode
    from Queue import Queue


__all__ = [
    'push_url',
    'translator',
    'coroutine',
    'text_sink',
    'spooler',
    'source'
]


def push_url(site):
    '''
    Decorates a function returning the url of translation API.
    Creates and maintains HTTP connection state

    Returns a dict response object from the server containing the translated
    text and metadata of the request body

    :param site: translator
    :type site: function
    :return: HTTP Response
    :rtype: json
    '''

    @wraps(site)
    def connection(*args, **kwargs):
        agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:27.0) Gecko/20100101 Firefox/27.0'
        headers = {'User-Agent': agent}
        url = site(*args, **kwargs)
        request = Request(url, headers=headers)

        # Make HTTP Request
        req = urlopen(request)
        req_stream = req.read().decode('utf-8')
        req.close()
        return json.loads(req_stream)

    return connection


@push_url
def translator(source, target, phrase):
    """
    Returns the url encoded string that will be pushed to the translation
    server for parsing.

    :param source: Language code for translation source
    :type source: str
    :param target: Language code that source will be translate into
    :type target: str
    :param phrase: Text body string that will be url encoded and translated
    :type phrase: str
    :return: url
    :rtype: str

    List of acceptable language codes for source and target languages
    can be found as a JSON file in the etc directory.

    Some source languages are limited in scope of the possible target languages
    that are available.

    .. code-block:: python

        >>> import translate
        >>> translate.translator('en', 'zh-TW', 'Hello World!')
            '你好世界！'

    """

    base = 'http://translate.google.com/translate_a/t'
    params = urlencode(
    {
        'client': 'webapp',
            'ie': 'utf-8',
            'oe': 'utf-8',
            'sl': source,
            'tl': target,
             'q': phrase,
    })
    url = '?'.join([base, params])
    return url


def coroutine(func):
    """
    Co-routine decorator primes first call to next
    """

    @wraps(func)
    def initialization(*args, **kwargs):
        start = func(*args, **kwargs)
        try:
            start.__next__()
        except AttributeError:
            start.next()
        return start

    return initialization


@coroutine
def text_sink(source, dest):
    """
    Coroutine end-point. Outputs text stream into translator
    """
    task_queue = []
    pool = ThreadPool(8)
    try:
        while True:
            line = (yield)
            task_queue.append(line)
    finally:
        result = pool.map(partial(translator, source, dest), task_queue)

        pool.close()
        pool.join()

        for trans in result:
            for line in trans['sentences']:
                sys.stdout.write(line['trans'])
        sys.stdout.write('\n')



@coroutine
def spooler(iterable):
    """Consumes text stream and spools into larger chunk for processing"""
    try:
        while True:
            wordcount, spool = 0, str()
            while wordcount < 1500:
                stream = (yield)
                spool += stream
                wordcount += len(quote(stream).encode('utf-8'))
            else:
                iterable.send(spool)
    finally:
        iterable.send(spool)
        sys.stdout.write('\n')


def source(target):
    """Coroutine start point. Produces text stream and forwards to consumers"""

    # TODO: Implement FileIO
    if sys.stdin.isatty():
        # target.send(args.file)
        return

    for line in sys.stdin:
        target.send(line)
