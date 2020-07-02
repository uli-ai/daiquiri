import pytest

def test_import():
    import daiquiri.security.guards

def test_yes():
    import daiquiri as dq
    guard = dq.security.guards.ImportGuard()
    input = 'Donald Trump is a stupid asshole.'
    assert guard.scan(input) == True

def test_no():
    import daiquiri as dq
    guard = dq.security.guards.ImportGuard()
    input = 'import os'
    assert guard.scan(input) == False
