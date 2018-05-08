# -*- coding: utf-8 -*-
"""Funtions that read and decrypt MySQL's login path file."""

from configparser import RawConfigParser
from io import BytesIO, TextIOWrapper
import os
import struct
import sys

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

VERSION = (0, 0, 1)

# Buffer at the beginning of the login path file.
_UNUSED_BUFFER_LENGTH = 4

# The key stored in the file.
_LOGIN_KEY_LENGTH = 20

# Number of bytes used to store the length of ciphertext.
_CIPHER_STORE_LENGTH = 4


def read(path=None) -> str:
    """Read contents of the login path file."""
    if path is None:
        path = _get_login_path_file()
    with open(path, "rb") as fp:
        return _read_encrypted_file(fp).decode()


def parse(login_path: str, path=None) -> dict:
    if path is None:
        path = _get_login_path_file()
    parser = RawConfigParser(
        dict_type=dict, allow_no_value=True, default_section="~~~UNUSED~~~"
    )
    parser.read_string(read(path), source=path)
    data = dict(parser.items(login_path))
    if 'port' in data:
        data['port'] = int(data['port'])
    return data


def _get_login_path_file():
    """Return the login path file's path or None if it doesn't exist."""
    file_path = os.getenv("MYSQL_TEST_LOGIN_FILE")
    if file_path:
        return file_path

    if sys.platform == "win32":
        file_path = os.path.join(getenv("APPDATA"), "MySQL", ".mylogin.cnf")
    else:
        file_path = os.path.join("~", ".mylogin.cnf")
    return os.path.expanduser(file_path)


def _read_key(fp):
    """Read the key from the login path file header."""
    # Move past the unused buffer.
    _buffer = fp.read(_UNUSED_BUFFER_LENGTH)

    if not _buffer or len(_buffer) != _UNUSED_BUFFER_LENGTH:
        # Login path file is blank or incomplete.
        return None

    return _create_key(fp.read(_LOGIN_KEY_LENGTH))


def _create_key(key):
    """Create the AES key from the login path file header."""
    rkey = bytearray(16)
    for i in range(len(key)):
        rkey[i % 16] ^= key[i]
    return bytes(rkey)


def _get_aes_cipher(key):
    """Get the AES cipher object."""
    return Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())


def _read_encrypted_file(f) -> bytes:
    """Decrypt a file *f*."""
    key = _read_key(f)
    cipher = _get_aes_cipher(key)
    decryptor = cipher.decryptor()

    plaintext = b""

    while True:
        # Read the length of the line.
        length_buffer = f.read(_CIPHER_STORE_LENGTH)
        if len(length_buffer) < _CIPHER_STORE_LENGTH:
            break
        line_length, = struct.unpack("<i", length_buffer)
        line = _read_line(f, line_length, decryptor)
        plaintext += line

    return plaintext


def _read_line(f, length, decryptor):
    """Read a line of length *length* from file *f* using *decryptor*."""
    line = f.read(length)
    return _remove_pad(decryptor.update(line))


def _remove_pad(line):
    """Remove the pad from the *line*."""
    try:
        pad_length = ord(line[-1:])
    except TypeError:
        # ord() was unable to get the value of the byte.
        return None

    if pad_length > len(line):
        # Pad length should be less than or equal to the length of the
        # plaintext.
        return None

    return line[:-pad_length]


if __name__ == "__main__":
    print(read())
    print(parse("test"))
