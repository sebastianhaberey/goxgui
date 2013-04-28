import unittest
import utilities


class Test(unittest.TestCase):

    def test_assert_valid_key_ok(self):
        utilities.assert_valid_key('fd8484c6-e826-418f-b1ef-2d120a77bb88')
        utilities.assert_valid_key('25685451-0602-418e-8cee-14f4f01647ed')

    def test_assert_valid_key_empty(self):
        self.assertRaises(Exception,
                          utilities.assert_valid_key,
                          '')

    def test_assert_valid_key_short(self):
        self.assertRaises(Exception,
                          utilities.assert_valid_key,
                          'b')

    def test_assert_valid_key_nohex(self):
        self.assertRaises(Exception,
                          utilities.assert_valid_key,
                          'fd8484x6-e826-418f-b1ef-2d120a77bb88')

    def test_encrypt_decrypt_ok(self):
        text = '/GU3lmrgX9LCG7cIpGySlgVIVT8t8CKn3p/uayvc57Z98UhYJYy4/eIdEvi5VSuFd/vwMTroy8ELc5VbqWdQWg==' # @IgnorePep8
        password = 'bar'
        encrypted = utilities.encrypt(text, password)
        self.assertEqual(text, utilities.decrypt(encrypted, password))

    def test_encrypt_decrypt_wrong_password(self):
        text = '/GU3lmrgX9LCG7cIpGySlgVIVT8t8CKn3p/uayvc57Z98UhYJYy4/eIdEvi5VSuFd/vwMTroy8ELc5VbqWdQWg==' # @IgnorePep8
        encrypted = utilities.encrypt(text, 'bar')
        self.assertRaises(Exception, utilities.decrypt, encrypted, 'foo')
