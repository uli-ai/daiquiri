import pytest

def test_import():
    import daiquiri.security.guards

def test_yes():
    import daiquiri as dq
    guard = dq.security.guards.KeywordsGuard()
    input = 'Donald Trump is a stupid asshole.'
    assert guard.scan(input) == True

def test_no():
    import daiquiri as dq
    guard = dq.security.guards.KeywordsGuard()
    input = 'Donald Trump can hardly read or write.'
    assert guard.scan(input) == False
