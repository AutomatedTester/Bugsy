from bugsy.flags import NeedInfo

def test_can_create_needinfo():
    ni = NeedInfo(requestee = "automatedtester@mozilla.com")
    assert ni.status == "?"
