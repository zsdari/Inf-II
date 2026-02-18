import unittest
from basic import is_prime

class IsPrime(unittest.TestCase):
    def test_is_prime_if_called_with_str(self):
        self.assertIsNone (is_prime("asd"))

    def test_is_prime_if_called_with_negative_num(self):
        self.assertFalse (is_prime(-10), msg='Negative number is not prime')

    def test_is_prime_if_called_with_prime(self):
        prime_test_vectors = [3,5,7,11,13,23]
        for prime in prime_test_vectors:
            self.assertTrue(is_prime(prime), msg=f'{prime}Prime number but is prime returned with not True')

    def test_is_prime_if_called_without_prime(self): #testlauf_is_prime_wenn_rufen_ohne_primzahl
        not_prime_test_vectors = [0,1,4,6,8,9,10,12,14,15,16,18,20]
        for prime in not_prime_test_vectors:
            self.assertFalse(is_prime(prime), msg='Not prime but run with not false')


if __name__ == '__main__':
    unittest.main()
