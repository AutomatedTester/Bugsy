#!/usr/bin/env python

import bugsy
from pdb import set_trace as bp

bugzilla = bugsy.Bugsy(api_key='REDACTED')
bugs = bugzilla.search_for\
        .product('Foo')\
        .search()

for bug in bugs:
    print(str(bug.id) + " " + bug.summary)