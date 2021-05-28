""" Parse each test vector, and compare them to known-good values. """
import myloginpath


def test_normal():
    expected = {
        "host": "testhost",
        "password": "testpass",
        "port": 1234,
        "socket": "testsocket",
        "user": "testuser",
    }
    actual = myloginpath.parse("test", "test/test.mylogin.cnf")
    assert expected == actual


def test_quoted():
    expected = {
        "host": "testhost",
        "password": "testpass",
        "port": 1234,
        "socket": "testsocket",
        "user": "testuser",
    }
    actual = myloginpath.parse("test", "test/test_quoted.mylogin.cnf")
    assert expected == actual


def test_special():
    expected = {"host": 'host with " quote'}
    actual = myloginpath.parse("test", "test/test_special.mylogin.cnf")
    assert expected == actual
