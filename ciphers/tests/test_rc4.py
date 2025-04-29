# PR - Add rc4 cipher #12687 

import unittest
from ciphers.rc4 import ksa, prga, rc4

class TestRC4(unittest.TestCase):
    def test_ksa(self):
        # Testa o KSA com uma chave conhecida
        key = b"Key"
        expected_s_box_start = [75, 51, 132, 157, 192]  
        s_box = ksa(key)
        self.assertEqual(s_box[:5], expected_s_box_start)

    def test_prga(self):
        # Testa o PRGA com uma S-box conhecida
        s_box = list(range(256))
        keystream = prga(s_box, 5)
        expected_keystream = [2, 5, 7, 13, 13]  
        self.assertEqual(keystream, expected_keystream)

    def test_rc4_encryption_decryption(self):
        # Testa a criptografia e descriptografia com RC4
        key = b"Key"
        plaintext = b"Plaintext"
        ciphertext = rc4(key, plaintext)
        decrypted = rc4(key, ciphertext)
        self.assertNotEqual(ciphertext, plaintext)  # Garante que a criptografia altera os dados
        self.assertEqual(decrypted, plaintext)      # Garante que a descriptografia restaura os dados

    def test_rc4_with_empty_input(self):
        # Testa o RC4 com entrada vazia
        key = b"Key"
        data = b""
        result = rc4(key, data)
        self.assertEqual(result, b"")

    def test_rc4_with_non_ascii_key(self):
        # Testa o RC4 com uma chave não-ASCII
        key = b"\xff\xfe\xfd"
        plaintext = b"Test"
        ciphertext = rc4(key, plaintext)
        decrypted = rc4(key, ciphertext)
        self.assertEqual(decrypted, plaintext)


if __name__ == "__main__":
    unittest.main()
