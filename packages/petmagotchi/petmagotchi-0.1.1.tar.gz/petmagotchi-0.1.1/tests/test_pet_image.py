import unittest
from unittest.mock import patch
from petmagotchi.pet import Pet

class TestPet(unittest.TestCase):
    def setUp(self):
        self.petCat = Pet(name="MeowMeow", type="Cat")
        self.petDog = Pet(name="BarkBark", type="Dog")
    
    # test image open cat
    def test_image_open_cat(self):
        self.petCat.mood_level = 0
        try:
            img = self.petCat.see_pet()
        except Exception:
            self.fail("Getting 'upset' image failed...")
        self.assertEqual(img.filename, "src/images/cat/cat_upset.png")
        
        self.petCat.mood_level = 30
        try:
            img = self.petCat.see_pet()
        except Exception:
            self.fail("Getting 'neutral' image failed...")
        self.assertEqual(img.filename, "src/images/cat/cat_neutral.png")
        
        self.petCat.mood_level = 80
        try:
            img = self.petCat.see_pet()
        except Exception:
            self.fail("Getting 'happy' image failed...")
        self.assertEqual(img.filename, "src/images/cat/cat_happy.png")
        

    # test image open dog
    def test_image_open_dog(self):
        self.petDog.mood_level = 0
        try:
            img = self.petDog.see_pet()
        except Exception:
            self.fail("Getting 'upset' image failed...")
        self.assertEqual(img.filename, "src/images/dog/dog_upset.png")
        
        self.petDog.mood_level = 30
        try:
            img = self.petDog.see_pet()
        except Exception:
            self.fail("Getting 'neutral' image failed...")
        self.assertEqual(img.filename, "src/images/dog/dog_neutral.png")
        
        self.petDog.mood_level = 80
        try:
            img = self.petDog.see_pet()
        except Exception:
            self.fail("Getting 'happy' image failed...")
        self.assertEqual(img.filename, "src/images/dog/dog_happy.png")