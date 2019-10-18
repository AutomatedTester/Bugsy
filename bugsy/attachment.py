import base64
import binascii
import copy
from datetime import datetime as dt

import six

from .errors import AttachmentException


class Attachment(object):
    """
        Represents a single Bugzilla attachment.

        To get comments you need to do the following

        >>> bugs = bugzilla.search_for.keywords("checkin-needed").search()
        >>> attachments = bugs[0].get_attachments()
        >>> # Returns the attachment's comment
        >>> attachments[0].comment
    """
    CREATE_REQUIRED = ['data', 'file_name', 'summary', 'content_type']
    CREATE_FIELDS = CREATE_REQUIRED + ['comment', 'flags', 'is_markdown', 'is_patch', 'is_private']
    UPDATE_FIELDS = ['bug_flags', 'comment', 'content_type', 'file_name', 'flags', 'is_obsolete',
                     'is_patch', 'is_private', 'summary']

    def __init__(self, bugsy, **kwargs):
        self._bugsy = bugsy
        self._attachment = dict(**kwargs)
        self._copy = copy.deepcopy(self._attachment)

    def __getattr__(self, attr):
        if attr not in self._attachment:
            return None

        return self._attachment[attr]

    def __setattr__(self, attr, value):
        if attr.startswith('_'):
            if attr == '_bugsy':
                object.__setattr__(self, attr, value)
            elif attr == '_attachment':
                clone = copy.deepcopy(value)
                time_fields = {'creation_time', 'last_change_time'}
                for time_field in list(time_fields & set(clone.keys())):
                    clone[time_field] = dt.strptime(clone[time_field], '%Y-%m-%dT%H:%M:%SZ')
                object.__setattr__(self, attr, clone)
            elif attr == '_copy':
                object.__setattr__(self, attr, value)
        else:
            if attr == 'data':
                # Attempt to decode data to ensure it's valid
                try:
                    if hasattr(base64, 'decodebytes'):
                        base64.decodebytes(value.encode('utf-8'))
                    else:
                        base64.decodestring(value)
                except binascii.Error:
                    raise AttachmentException('The data field value must be in base64 format')
            elif attr in ['comment', 'content_type', 'file_name', 'summary']:
                if not isinstance(value, six.string_types):
                    raise AttachmentException('The %s field value must be of type string' % attr)
            elif attr in ['is_patch', 'is_private']:
                if not isinstance(value, bool):
                    raise AttachmentException('The %s field value must be of type bool' % attr)
            elif attr == 'flags' or attr == 'bug_flags':
                if not isinstance(value, list):
                    # ToDo: Once flags are implemented, this should check isInstance(list[i], Flag)
                    raise AttachmentException('The %s field value must be of type list' % attr)

            self._attachment[attr] = copy.copy(value)

    def to_dict(self):
        """
            Return the raw dict that is used inside this object
        """
        return self._attachment

    def update(self):
        if not self.id:
            raise AttachmentException('Cannot update bug without an attachment id')

        updates = {}
        for k in self._attachment:
            if k in self.UPDATE_FIELDS:
                updates[k] = self._attachment[k]

        res = self._bugsy.request('bug/attachment/%s' % self.id,
                                  method='PUT', json=updates)

        self._attachment = res['attachments'][0]
        self._copy = copy.deepcopy(self._attachment)
