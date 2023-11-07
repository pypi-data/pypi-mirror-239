import unittest
from unittest.mock import patch
from petmagotchi.pet import Pet

class TestPet(unittest.TestCase):
    def setUp(self):
        self.pet = Pet(name="Spot", type="Dog")
        
    def test_wash(self):
        self.pet.sanitation_level = 100
        self.pet.wash()
        self.assertEqual(self.pet.sanitation_level, 100)