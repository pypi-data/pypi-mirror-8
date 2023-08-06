#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
.. deprecated:: 0.6
    You should use safe connection encoding, such as utf-8. This module will be
    removed in a future release.

.. warning::
    This module will be removed in version 0.11.

It applies the escape function in psycopg2 to :mod:`mosql.util`.

Usage:

::

    import mosql.psycopg2_escape
    mosql.psycopg2_escape.conn = CONNECTION

It will replace the escape functions in :mod:`mosql.util`.

.. versionadded:: 0.3
'''

# --- the removal warning ---
from .util import warning
warning('mosql.psycopg2_escape will be removed in version 0.11.')
# --- end ---

from psycopg2.extensions import QuotedString
import psycopg2

conn = None

def escape(s):
    qs = QuotedString(s)
    if conn:
        qs.prepare(conn)
    return qs.getquoted()[1:-1]

import mosql.util
mosql.util.escape = escape
