import base64
import hashlib
import binascii
from Crypto.Cipher import AES
import sys
import os
import platform


platform_string = None


def encrypt(secret, password):
    '''
    Encrypts the specified secret using the specified password.
    '''

    # pylint: disable=E1101
    hashed_pass = hashlib.sha512(password.encode('utf-8')).digest()
    crypt_key = hashed_pass[:32]
    crypt_ini = hashed_pass[-16:]
    aes = AES.new(crypt_key, AES.MODE_OFB, crypt_ini)

    # since the secret is a base64 string we can just just pad it with
    # spaces which can easily be stripped again after decryping
    secret += ' ' * (16 - len(secret) % 16)
    return base64.b64encode(aes.encrypt(secret)).decode('ascii')


def decrypt(secret, password):
    '''
    Decrypts the specified key using the specified password,
    throws exception in case of failure.
    '''

    if secret == '':
        raise Exception('secret cannot be empty')

    # pylint: disable=E1101
    hashed_pass = hashlib.sha512(password.encode('utf-8')).digest()
    crypt_key = hashed_pass[:32]
    crypt_ini = hashed_pass[-16:]
    aes = AES.new(crypt_key, AES.MODE_OFB, crypt_ini)
    encrypted_secret = base64.b64decode(secret.strip().encode('ascii'))
    secret = aes.decrypt(encrypted_secret).strip()

    # is it plain ascii? (if not this will raise exception)
    dummy = secret.decode('ascii')
    # can it be decoded? correct size afterwards?
    if len(base64.b64decode(secret)) != 64:
        raise Exception('decrypted secret has wrong size')

    return secret


def assert_valid_key(key):
    '''
    Asserts that the specified key is valid,
    throws an exception otherwise.
    '''

    if key == '':
        raise Exception('key cannot be empty')

    # key must be only hex digits and have the right size
    key = key.strip()
    hex_key = key.replace('-', '').encode('ascii')
    if len(binascii.unhexlify(hex_key)) != 16:
        raise Exception('key has wrong size')


def assert_valid_secret(secret):
    '''
    Asserts that the specified secret is valid,
    throws an exception otherwise.
    '''
    result = decrypt(encrypt(secret, 'foo'), 'foo')
    if result != secret:
        raise Exception('encryption / decryption test failed.')


def resource_path(relative_path):
    '''
    Get absolute path to resource, works for dev and for PyInstaller.
    Taken from: http://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile # @IgnorePep8
    '''
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = getattr(sys, '_MEIPASS', os.getcwd())
    except Exception:
        base_path = os.path.abspath('.')

    return os.path.join(base_path, relative_path)


def get_platform():
    global platform_string
    if platform_string == None:
        platform_string = platform.system()

    return platform_string


def platform_is_mac():
    '''
    Returns true if the current platform is mac.
    '''
    return get_platform() == 'Darwin'
