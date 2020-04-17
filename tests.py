import unittest

from pyw import ProveMyWorth


class ProveMyWorthTestCase(unittest.TestCase):
    def test_execution(self):
        pmw = ProveMyWorth()
        pmw.request_start()
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
