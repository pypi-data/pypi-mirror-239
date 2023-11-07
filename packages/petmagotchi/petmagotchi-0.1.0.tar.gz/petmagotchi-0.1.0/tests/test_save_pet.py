import unittest
import os
import pickle
from petmagotchi.pet import Pet  # Make sure to import your Pet class from the correct file

class TestSavePetFunction(unittest.TestCase):

    def setUp(self):
        """ Set up a pet object for use in tests """
        self.pet = Pet(name='Buddy Boy', type = 'Dog')
        self.filename = f"{self.pet.name.replace(' ', '_')}.pickle"

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_save_pet_creates_file(self):
        self.pet.save_pet()
        self.assertTrue(os.path.exists(self.filename))

    def test_save_pet_creates_non_empty_file(self):
        self.pet.save_pet()
        self.assertTrue(os.path.exists(self.filename))
        self.assertGreater(os.stat(self.filename).st_size, 0)

    def test_save_pet_with_invalid_name(self):
        self.pet.name = "Invalid/Name\\Test"  
        with self.assertRaises(ValueError):
            self.pet.save_pet()  