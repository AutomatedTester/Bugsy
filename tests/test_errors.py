from . import rest_url
from bugsy import (Bugsy, Bug)
from bugsy.errors import (BugsyException, LoginException)

import responses
import json

@responses.activate
def test_an_exception_is_raised_when_we_hit_an_error():
    responses.add(responses.GET, rest_url('bug', 1017315),
                      body="It's all broken", status=500,
                      content_type='application/json', match_querystring=True)
    bugzilla = Bugsy()
    try:
        bugzilla.get(1017315)
        assert False, "Should have thrown an error that a 500 response was received"
    except BugsyException as e:
        assert str(e) == "Message: We received a 500 error with the following: It's all broken"
