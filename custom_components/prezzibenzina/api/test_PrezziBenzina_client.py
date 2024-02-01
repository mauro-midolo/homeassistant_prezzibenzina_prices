from PrezziBenzina_client import prezzibenzina_client
from PrezziBenzina import PrezziBenzina

import unittest


class TestPrezziBenzina(unittest.TestCase):

    def setUp(self):
        pass

    def test_exists_true(self):
        self.assertTrue(prezzibenzina_client().id_exists("6106"))
    
    def test_exists_false(self):
        self.assertFalse(prezzibenzina_client().id_exists("Not_exists"))

    def test_get_name(self):
        prezzi_benzina: PrezziBenzina = prezzibenzina_client().retrive_info("6106")
        self.assertEqual(prezzi_benzina.get_name(), "Distributore - San Lazzaro di Savena Via Poggi")

    def test_get_street(self):
        prezzi_benzina: PrezziBenzina = prezzibenzina_client().retrive_info("6106")
        self.assertEqual(prezzi_benzina.get_street(),
                         "Via Paolo Poggi 4, 40068 San Lazzaro di Savena (BO)")

    def test_get_values(self):
        prezzi_benzina: PrezziBenzina = prezzibenzina_client().retrive_info("6106")
        result: list = prezzi_benzina.get_values()
        self.assertTrue(result)

    def test_values_are_int(self):
        prezzi_benzina: PrezziBenzina = prezzibenzina_client().retrive_info("6106")
        result = prezzi_benzina.get_values()[0]
        self.assertEqual(type(result['price']), float)


if __name__ == '__main__':
    unittest.main()
