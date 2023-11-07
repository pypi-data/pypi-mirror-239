import unittest
import os
from petmagotchi.pet import Pet

class TestLoadPet(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_pet_name = 'Furry Cat'
        cls.pet = Pet(name=cls.test_pet_name, type = 'Cat')
        cls.pet.save_pet()
        cls.file_path = f"{cls.test_pet_name.replace(' ', '_')}.pickle"

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.file_path):
            os.remove(cls.file_path)

    def test_load_existing_pet(self):
        loaded_pet = Pet.load_pet(self.file_path)
        self.assertEqual(loaded_pet.name, self.test_pet_name)

    def test_load_nonexistent_pet(self):
        with self.assertRaises(FileNotFoundError):
            Pet.load_pet("nonexistent_pet.pickle")

    def test_load_pet_incorrect_file_extension(self):
        with self.assertRaises(FileNotFoundError):
            Pet.load_pet("Test_Pet.txt")