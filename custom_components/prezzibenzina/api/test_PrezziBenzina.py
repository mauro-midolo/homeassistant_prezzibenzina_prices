from PrezziBenzina import PrezziBenzina

import unittest

class TestPrezziBenzina(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_name(self):
        prezzi_benzina = PrezziBenzina("Example Name", "Example Street", "Example Values")
        self.assertEqual(prezzi_benzina.get_name(), "Example Name")

    def test_get_street(self):
        prezzi_benzina = PrezziBenzina("Example Name", "Example Street", "Example Values")
        self.assertEqual(prezzi_benzina.get_street(), "Example Street")

    def test_get_values(self):
        prezzi_benzina = PrezziBenzina("Example Name", "Example Street", "Example Values")
        self.assertEqual(prezzi_benzina.get_values(), "Example Values")

if __name__ == '__main__':
    unittest.main()