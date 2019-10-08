import copy
import datetime
import json

import responses

from bugsy import Bugsy, Bug, Attachment
from bugsy.errors import (BugsyException, BugException)
from . import rest_url


def test_can_create_bug_and_set_summary_afterwards():
    bug = Bug()
    assert bug.id is None, "Id has been set"
    assert bug.summary is None, "Summary is not set to nothing on plain initialisation"
    bug.summary = "Foo"
    assert bug.summary == 'Foo', "Summary is not being set"
    assert bug.status is None, 'Status has been set'

def test_we_cant_set_status_unless_there_is_a_bug_id():
    bug = Bug()
    try:
        bug.status = 'RESOLVED'
    except BugException as e:
        assert str(e) == "Message: Can not set status unless there is a bug id. Please call Update() before setting Code: None"

def test_we_can_get_OS_set_from_default():
    bug = Bug()
    assert bug.op_sys == "All"

def test_we_can_get_OS_we_set():
    bug = Bug(op_sys="Linux")
    assert bug.op_sys == "Linux"

def test_we_can_get_Product_set_from_default():
    bug = Bug()
    assert bug.product == "core"

def test_we_can_get_the_keywords(bug_return):
    bug = Bug(**bug_return['bugs'][0])
    keywords = bug.keywords
    assert ['regression'] == keywords

def test_we_can_add_single_keyword(bug_return):
    bug = Bug(**bug_return['bugs'][0])
    bug.keywords.append('ateam-marionette-server')
    output = bug.diff()
    assert isinstance(output, dict)
    assert output == {'keywords': {
        'add': ['ateam-marionette-server']
    }}
    assert ['regression', 'ateam-marionette-server'] == bug.keywords

def test_we_can_add_multiple_keywords_to_list(bug_return):
    bug = Bug(**bug_return['bugs'][0])
    bug.keywords.extend(['intermittent', 'ateam-marionette-server'])
    output = bug.diff()
    assert isinstance(output, dict)
    assert sorted(output['keywords']['add']) == sorted(['intermittent', 'ateam-marionette-server'])
    keywords = bug.keywords
    assert sorted(['regression', 'intermittent', 'ateam-marionette-server']) == sorted(keywords)

def test_we_can_add_remove_a_keyword_list(bug_return):
    bug = Bug(**bug_return['bugs'][0])
    bug.keywords.remove('regression')
    output = bug.diff()
    assert isinstance(output, dict)
    assert output == {'keywords': {
        'remove': ['regression']
    }}
    keywords = bug.keywords
    assert [] == keywords

def test_we_can_get_product_we_set():
    bug = Bug(product="firefox")
    assert bug.product == "firefox"

def test_we_can_get_get_cc_list(bug_return):
    bug = Bug(**bug_return['bugs'][0])
    cced = bug.cc
    assert isinstance(cced, list)
    assert ['coop@mozilla.com', 'dburns@mozilla.com',
            'jlund@mozilla.com', 'mdas@mozilla.com'] == cced

def test_we_can_add_single_email_to_cc_list(bug_return):
    bug = Bug(**bug_return['bugs'][0])
    bug.cc.append('foo@bar.com')
    output = bug.diff()
    assert isinstance(output, dict)
    assert output == {'cc': {'add': ['foo@bar.com']}}

def test_we_can_add_multiple_emails_to_cc_list(bug_return):
    bug = Bug(**bug_return['bugs'][0])
    bug.cc.extend(['automatedtester@mozilla.com', 'foobar@mozilla.com'])
    output = bug.diff()
    assert isinstance(output, dict)
    assert sorted(output['cc']['add']) == sorted(['automatedtester@mozilla.com', 'foobar@mozilla.com'])

def test_we_can_add_remove_an_email_to_cc_list(bug_return):
    bug = Bug(**bug_return['bugs'][0])
    bug.cc.append('automatedtester@mozilla.com')
    bug.cc.remove('dburns@mozilla.com')
    output = bug.diff()
    assert isinstance(output, dict)
    assert output == {'cc': {
        'add': ['automatedtester@mozilla.com'],
        'remove': ['dburns@mozilla.com']
    }}

def test_we_can_remove_an_email_to_cc_list(bug_return):
    bug = Bug(**bug_return['bugs'][0])
    bug.cc.remove('dburns@mozilla.com')
    output = bug.diff()
    assert isinstance(output, dict)
    assert output == {'cc': {'remove': ['dburns@mozilla.com']}}

def test_we_throw_an_error_for_invalid_status_types(bug_return):
    bug = Bug(**bug_return['bugs'][0])
    try:
        bug.status = "foo"
        assert False, "Should have thrown an error about invalid type"
    except BugException as e:
        assert str(e) == "Message: Invalid status type was used Code: None"

def test_we_can_get_the_resolution(bug_return):
    bug = Bug(**bug_return['bugs'][0])
    assert "FIXED" == bug.resolution

def test_we_can_set_the_resolution(bug_return):
    bug = Bug(**bug_return['bugs'][0])
    bug.resolution = 'INVALID'
    assert bug.resolution == 'INVALID'

def test_we_cant_set_the_resolution_when_not_valid(bug_return):
    bug = Bug(**bug_return['bugs'][0])
    try:
        bug.resolution = 'FOO'
        assert False, "Should thrown an error"
    except BugException as e:
        assert str(e) == "Message: Invalid resolution type was used Code: None"

def test_we_can_pass_in_dict_and_get_a_bug(bug_return):
    bug = Bug(**bug_return['bugs'][0])
    assert bug.id == 1017315
    assert bug.status == 'RESOLVED'
    assert bug.summary == 'Schedule Mn tests on opt Linux builds on cedar'
    assert bug.assigned_to == "jgriffin@mozilla.com"

def test_we_can_get_a_dict_version_of_the_bug(bug_return):
    bug = Bug(**bug_return['bugs'][0])
    result = bug.to_dict()
    assert bug_return['bugs'][0]['id'] == result['id']

def test_we_can_get_depends_on_list(bug_return):
    bug = Bug(**bug_return['bugs'][0])
    depends_on = bug.depends_on
    assert isinstance(depends_on, list)
    assert depends_on == [123456]

def test_we_can_add_and_remove_depends_on(bug_return):
    bug = Bug(**bug_return['bugs'][0])
    bug.depends_on.remove(123456)
    bug.depends_on.append(145123)
    output = bug.diff()
    assert isinstance(output, dict)
    assert output == {'depends_on': {
        'add': [145123],
        'remove': [123456]
    }}
    deps = bug.depends_on
    assert isinstance(deps, list)
    assert [145123] == deps

def test_we_can_get_blocks_list(bug_return):
    bug = Bug(**bug_return['bugs'][0])
    blocks = bug.blocks
    assert isinstance(blocks, list)
    assert blocks == [654321]

def test_we_can_add_and_remove_blocks(bug_return):
    bug = Bug(**bug_return['bugs'][0])
    bug.blocks.remove(654321)
    bug.blocks.append(145123)
    output = bug.diff()
    assert isinstance(output, dict)
    assert output == {'blocks': {
        'add': [145123],
        'remove': [654321]
    }}
    deps = bug.blocks
    assert isinstance(deps, list)
    assert [145123] == deps

@responses.activate
def test_we_can_update_a_bug_from_bugzilla(bug_return):
    responses.add(responses.GET, rest_url('bug', 1017315),
                  body=json.dumps(bug_return), status=200,
                  content_type='application/json', match_querystring=True)
    bugzilla = Bugsy()
    bug = bugzilla.get(1017315)
    responses.reset()
    responses.add(responses.GET, 'https://bugzilla.mozilla.org/rest/bug/1017315',
                  body=json.dumps(bug_return), status=200,
                  content_type='application/json')
    clone = Bug(bugsy=bugzilla, **bug.to_dict())
    clone.status = 'NEW'
    clone.update()
    assert clone.id == 1017315
    assert clone.status == 'RESOLVED'

def test_we_cant_update_unless_we_have_a_bug_id():
    bug = Bug()
    try:
        bug.update()
    except BugException as e:
        assert str(e) == "Message: Unable to update bug that isn't in Bugzilla Code: None"

@responses.activate
def test_we_can_update_a_bug_with_login_token(bug_return):
  responses.add(responses.GET, 'https://bugzilla.mozilla.org/rest/login',
                        body='{"token": "foobar"}', status=200,
                        content_type='application/json', match_querystring=True)

  responses.add(responses.GET, rest_url('bug', 1017315),
                body=json.dumps(bug_return), status=200,
                content_type='application/json', match_querystring=True)
  bugzilla = Bugsy()
  bug = bugzilla.get(1017315)
  responses.reset()
  responses.add(responses.GET, 'https://bugzilla.mozilla.org/rest/bug/1017315',
                body=json.dumps(bug_return), status=200,
                content_type='application/json')
  clone = Bug(bugsy=bugzilla, **bug.to_dict())
  clone.status = 'NEW'
  clone.update()
  assert clone.id == 1017315
  assert clone.status == 'RESOLVED'

@responses.activate
def test_that_we_can_add_a_comment_to_a_bug_before_it_is_put(bug_return):
    responses.add(responses.GET, 'https://bugzilla.mozilla.org/rest/login',
                          body='{"token": "foobar"}', status=200,
                          content_type='application/json', match_querystring=True)

    responses.add(responses.GET, 'https://bugzilla.mozilla.org/rest/bug/1017315?include_fields=version&include_fields=id&include_fields=summary&include_fields=status&include_fields=op_sys&include_fields=resolution&include_fields=product&include_fields=component&include_fields=platform',
                  body=json.dumps(bug_return), status=200,
                  content_type='application/json', match_querystring=True)
    bugzilla = Bugsy("foo", "bar")
    bug = Bug()
    bug.summary = "I like cheese"
    bug.add_comment("I like sausages")

    bug_dict = bug.to_dict().copy()
    bug_dict['id'] = 123123

    responses.add(responses.POST, 'https://bugzilla.mozilla.org/rest/bug',
                      body=json.dumps(bug_dict), status=200,
                      content_type='application/json', match_querystring=True)
    bugzilla.put(bug)

@responses.activate
def test_that_we_can_add_a_comment_to_an_existing_bug(bug_return):
    responses.add(responses.GET, 'https://bugzilla.mozilla.org/rest/login',
                          body='{"token": "foobar"}', status=200,
                          content_type='application/json', match_querystring=True)

    responses.add(responses.GET, rest_url('bug', 1017315),
                  body=json.dumps(bug_return), status=200,
                  content_type='application/json', match_querystring=True)
    bugzilla = Bugsy("foo", "bar")
    bug = bugzilla.get(1017315)

    responses.add(responses.POST, 'https://bugzilla.mozilla.org/rest/bug/1017315/comment',
                      body=json.dumps({}), status=200,
                      content_type='application/json', match_querystring=True)

    bug.add_comment("I like sausages")

    assert len(responses.calls) == 3

@responses.activate
def test_comment_retrieval(bug_return, comments_return):
    responses.add(responses.GET, 'https://bugzilla.mozilla.org/rest/login',
                        body='{"token": "foobar"}', status=200,
                        content_type='application/json', match_querystring=True)
    responses.add(responses.GET, rest_url('bug', 1017315),
                  body=json.dumps(bug_return), status=200,
                  content_type='application/json', match_querystring=True)
    responses.add(responses.GET, 'https://bugzilla.mozilla.org/rest/bug/1017315/comment',
                    body=json.dumps(comments_return), status=200,
                    content_type='application/json', match_querystring=True)

    bugzilla = Bugsy("foo", "bar")
    bug = bugzilla.get(1017315)
    comments = bug.get_comments()
    assert len(comments) == 2
    c1 = comments[0]
    assert c1.attachment_id is None
    assert c1.author == u'gps@mozilla.com'
    assert c1.bug_id == 1017315
    assert c1.creation_time == datetime.datetime(2014, 3, 27, 23, 47, 45)
    assert c1.creator == u'gps@mozilla.com'
    assert c1.id == 8589785
    assert c1.is_private is False
    assert c1.text == u'text 1'
    assert c1.tags == set([u'tag1', u'tag2'])
    assert c1.time == datetime.datetime(2014, 3, 27, 23, 47, 45)

@responses.activate
def test_we_raise_an_exception_when_getting_comments_and_bugzilla_errors(bug_return):
    responses.add(responses.GET, 'https://bugzilla.mozilla.org/rest/login',
                          body='{"token": "foobar"}', status=200,
                          content_type='application/json', match_querystring=True)

    responses.add(responses.GET, rest_url('bug', 1017315),
                  body=json.dumps(bug_return), status=200,
                  content_type='application/json', match_querystring=True)
    bugzilla = Bugsy("foo", "bar")
    bug = bugzilla.get(1017315)

    error_response = {'code': 67399,
                      'message': "The requested method 'Bug.comments' was not found.",
                      'documentation': u'http://www.bugzilla.org/docs/tip/en/html/api/',
                       'error': True}

    responses.add(responses.GET, 'https://bugzilla.mozilla.org/rest/bug/1017315/comment',
                    body=json.dumps(error_response), status=400,
                    content_type='application/json', match_querystring=True)
    try:
        comments = bug.get_comments()
        assert False, "Should have raised an BugException for the bug not existing"
    except BugsyException as e:
        assert str(e) == "Message: The requested method 'Bug.comments' was not found. Code: 67399"

@responses.activate
def test_we_raise_an_exception_if_commenting_on_a_bug_that_returns_an_error(bug_return):
    responses.add(responses.GET, 'https://bugzilla.mozilla.org/rest/login',
                          body='{"token": "foobar"}', status=200,
                          content_type='application/json', match_querystring=True)

    responses.add(responses.GET, rest_url('bug', 1017315),
                  body=json.dumps(bug_return), status=200,
                  content_type='application/json', match_querystring=True)
    bugzilla = Bugsy("foo", "bar")
    bug = bugzilla.get(1017315)

    # will now return the following error. This could happen if the bug was open
    # when we did a `get()` but is now hidden
    error_response = {'code': 101,
                      'message': 'Bug 1017315 does not exist.',
                      'documentation': 'http://www.bugzilla.org/docs/tip/en/html/api/',
                      'error': True}
    responses.add(responses.POST, 'https://bugzilla.mozilla.org/rest/bug/1017315/comment',
                      body=json.dumps(error_response), status=404,
                      content_type='application/json', match_querystring=True)
    try:
        bug.add_comment("I like sausages")
        assert False, "Should have raised an BugException for the bug not existing"
    except BugsyException as e:
        assert str(e) == "Message: Bug 1017315 does not exist. Code: 101"

    assert len(responses.calls) == 3

@responses.activate
def test_we_can_add_tags_to_bug_comments(bug_return, comments_return):
    responses.add(responses.GET, 'https://bugzilla.mozilla.org/rest/login',
                          body='{"token": "foobar"}', status=200,
                          content_type='application/json', match_querystring=True)

    responses.add(responses.GET, rest_url('bug', 1017315),
                  body=json.dumps(bug_return), status=200,
                  content_type='application/json', match_querystring=True)
    bugzilla = Bugsy("foo", "bar")
    bug = bugzilla.get(1017315)

    responses.add(responses.GET, 'https://bugzilla.mozilla.org/rest/bug/1017315/comment',
                    body=json.dumps(comments_return), status=200,
                    content_type='application/json', match_querystring=True)

    comments = bug.get_comments()

    responses.add(responses.PUT, 'https://bugzilla.mozilla.org/rest/bug/comment/8589785/tags',
                    body=json.dumps(["spam", "foo"]), status=200,
                    content_type='application/json', match_querystring=True)
    comments[0].add_tags("foo")

    assert len(responses.calls) == 4

@responses.activate
def test_we_can_remove_tags_to_bug_comments(bug_return, comments_return):
    responses.add(responses.GET, 'https://bugzilla.mozilla.org/rest/login',
                          body='{"token": "foobar"}', status=200,
                          content_type='application/json', match_querystring=True)

    responses.add(responses.GET, rest_url('bug', 1017315),
                  body=json.dumps(bug_return), status=200,
                  content_type='application/json', match_querystring=True)
    bugzilla = Bugsy("foo", "bar")
    bug = bugzilla.get(1017315)

    responses.add(responses.GET, 'https://bugzilla.mozilla.org/rest/bug/1017315/comment',
                    body=json.dumps(comments_return), status=200,
                    content_type='application/json', match_querystring=True)

    comments = bug.get_comments()

    responses.add(responses.PUT, 'https://bugzilla.mozilla.org/rest/bug/comment/8589785/tags',
                    body=json.dumps(["spam","foo"]), status=200,
                    content_type='application/json', match_querystring=True)
    comments[0].remove_tags("foo")

    assert len(responses.calls) == 4

def test_adding_new_field_to_existing_bug():
    # This can occur if a bug is retrieved using limited fields
    bug = Bug({})
    bug.alias = 'foobar'
    diff = bug.diff()
    assert diff['alias'] == 'foobar'

@responses.activate
def test_bug_update_updates_copy_dict(bug_return, comments_return):
    responses.add(responses.GET, 'https://bugzilla.mozilla.org/rest/login',
                  body='{"token": "foobar"}', status=200,
                  content_type='application/json', match_querystring=True)
    bugzilla = Bugsy("foo", "bar")
    bug = Bug(bugzilla, **bug_return['bugs'][0])

    bug.status = 'NEW'
    diff = bug.diff()
    bug_dict = copy.deepcopy(bug_return)
    bug_dict['bugs'][0]['status'] = 'NEW'
    responses.add(responses.GET, 'https://bugzilla.mozilla.org/rest/bug/1017315',
                  body=json.dumps(bug_dict), status=200,
                  content_type='application/json')

    responses.add(responses.PUT, 'https://bugzilla.mozilla.org/rest/bug/1017315',
                  body=json.dumps(diff), status=200,
                  content_type='application/json')

    bugzilla.put(bug)
    bug.update()
    assert bug._copy['status'] == 'NEW'

@responses.activate
def test_attachment_retrieval(attachment_return, bug_return):
    responses.add(responses.GET, 'https://bugzilla.mozilla.org/rest/login',
                        body='{"token": "foobar"}', status=200,
                        content_type='application/json', match_querystring=True)
    responses.add(responses.GET, rest_url('bug', 1017315),
                  json=bug_return, status=200,
                  content_type='application/json', match_querystring=True)
    responses.add(responses.GET, 'https://bugzilla.mozilla.org/rest/bug/1017315/attachment',
                  json=attachment_return, status=200,
                  content_type='application/json', match_querystring=True)

    bugzilla = Bugsy("foo", "bar")
    bug = bugzilla.get(1017315)
    attachments = bug.get_attachments()
    assert len(attachments) == 1

    attachment = attachments[0].to_dict()
    for k, v in attachment.items():
        if k in ['creation_time', 'last_change_time']:
            orig = attachment_return['bugs']['1017315'][0][k]
            assert v == datetime.datetime.strptime(orig, '%Y-%m-%dT%H:%M:%SZ')
        else:
            orig = attachment_return['bugs']['1017315'][0][k]
            assert v == orig

@responses.activate
def test_add_attachment(attachment_return, bug_return):
    responses.add(responses.GET, 'https://bugzilla.mozilla.org/rest/login',
                        body='{"token": "foobar"}', status=200,
                        content_type='application/json', match_querystring=True)
    responses.add(responses.GET, rest_url('bug', 1017315),
                  json=bug_return, status=200,
                  content_type='application/json', match_querystring=True)
    responses.add(responses.POST, 'https://bugzilla.mozilla.org/rest/bug/1017315/attachment',
                  json=attachment_return, status=200,
                  content_type='application/json', match_querystring=True)

    bugzilla = Bugsy("foo", "bar")
    bug = bugzilla.get(1017315)
    attachment = Attachment(bugzilla, **attachment_return['bugs']['1017315'][0])
    bug.add_attachment(attachment)

    assert len(responses.calls) == 3

@responses.activate
def test_add_attachment_with_missing_required_fields(attachment_return, bug_return):
    responses.add(responses.GET, 'https://bugzilla.mozilla.org/rest/login',
                        body='{"token": "foobar"}', status=200,
                        content_type='application/json', match_querystring=True)
    responses.add(responses.GET, rest_url('bug', 1017315),
                  json=bug_return, status=200,
                  content_type='application/json', match_querystring=True)
    responses.add(responses.POST, 'https://bugzilla.mozilla.org/rest/bug/1017315/attachment',
                  json=attachment_return, status=200,
                  content_type='application/json', match_querystring=True)

    bugzilla = Bugsy("foo", "bar")
    bug = bugzilla.get(1017315)
    clone = copy.deepcopy(attachment_return['bugs']['1017315'][0])
    del clone['data']
    attachment = Attachment(bugzilla, **clone)

    try:
        bug.add_attachment(attachment)
        assert False, "Should have raised a BugException due to add without data"
    except BugException as e:
        assert str(e) == "Message: Cannot add attachment without all required fields Code: None"

def test_we_cant_add_attachment_without_id(attachment_return):
    bug = Bug()
    attachment = Attachment(None, **attachment_return['bugs']['1017315'][0])

    try:
        bug.add_attachment(attachment)
    except BugException as e:
        assert str(e) == "Message: Cannot add an attachment without a bug id Code: None"
