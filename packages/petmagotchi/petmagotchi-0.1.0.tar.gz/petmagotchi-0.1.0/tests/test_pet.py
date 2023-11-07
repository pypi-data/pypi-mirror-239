import unittest
from unittest.mock import patch
from petmagotchi.pet import Pet

class TestPet(unittest.TestCase):
    def setUp(self):
        self.pet = Pet(name="Mittins", type="Cat")
        
    # pet mood lower than 30
    def test_pet_mood_upset(self):
        self.pet.get_status()
        self.pet.mood_level = 10
        self.pet.pet()
        self.assertEqual(self.pet.mood_level, 10)
    
    # pet mood higher than 30
    def test_pet_not_upset(self):
        self.pet.get_status()
        self.pet.mood_level = 50
        self.pet.pet()
        self.assertGreater(self.pet.mood_level, 50)