import bugsy
from bugsy import Bugsy, BugsyException, LoginException
from bugsy import Bug
try:
    from unittest.mock import Mock, MagicMock, patch
except:
    from mock import Mock, MagicMock, patch
import responses
import json

@responses.activate
def test_we_only_ask_for_the_include_fields():
  include_return = {
   "bugs" : [
      {
         "product" : "MozillaClassic",
         "summary" : "Bookmark properties leads to an Assert  failed"
      }
   ],
   "faults" : []
  }
  responses.add(responses.GET, 'https://bugzilla.mozilla.org/rest/bug?include_fields=product',
                    body=json.dumps(include_return), status=200,
                    content_type='application/json', match_querystring=True)

  bugzilla = Bugsy()
  bugs = bugzilla.search_for\
          .include_fields('product')\
          .search()

  assert len(responses.calls) == 1
  assert len(bugs) == 1
  assert bugs[0].product == include_return['bugs'][0]['product']

@responses.activate
def test_we_only_ask_for_the_include_fields_while_logged_in():
  include_return = {
   "bugs" : [
      {
         "product" : "MozillaClassic",
         "summary" : "Bookmark properties leads to an Assert  failed"
      }
   ],
   "faults" : []
  }
  responses.add(responses.GET, 'https://bugzilla.mozilla.org/rest/login?login=foo&password=bar',
                    body='{"token": "foobar"}', status=200,
                    content_type='application/json', match_querystring=True)

  responses.add(responses.GET, 'https://bugzilla.mozilla.org/rest/bug?include_fields=product&token=foobar',
                    body=json.dumps(include_return), status=200,
                    content_type='application/json', match_querystring=True)

  bugzilla = Bugsy('foo', 'bar')
  bugs = bugzilla.search_for\
          .include_fields('product')\
          .search()

  assert len(responses.calls) == 2
  assert len(bugs) == 1
  assert bugs[0].product == include_return['bugs'][0]['product']

@responses.activate
def test_we_can_return_keyword_search():
    keyword_return = {
      "bugs" : [
      {
         "component" : "Networking: HTTP",
         "product" : "Core",
         "summary" : "IsPending broken for requests without Content-Type"
      },
      {
         "component" : "Developer Tools: Graphic Commandline and Toolbar",
         "product" : "Firefox",
         "summary" : "GCLI Command to open Profile Directory"
      },
      {
         "component" : "Video/Audio Controls",
         "product" : "Toolkit",
         "summary" : "Fullscreen video should disable screensaver during playback on Linux"
      },
      {
         "component" : "Reader Mode",
         "product" : "Firefox for Android",
         "summary" : "Article showing twice in reader mode"
      },
      {
         "component" : "Message Reader UI",
         "product" : "Thunderbird",
         "summary" : "Make \"visited link\" coloring work in thunderbird"
      }]
    }

    responses.add(responses.GET, 'https://bugzilla.mozilla.org/rest/bug?include_fields=product&include_fields=component&keywords=checkin-needed&',
                    body=json.dumps(keyword_return), status=200,
                    content_type='application/json', match_querystring=True)

    bugzilla = Bugsy()
    bugs = bugzilla.search_for\
            .include_fields('product', "component")\
            .keywords('checkin-needed')\
            .search()

    assert len(responses.calls) == 1
    assert len(bugs) == 5
    assert bugs[0].product == keyword_return['bugs'][0]['product']
    assert bugs[0].component == keyword_return['bugs'][0]['component']

@responses.activate
def test_that_we_can_search_for_a_specific_user():
    user_return = {
        "bugs" : [
            {
              "product" : "addons.mozilla.org",
               "summary" : "Add Selenium tests to the repository"
            },
            {
               "product" : "addons.mozilla.org",
               "summary" : "Add Ids to links to help with testability"
            },
            {
               "product" : "addons.mozilla.org",
               "summary" : "Add a name for AMO Themes sort links for testability"
            },
            {
               "product" : "addons.mozilla.org",
               "summary" : "Missing ID for div with class \"feature ryff\" (Mobile Add-on: Foursquare)"
            }
           ]
        }
    responses.add(responses.GET, 'https://bugzilla.mozilla.org/rest/bug?include_fields=product&include_fields=summary&assigned_to=dburns@mozilla.com&',
                    body=json.dumps(user_return), status=200,
                    content_type='application/json', match_querystring=True)

    bugzilla = Bugsy()
    bugs = bugzilla.search_for\
            .include_fields('product', "summary")\
            .assigned_to('dburns@mozilla.com')\
            .search()

    assert len(responses.calls) == 1
    assert len(bugs) == 4
    assert bugs[0].product == user_return['bugs'][0]['product']
    assert bugs[0].summary == user_return['bugs'][0]['summary']

@responses.activate
def test_we_can_search_summary_fields():
    summary_return = {
     "bugs" : [
        {
           "component" : "CSS Parsing and Computation",
           "product" : "Core",
           "summary" : "Map \"rebeccapurple\" to #663399 in named color list."
        }
      ]
    }


    responses.add(responses.GET, 'https://bugzilla.mozilla.org/rest/bug?assigned_to=dburns@mozilla.com&short_desc=rebecca&short_desc_type=allwordssubstr&include_fields=summary&include_fields=product&include_fields=component&',
                    body=json.dumps(summary_return), status=200,
                    content_type='application/json', match_querystring=True)

    bugzilla = Bugsy()
    bugs = bugzilla.search_for\
            .include_fields("summary", 'product', "component")\
            .assigned_to('dburns@mozilla.com')\
            .summary("rebecca")\
            .search()

    assert len(responses.calls) == 1
    assert len(bugs) == 1
    assert bugs[0].product == summary_return['bugs'][0]['product']
    assert bugs[0].summary == summary_return['bugs'][0]['summary']


@responses.activate
def test_we_can_search_whiteboard_fields():
    whiteboard_return = {
       "bugs" : [
          {
             "component" : "Marionette",
             "product" : "Testing",
             "summary" : "Tracking bug for uplifting is_displayed issue fix for WebDriver"
          },
          {
             "component" : "Marionette",
             "product" : "Testing",
             "summary" : "Marionette thinks that the play button in the music app is not displayed"
          }
       ]
    }


    responses.add(responses.GET, 'https://bugzilla.mozilla.org/rest/bug?assigned_to=dburns@mozilla.com&whiteboard=affects&short_desc_type=allwordssubstr&include_fields=summary&include_fields=product&include_fields=component&',
                    body=json.dumps(whiteboard_return), status=200,
                    content_type='application/json', match_querystring=True)

    bugzilla = Bugsy()
    bugs = bugzilla.search_for\
            .include_fields("summary", 'product', "component")\
            .assigned_to('dburns@mozilla.com')\
            .whiteboard("affects")\
            .search()

    assert len(responses.calls) == 1
    assert len(bugs) == 2
    assert bugs[0].product == whiteboard_return['bugs'][0]['product']
    assert bugs[0].summary == whiteboard_return['bugs'][0]['summary']