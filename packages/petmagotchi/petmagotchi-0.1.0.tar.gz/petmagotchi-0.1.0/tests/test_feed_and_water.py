import unittest
from unittest.mock import patch
from petmagotchi.pet import Pet

class TestPet(unittest.TestCase):

    def setUp(self):
        self.pet = Pet(name="Fluffy", type="Cat")

    def test_feed_pet_valid_food(self):
        self.pet.get_status()
        initial_food_level = self.pet.food_level
        initial_mood_level = self.pet.mood_level
        self.pet.feed_pet("meat", 2)
        self.assertGreater(self.pet.food_level, initial_food_level)
        self.assertGreater(self.pet.mood_level, initial_mood_level)

    def test_feed_pet_invalid_food(self):
        with self.assertRaises(Pet.InvalidFoodError):
            self.pet.feed_pet("chocolate", 2)

    def test_feed_pet_invalid_quantity(self):
        with self.assertRaises(Pet.InvalidQuantityError):
            self.pet.feed_pet("meat", 5)

    def test_feed_pet_exact_values(self):
        food = "meat"
        quantity = 2
        initial_food_level = self.pet.food_level
        initial_mood_level = self.pet.mood_level
        
        expected_food_increase = Pet.VALID_FOODS[food][0] * quantity
        expected_mood_increase = Pet.VALID_FOODS[food][1] * quantity

        self.pet.feed_pet(food, quantity)

        self.assertEqual(self.pet.food_level, min(initial_food_level + expected_food_increase,100))
        self.assertEqual(self.pet.mood_level, min(initial_mood_level + expected_mood_increase,100))


    def test_hydrate_pet_valid_drink(self):
        self.pet.get_status()
        initial_water_level = self.pet.water_level
        initial_mood_level = self.pet.mood_level
        self.pet.hydrate_pet("milk", 3)
        self.assertGreater(self.pet.water_level, initial_water_level)
        self.assertGreater(self.pet.mood_level, initial_mood_level)

    def test_hydrate_pet_invalid_drink(self):
        with self.assertRaises(Pet.InvalidDrinkError):
            self.pet.hydrate_pet("dogwater", 1)

    def test_hydrate_pet_invalid_quantity(self):
        with self.assertRaises(Pet.InvalidQuantityError):
            self.pet.hydrate_pet("lemonade", -1)
    
    def test_hydrate_pet_exact_values(self):
        drink = "milk"
        quantity = 2
        initial_water_level = self.pet.water_level
        initial_mood_level = self.pet.mood_level
        
        expected_water_increase = Pet.VALID_DRINKS[drink][0] * quantity
        expected_mood_increase = Pet.VALID_DRINKS[drink][1] * quantity + (10 if drink == self.pet.favoriteDrink else 0)

        self.pet.hydrate_pet(drink, quantity)

        self.assertEqual(self.pet.water_level, min(initial_water_level + expected_water_increase,100))
        self.assertEqual(self.pet.mood_level, min(initial_mood_level + expected_mood_increase,100))