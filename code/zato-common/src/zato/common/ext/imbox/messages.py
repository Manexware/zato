# -*- coding: utf-8 -*-

"""
This module is a modified vendor copy of the Imbox package from https://pypi.org/project/imbox/

The MIT License (MIT)

Copyright (c) 2013 Martin Rusev

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import logging

from zato.common.ext.imbox.query import build_search_query
from zato.common.ext.imbox.parser import fetch_email_by_uid


logger = logging.getLogger(__name__)


class Messages:

    IMAP_ATTRIBUTE_LOOKUP = {
        'unread': '(UNSEEN)',
        'flagged': '(FLAGGED)',
        'unflagged': '(UNFLAGGED)',
        'sent_from': '(FROM "{}")',
        'sent_to': '(TO "{}")',
        'date__gt': '(SINCE "{}")',
        'date__lt': '(BEFORE "{}")',
        'date__on': '(ON "{}")',
        'subject': '(SUBJECT "{}")',
        'uid__range': '(UID {})',
        'text': '(TEXT "{}")',
    }

    FOLDER_LOOKUP = {}

    def __init__(self,
                 connection,
                 parser_policy,
                 **kwargs):

        self.connection = connection
        self.parser_policy = parser_policy
        self.kwargs = kwargs
        self._uid_list = self._query_uids(**kwargs)

        logger.debug("Fetch all messages for UID in {}".format(self._uid_list))

    def _fetch_email(self, uid):
        return fetch_email_by_uid(uid=uid,
                                  connection=self.connection,
                                  parser_policy=self.parser_policy)

    def _query_uids(self, **kwargs):
        query_ = build_search_query(self.IMAP_ATTRIBUTE_LOOKUP, **kwargs)
        _, data = self.connection.uid('search', None, query_)
        if data[0] is None:
            return []
        return data[0].split()

    def _fetch_email_list(self):
        for uid in self._uid_list:
            yield uid, self._fetch_email(uid)

    def __repr__(self):
        if len(self.kwargs) > 0:
            return 'Messages({})'.format('\n'.join('{}={}'.format(key, value)
                                                   for key, value in self.kwargs.items()))
        return 'Messages(ALL)'

    def __iter__(self):
        return self._fetch_email_list()

    def __next__(self):
        return self

    def __len__(self):
        return len(self._uid_list)

    def __getitem__(self, index):
        uids = self._uid_list[index]

        if not isinstance(uids, list):
            uid = uids
            return uid, self._fetch_email(uid)

        return [(uid, self._fetch_email(uid))
                for uid in uids]
