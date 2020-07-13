import copy
import datetime

from .attachment import Attachment
from .errors import BugException

VALID_STATUS = ["ASSIGNED", "NEW", "REOPENED", "RESOLVED", "UNCONFIRMED", "VERIFIED"]
VALID_RESOLUTION = ["DUPLICATE", "FIXED", "INACTIVE", "INCOMPLETE",
                    "INVALID", "MOVED", "WONTFIX", "WORKSFORME"]
ARRAY_TYPES = ["blocks", "cc", "cc_detail", "depends_on",
               "flags", "groups", "keywords", "see_also"]


def str2datetime(s):
    return datetime.datetime.strptime(s, '%Y-%m-%dT%H:%M:%SZ')


def unpack(src):
    result = copy.deepcopy(src)
    if 'cc_detail' in result:
        result['cc'] = [item['email'] for item in result['cc_detail']]
        del result['cc_detail']
    for field in ARRAY_TYPES:
        if field not in result or not result[field]:
            result[field] = []

    return result


class Bug(object):
    """This represents a Bugzilla Bug"""

    def __init__(self, bugsy=None, **kwargs):
        """
            Defaults are set if there are no kwargs passed in. To pass in
            a dict create the Bug object like the following

            :param bugsy: Bugsy instance to use to connect to Bugzilla.

            >>> bug = Bug(**myDict)
        """
        self._bugsy = bugsy
        self._bug = dict(**kwargs)
        self._copy = dict(**kwargs)
        self._bug['op_sys'] = kwargs.get('op_sys', 'All')
        self._bug['product'] = kwargs.get('product', 'core')
        self._bug['component'] = kwargs.get('component', 'general')
        self._bug['platform'] = kwargs.get('platform', 'All')
        self._bug['version'] = kwargs.get('version', 'unspecified')

    def __getattr__(self, attr):
        if attr not in self._bug:
            return None

        return self._bug[attr]

    def __setattr__(self, attr, value):
        if attr == '_bug' or attr == '_copy':
            object.__setattr__(self, attr, unpack(value))
        elif attr == '_bugsy':
            object.__setattr__(self, attr, value)
        elif attr == 'status':
            if self.id:
                if value in VALID_STATUS:
                    self._bug['status'] = value
                else:
                    raise BugException("Invalid status type was used")
            else:
                raise BugException("Can not set status unless there is a bug id."
                                   " Please call Update() before setting")
        elif attr == 'resolution':
            if value in VALID_RESOLUTION:
                self._bug['resolution'] = value
            else:
                raise BugException("Invalid resolution type was used")
        elif attr in ARRAY_TYPES and not isinstance(value, list):
            raise BugException("Cannot set value to non-list type")
        else:
            self._bug[attr] = copy.copy(value)

    def to_dict(self):
        """
            Return the raw dict that is used inside this object
        """
        return self._bug

    def update(self):
        """
            Update this object with the latest changes from Bugzilla

            >>> bug.status
            'NEW'
            #Changes happen on Bugzilla
            >>> bug.update()
            >>> bug.status
            'FIXED'
        """
        if 'id' in self._bug:
            result = self._bugsy.request('bug/%s' % self._bug['id'])
            self._bug = dict(**result['bugs'][0])
            self._copy = dict(**result['bugs'][0])
        else:
            raise BugException("Unable to update bug that isn't in Bugzilla")

    def get_comments(self):
        """
            Obtain comments for this bug.

            Returns a list of Comment instances.
        """
        bug = str(self._bug['id'])
        res = self._bugsy.request('bug/%s/comment' % bug)

        return [Comment(bugsy=self._bugsy, **comments) for comments
                in res['bugs'][bug]['comments']]

    def add_comment(self, comment):
        """
            Adds a comment to a bug. If the bug object does not have a bug ID
            (ie you are creating a bug) then you will need to also call `put`
            on the :class:`Bugsy` class.

            >>> bug.add_comment("I like sausages")
            >>> bugzilla.put(bug)

            If it does have a bug id then this will immediately post to the server

            >>> bug.add_comment("I like eggs too")

            More examples can be found at:
            https://github.com/AutomatedTester/Bugsy/blob/master/example/add_comments.py
        """
        # If we have a key post immediately otherwise hold onto it until
        # put(bug) is called
        if 'id' in self._bug:
            self._bugsy.request('bug/{}/comment'.format(self._bug['id']),
                                method='POST', json={"comment": comment}
                                )
        else:
            self._bug['comment'] = comment

    def get_attachments(self):
        """
            Obtain comments for this bug.

            Returns a list of Comment instances.
        """
        bug = str(self._bug['id'])
        res = self._bugsy.request(
            'bug/%s/attachment' % bug,
        )

        return [Attachment(bugsy=self._bugsy, **attachments) for attachments
                in res['bugs'][bug]]

    def add_attachment(self, attachment):
        if not self.id:
            raise BugException("Cannot add an attachment without a bug id")

        attach_dict = attachment.to_dict()
        missing = list(set(Attachment.CREATE_REQUIRED) - set(attach_dict.keys()))
        if missing:
            raise BugException("Cannot add attachment without all required fields")

        output = {'ids': [self.id]}
        for field in list(set(Attachment.CREATE_FIELDS) & set(attach_dict.keys())):
            output[field] = attach_dict[field]

        self._bugsy.request('bug/%s/attachment' % self._bug['id'],
                            method='POST', json=output)

    def diff(self):
        """
            Generates a dictionary containing only the changed values

            Special handling of ARRAY_TYPES fields is required to only PUT changed objects

            >>> bug.cc
            ['foo@bar.com']
            >>> bug.cc.append('abc@xyz.com')
            >>> bug.cc
            ['foo@bar.com', 'abc@xyz.com']
            >>>bug.diff()
            {'cc': {'added': ['abc@xyz.com']}}
        """
        changed = {}
        for key in self._bug:
            if key not in ARRAY_TYPES:
                if key not in self._copy or self._bug[key] != self._copy[key]:
                    changed[key] = self._bug[key]
            elif key == 'flags':
                if self._bug.get(key, []) != self._copy.get(key, []):
                    changed[key] = self._bug.get(key, [])
            else:
                values_now = set(self._bug.get(key, []))
                values_orig = set(self._copy.get(key, []))
                additions = list(values_now - values_orig)
                subtractions = list(values_orig - values_now)
                if additions or subtractions:
                    changed[key] = {}
                    if len(additions):
                        changed[key]['add'] = additions
                    if len(subtractions):
                        changed[key]['remove'] = subtractions
        return changed


class Comment(object):
    """
        Represents a single Bugzilla comment.

        To get comments you need to do the following

        >>> bugs = bugzilla.search_for.keywords("checkin-needed").search()
        >>> comments = bugs[0].get_comments()
        >>> # Returns the comment 0 of the first checkin-needed bug
        >>> comments[0].text
    """

    def __init__(self, bugsy=None, **kwargs):
        self._bugsy = bugsy
        kwargs['time'] = str2datetime(kwargs['time'])
        kwargs['creation_time'] = str2datetime(kwargs['creation_time'])
        if 'tags' in kwargs:
            kwargs['tags'] = set(kwargs['tags'])
        else:
            kwargs['tags'] = set()
        self._comment = kwargs

    @property
    def text(self):
        r"""
            Return the text that is in this comment

            >>> comment.text # David really likes cheese apparently

        """
        return self._comment['text']

    @property
    def id(self):
        r"""
            Return the comment id that is associated with Bugzilla.
        """
        return self._comment['id']

    @property
    def attachment_id(self):
        """
            If the comment was made on an attachment, return the ID of that
            attachment. Otherwise it will return None.
        """
        return self._comment['attachment_id']

    @property
    def author(self):
        """
            Return the login name of the comment's author.
        """
        return self._comment['author']

    @property
    def creator(self):
        """
            Return the login name of the comment's author.
        """
        return self._comment['creator']

    @property
    def bug_id(self):
        """
            Return the ID of the bug that this comment is on.
        """
        return self._comment['bug_id']

    @property
    def time(self):
        """
            This is exactly same as :attr:`creation_time`.

            For compatibility, time is still usable. However, please note
            that time may be deprecated and removed in a future release.

            Prefer :attr:`creation_time` instead.
        """
        return self._comment['time']

    @property
    def creation_time(self):
        """
            Return the time (in Bugzilla's timezone) that the comment was
            added.
        """
        return self._comment['creation_time']

    @property
    def is_private(self):
        """
            Return True if this comment is private (only visible to a certain
            group called the "insidergroup").
        """
        return self._comment['is_private']

    @property
    def tags(self):
        """
            Return a set of comment tags currently set for the comment.
        """
        return self._comment['tags']

    def add_tags(self, tags):
        """
            Add tags to the comments
        """
        if not isinstance(tags, list):
            tags = [tags]
        self._bugsy.request('bug/comment/%s/tags' % self._comment['id'],
                            method='PUT', json={"add": tags})

    def remove_tags(self, tags):
        """
            Add tags to the comments
        """
        if not isinstance(tags, list):
            tags = [tags]
        self._bugsy.request('bug/comment/%s/tags' % self._comment['id'],
                            method='PUT', json={"remove": tags})
