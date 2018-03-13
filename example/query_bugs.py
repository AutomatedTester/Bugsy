#!/usr/bin/env python

import bugsy
from pdb import set_trace as bp

# This example demonstrates querying bugs with an API key for product "Foo"

bugzilla = bugsy.Bugsy(username='REDACTED', api_key='REDACTED')
bugs = bugzilla.search_for\
        .product('Foo')\
        .search()

for bug in bugs:
    print(str(bug.id) + " " + bug.summary)