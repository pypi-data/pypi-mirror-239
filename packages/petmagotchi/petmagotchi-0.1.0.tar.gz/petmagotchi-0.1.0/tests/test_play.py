import unittest
from unittest.mock import patch
from petmagotchi.pet import Pet

class TestPet(unittest.TestCase):
    def setUp(self):
        self.pet = Pet(name="Rocky", type="Dog")
    
    # play no string
    def test_play_no_string(self):
        with self.assertRaises(ValueError):
            self.pet.play(123)
    
    # play invalid string
    def test_play_invalid_toy(self):
        with self.assertRaises(Pet.InvalidToyError):
            self.pet.play("invalid")
    
    # play valid string
    def test_play_valid_toy(self):
        self.pet.get_status()
        initial_mood_level = self.pet.mood_level
        self.pet.play("ball")
        self.assertGreater(self.pet.mood_level, initial_mood_level)
    
    # play favorite toy, not max mood
    def test_play_favorite_toy_not_max_mood(self):
        self.pet.get_status()
        self.pet.mood_level = 50
        self.pet.energy_level = 50
        
        initial_mood_level = self.pet.mood_level
        initial_energy_level = self.pet.energy_level
        
        self.pet.play(self.pet.favoriteToy)
        self.assertGreaterEqual(self.pet.mood_level - initial_mood_level, Pet.TOYS[self.pet.favoriteToy] * 2)
        self.assertLess(self.pet.energy_level, initial_energy_level)
    
    # play max mood
    def test_play_max_mood(self):
        self.pet.get_status()
        self.pet.mood_level = 100
        self.pet.energy_level = 50
        
        initial_energy_level = self.pet.energy_level
        
        self.pet.play("ball")
        self.assertEqual(self.pet.mood_level, 100)
        self.assertLess(self.pet.energy_level, initial_energy_level)
    
    # check too tired
    def test_play_too_tired(self):
        self.pet.energy_level = 0
        initial_mood_level = self.pet.mood_level
        initial_energy_level = self.pet.energy_level
        self.pet.play("ball")
        self.assertEqual(self.pet.energy_level, initial_energy_level)
        self.assertEqual(self.pet.mood_level, initial_mood_level)