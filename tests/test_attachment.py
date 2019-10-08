import copy
import datetime
import json

import responses

from bugsy import Bugsy, Attachment, AttachmentException


def test_init(attachment_return):
    bugzilla = Bugsy()
    source = attachment_return['bugs']['1017315'][0]
    attachment = Attachment(bugzilla, **source)
    attach_dict = attachment.to_dict()
    for k in attachment_return['bugs']['1017315'][0]:
        if k in ['creation_time', 'last_change_time']:
            continue
        assert attach_dict[k] == source[k]


def test_retrieve_unset_field(attachment_return):
    bugzilla = Bugsy()
    source = attachment_return['bugs']['1017315'][0]
    attachment = Attachment(bugzilla, **source)
    assert attachment.foo is None


def test_we_can_get_a_dict_version_of_the_bug(attachment_return):
    bugzilla = Bugsy()
    attachment = Attachment(bugzilla, **attachment_return['bugs']['1017315'][0])
    result = attachment.to_dict()
    assert attachment_return['bugs']['1017315'][0]['id'] == result['id']


def test_datetime_conversion(attachment_return):
    bugzilla = Bugsy()
    source = attachment_return['bugs']['1017315'][0]
    attachment = Attachment(bugzilla, **source)

    assert isinstance(attachment.creation_time, datetime.datetime)


def test_setter_validate_base64_types(attachment_return):
    bugzilla = Bugsy()
    source = attachment_return['bugs']['1017315'][0]
    attachment = Attachment(bugzilla, **source)

    attachment.data = 'Rm9vYmFy'
    assert attachment.data == 'Rm9vYmFy'

    try:
        attachment.data = 'foobar'
        assert False, "Should have raised an AttachmentException due to invalid data value"
    except AttachmentException as e:
        assert str(e) == "Message: The data field value must be in base64 format Code: None"


def test_setter_validate_string_types(attachment_return):
    bugzilla = Bugsy()
    source = attachment_return['bugs']['1017315'][0]
    attachment = Attachment(bugzilla, **source)

    for field in ['comment', 'content_type', 'file_name', 'summary']:
        setattr(attachment, field, 'foobar')
        assert getattr(attachment, field) == 'foobar'

        try:
            setattr(attachment, field, 1)
            assert False, "Should have raised an AttachmentException due to invalid data value"
        except AttachmentException as e:
            match = "Message: The %s field value must be of type string Code: None" % field
            assert str(e) == match


def test_setter_validate_boolean_types(attachment_return):
    bugzilla = Bugsy()
    source = attachment_return['bugs']['1017315'][0]
    attachment = Attachment(bugzilla, **source)

    for field in ['is_patch', 'is_private']:
        setattr(attachment, field, True)
        assert getattr(attachment, field)

        try:
            setattr(attachment, field, 'non-boolean')
            assert False, "Should have raised an AttachmentException due to invalid data value"
        except AttachmentException as e:
            match = "Message: The %s field value must be of type bool Code: None" % field
            assert str(e) == match


def test_setter_validate_list_types(attachment_return):
    bugzilla = Bugsy()
    source = attachment_return['bugs']['1017315'][0]
    attachment = Attachment(bugzilla, **source)

    for field in ['bug_flags', 'flags']:
        setattr(attachment, field, ['flag'])
        assert getattr(attachment, field) == ['flag']

        try:
            setattr(attachment, field, 'non-boolean')
            assert False, "Should have raised an AttachmentException due to invalid list value"
        except AttachmentException as e:
            match = "Message: The %s field value must be of type list Code: None" % field
            assert str(e) == match


@responses.activate
def test_update_post_required_fields(attachment_return):
    resp_dict = {'attachments': [{}]}
    for k, v in attachment_return['bugs']['1017315'][0].items():
        if k in Attachment.UPDATE_FIELDS:
            resp_dict['attachments'][0][k] = copy.deepcopy(v)
    resp_dict['attachments'][0]['summary'] = 'Updated summary'

    def request_callback(request):
        header = {}
        body = json.dumps(json.loads(request.body), sort_keys=True)
        if body != json.dumps(resp_dict['attachments'][0], sort_keys=True):
            return 500, header, "Invalid payload supplied"
        else:
            return 200, header, json.dumps(resp_dict)

    attach_id = attachment_return['bugs']['1017315'][0]['id']
    responses.add_callback(
        responses.PUT, 'https://bugzilla.mozilla.org/rest/bug/attachment/%s' % attach_id,
        callback=request_callback,
        content_type='application/json',
    )

    bugzilla = Bugsy()
    attachment = Attachment(bugzilla, **attachment_return['bugs']['1017315'][0])
    attachment.summary = 'Updated summary'
    attachment.update()

    assert attachment.summary == 'Updated summary'


@responses.activate
def test_update_without_an_id_fails(attachment_return):
    data = copy.deepcopy(attachment_return['bugs']['1017315'][0])
    resp_dict = {'attachments': [data]}
    resp_dict['attachments'][0]['id'] = None
    bugzilla = Bugsy()
    attachment = Attachment(bugzilla, **resp_dict)

    try:
        attachment.update()
        assert False, "Should have raised an AttachmentException due to update without id"
    except AttachmentException as e:
        assert str(e) == "Message: Cannot update bug without an attachment id Code: None"
