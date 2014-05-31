from bugzilla import Bug

def test_can_create_bug_and_set_summary_afterwards():
    bug = Bug()
    assert bug.summary == '', "Summary is not set to nothing on plain initialisation"
    bug.summary = "Foo"
    assert bug.summary == 'Foo', "Summary is not being set"
