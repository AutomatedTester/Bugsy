import pytest


@pytest.fixture(scope="module")
def bug_return():
    return {
        u'faults': [],
        u'bugs': [{
            u'cf_tracking_firefox29': u'---',
            u'classification': u'Other',
            u'creator': u'jgriffin@mozilla.com',
            u'cf_status_firefox30': u'---',
            u'depends_on': [123456],
            u'cf_status_firefox32': u'---',
            u'creation_time': u'2014-05-28T23:57:58Z',
            u'product': u'Release Engineering',
            u'cf_user_story': u'',
            u'dupe_of': None,
            u'cf_tracking_firefox_relnote': u'---',
            u'keywords': [u'regression'],
            u'cf_tracking_b2g18': u'---',
            u'summary': u'Schedule Mn tests on opt Linux builds on cedar',
            u'id': 1017315,
            u'assigned_to_detail': {
                u'id': 347295,
                u'email': u'jgriffin@mozilla.com',
                u'name': u'jgriffin@mozilla.com',
                u'real_name': u'Jonathan Griffin (:jgriffin)'
            },
            u'severity': u'normal',
            u'is_confirmed': True,
            u'is_creator_accessible': True,
            u'cf_status_b2g_1_1_hd': u'---',
            u'qa_contact_detail': {
                u'id': 20203,
                u'email': u'catlee@mozilla.com',
                u'name': u'catlee@mozilla.com',
                u'real_name': u'Chris AtLee [:catlee]'
            },
            u'priority': u'--',
            u'platform': u'All',
            u'cf_crash_signature': u'',
            u'version': u'unspecified',
            u'cf_qa_whiteboard': u'',
            u'cf_status_b2g_1_3t': u'---',
            u'cf_status_firefox31': u'---',
            u'is_open': False,
            u'cf_blocking_fx': u'---',
            u'status': u'RESOLVED',
            u'cf_tracking_relnote_b2g': u'---',
            u'cf_status_firefox29': u'---',
            u'blocks': [654321],
            u'qa_contact': u'catlee@mozilla.com',
            u'see_also': [],
            u'component': u'General Automation',
            u'cf_tracking_firefox32': u'---',
            u'cf_tracking_firefox31': u'---',
            u'cf_tracking_firefox30': u'---',
            u'op_sys': u'All',
            u'groups': [],
            u'cf_blocking_b2g': u'---',
            u'target_milestone': u'---',
            u'is_cc_accessible': True,
            u'cf_tracking_firefox_esr24': u'---',
            u'cf_status_b2g_1_2': u'---',
            u'cf_status_b2g_1_3': u'---',
            u'cf_status_b2g18': u'---',
            u'cf_status_b2g_1_4': u'---',
            u'url': u'',
            u'creator_detail': {
                u'id': 347295,
                u'email': u'jgriffin@mozilla.com',
                u'name': u'jgriffin@mozilla.com',
                u'real_name': u'Jonathan Griffin (:jgriffin)'
            },
            u'whiteboard': u'',
            u'cf_status_b2g_2_0': u'---',
            u'cc_detail': [{
                u'id': 30066,
                u'email': u'coop@mozilla.com',
                u'name': u'coop@mozilla.com',
                u'real_name': u'Chris Cooper [:coop]'
            },
                {
                    u'id': 397261,
                    u'email': u'dburns@mozilla.com',
                    u'name': u'dburns@mozilla.com',
                    u'real_name': u'David Burns :automatedtester'
                },
                {
                    u'id': 438921,
                    u'email': u'jlund@mozilla.com',
                    u'name': u'jlund@mozilla.com',
                    u'real_name': u'Jordan Lund (:jlund)'
                },
                {
                    u'id': 418814,
                    u'email': u'mdas@mozilla.com',
                    u'name': u'mdas@mozilla.com',
                    u'real_name': u'Malini Das [:mdas]'
                }
            ],
            u'alias': None,
            u'cf_tracking_b2g_v1_2': u'---',
            u'cf_tracking_b2g_v1_3': u'---',
            u'flags': [],
            u'assigned_to': u'jgriffin@mozilla.com',
            u'cf_status_firefox_esr24': u'---',
            u'resolution': u'FIXED',
            u'last_change_time': u'2014-05-30T21:20:17Z',
            u'cc': [u'coop@mozilla.com', u'dburns@mozilla.com', u'jlund@mozilla.com', u'mdas@mozilla.com'],
            u'cf_blocking_fennec': u'---'
        }]
    }


@pytest.fixture(scope="module")
def comments_return():
    return {
        u'bugs': {
            u'1017315': {
                u'comments': [
                    {
                        u'attachment_id': None,
                        u'author': u'gps@mozilla.com',
                        u'bug_id': 1017315,
                        u'creation_time': u'2014-03-27T23:47:45Z',
                        u'creator': u'gps@mozilla.com',
                        u'id': 8589785,
                        u'is_private': False,
                        u'raw_text': u'raw text 1',
                        u'tags': [u'tag1', u'tag2'],
                        u'text': u'text 1',
                        u'time': u'2014-03-27T23:47:45Z'
                    },
                    {
                        u'attachment_id': 8398207,
                        u'author': u'gps@mozilla.com',
                        u'bug_id': 1017315,
                        u'creation_time': u'2014-03-27T23:56:34Z',
                        u'creator': u'gps@mozilla.com',
                        u'id': 8589812,
                        u'is_private': True,
                        u'raw_text': u'raw text 2',
                        u'tags': [],
                        u'text': u'text 2',
                        u'time': u'2014-03-27T23:56:34Z'
                    },
                ],
            },
        },
    }


@pytest.fixture(scope="module")
def attachment_return():
    return {
        "bugs": {
            "1017315": [
                {
                    "is_private": 0,
                    "creator": "abc@xyz.com",
                    "bug_id": 1017315,
                    "last_change_time": "2019-09-18T18:31:57Z",
                    "size": 0,
                    "creator_detail": {},
                    "file_name": "file1.txt",
                    "summary": "File 1 summary",
                    "creation_time": "2017-03-02T17:21:23Z",
                    "id": 8842942,
                    "is_obsolete": 0,
                    "flags": [],
                    "data": "",
                    "description": "File 2 description",
                    "content_type": "text/html",
                    "attacher": "abc@xyz.com",
                    "is_patch": 0
                }
            ]
        }
    }
