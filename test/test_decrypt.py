""" Read each test vector, decrypt, and check that they're correct."""
import myloginpath


def test_normal():
    expected = """[test]
user = testuser
password = testpass
host = testhost
socket = testsocket
port = 1234
"""
    actual = myloginpath.read("test/test.mylogin.cnf")
    assert expected == actual


def test_quoted():
    expected = """[test]
user = "testuser"
password = "testpass"
host = "testhost"
socket = "testsocket"
port = 1234
"""
    actual = myloginpath.read("test/test_quoted.mylogin.cnf")
    assert expected == actual


def test_special():
    expected = """[test]
host = "host with \\" quote"
"""
    actual = myloginpath.read("test/test_special.mylogin.cnf")
    assert expected == actual
