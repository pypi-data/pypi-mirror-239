import pytest
import random
from io import StringIO
from petmagotchi.pet import Pet
from unittest.mock import patch, Mock

class TestPet:
    def setup_method(self):
        self.pet = Pet(name="Yuka", type="Cat")

    #helper mock function
    def mocked_update_status(self):
        self.pet.food_level = 10
        self.pet.water_level = 20
        self.pet.energy_level = 50
        self.pet.sanitation_level = 30
        self.pet.mood_level = 40
    
    #tests constructor
    def test_pet_creation(self):
        assert isinstance(self.pet.name,str)
        assert isinstance(self.pet.type,str)
        assert 55 <= self.pet.food_level <= 80
        assert 55 <= self.pet.water_level <= 80
        assert 55 <= self.pet.sanitation_level <= 80
        assert self.pet.mood_level == 90

    def test_invalid_pet_creation(self):
        with pytest.raises(ValueError):
            Pet(name=123,type="Cat")
        with pytest.raises(ValueError):
            Pet(name="Yuka",type=123)
    
    def test_pet_creation_boundary_values(self):
        pets = [Pet(name="Test",type="Cat") for _ in range(1000)]
        food_levels = [pet.food_level for pet in pets]
        water_levels = [pet.water_level for pet in pets]
        sanitation_levels = [pet.sanitation_level for pet in pets]
        mood_levels = [pet.mood_level for pet in pets]
        assert min(food_levels) == 55
        assert max(food_levels) == 80 
        assert min(water_levels) == 55
        assert max(water_levels) == 80
        assert min(sanitation_levels) == 55
        assert max(sanitation_levels) == 80
        assert min(mood_levels) == 90
        assert max(mood_levels) == 90
    
    #tests get_mood
    def test_mood_status(self):
        self.pet.mood_level = 0
        assert self.pet.get_mood() == f"{self.pet.name} is upset..."
        
        self.pet.mood_level = 30
        assert self.pet.get_mood() == f"{self.pet.name} is feeling ok..."

        self.pet.mood_level = 80
        assert self.pet.get_mood() == f"{self.pet.name} is excited and happy to be with you!"

    def test_mood_boundaries(self):
        boundaries = [0, 29, 30, 79, 80, 100]
        expected_responses = [
            f"{self.pet.name} is upset...",
            f"{self.pet.name} is upset...",
            f"{self.pet.name} is feeling ok...",
            f"{self.pet.name} is feeling ok...",
            f"{self.pet.name} is excited and happy to be with you!",
            f"{self.pet.name} is excited and happy to be with you!"
        ]
        for i, boundary in enumerate(boundaries):
            self.pet.mood_level = boundary
            assert self.pet.get_mood() == expected_responses[i]
    
    def test_randomized_mood_status(self):
        mood_ranges = {
            (0, 29): f"{self.pet.name} is upset...",
            (30, 79): f"{self.pet.name} is feeling ok...",
            (80, 100): f"{self.pet.name} is excited and happy to be with you!"
        }

        for mood_range, expected_mood in mood_ranges.items():
            for i in range(1000):
                random_mood = random.randint(mood_range[0], mood_range[1])
                self.pet.mood_level = random_mood
                assert self.pet.get_mood() == expected_mood

    #Test get_status
    def test_get_status_without_actual_update(self):
        mock_update_status = Mock()
        with patch.object(Pet, '_update_status', mock_update_status):
            status = self.pet.get_status()
        mock_update_status.assert_called_once()
        assert status["Hunger"] == self.pet.food_level
        assert status["Thirst"] == self.pet.water_level
        assert status["Energy"] == self.pet.energy_level
        assert status["Cleanliness"] == self.pet.sanitation_level
        assert status["Mood"] == self.pet.get_mood()
        assert status["Favorite Toy"] == self.pet.favoriteToy

    def test_get_status_with_mocked_update(self):
        with patch.object(Pet, '_update_status', side_effect=self.mocked_update_status):
            status = self.pet.get_status()

        assert status["Hunger"] == 10
        assert status["Thirst"] == 20
        assert status["Cleanliness"] == 30
        assert status["Energy"] == 50
        assert status["Mood"] == self.pet.get_mood()


    #Test update_status
    def test_update_status_value_decrease(self):
        starting_time = 0
        jump = 3600
        with patch('time.time', return_value=starting_time):
            self.pet = Pet(name="Yuka", type="Cat")
            self.pet._update_status()
            initial_food = self.pet.food_level
            initial_water = self.pet.water_level
            initial_sanitation = self.pet.sanitation_level
            initial_energy = self.pet.energy_level
            initial_mood = self.pet.mood_level

        with patch('time.time', return_value=starting_time + jump):
            self.pet._update_status()
            updated_food = self.pet.food_level
            updated_water = self.pet.water_level
            updated_sanitation = self.pet.sanitation_level
            updated_energy = self.pet.energy_level
            updated_mood = self.pet.mood_level

        assert updated_food < initial_food
        assert updated_water < initial_water
        assert updated_sanitation < initial_sanitation
        assert updated_energy > initial_energy
        assert updated_mood < initial_mood
        

    def test_exact_status_update_values(self):
        starting_time = 0
        jump = 3600  # 1 hour
        with patch('time.time', return_value=starting_time):
            self.pet = Pet(name="Yuka", type="Cat")
            initial_food = self.pet.food_level
            initial_water = self.pet.water_level
            initial_sanitation = self.pet.sanitation_level
            initial_energy = self.pet.energy_level
            initial_mood = self.pet.mood_level

        expected_food_change = (jump / 1800) * Pet.HUNGER_RATE
        expected_water_change = (jump / 1800) * Pet.THIRST_RATE
        expected_sanitation_change = (jump / 1800) * Pet.CLEANLINESS_RATE
        expected_energy_change = (jump / 1800) * Pet.ENERGY_RATE
        expected_mood_change = (jump / 1800) * Pet.MOOD_RATE

        with patch('time.time', return_value=starting_time + jump):
            updated_status = self.pet.get_status()

        assert self.pet.food_level == max(round(initial_food - expected_food_change), 0)
        assert self.pet.water_level == max(round(initial_water - expected_water_change), 0)
        assert self.pet.sanitation_level == max(round(initial_sanitation - expected_sanitation_change), 0)
        assert self.pet.energy_level == min(round(initial_energy + expected_energy_change), 100)
        assert self.pet.mood_level == max(round(initial_mood - expected_mood_change), 0)


    def test_minimum_status_values_after_large_time_jump(self):
        starting_time = 0
        large_jump = 10000000
        with patch('time.time', return_value=starting_time):
            self.pet = Pet(name="Yuka", type="Cat")

        with patch('time.time', return_value=starting_time + large_jump):
            self.pet._update_status()

        assert self.pet.food_level == 0
        assert self.pet.water_level == 0
        assert self.pet.energy_level == 100
        assert self.pet.sanitation_level == 0
        assert self.pet.mood_level == 0

    #test print status
    def test_print_status(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.pet.print_status()
            output = mock_stdout.getvalue()

        lines = output.strip().split("\n")

        expected_output = [
            "Pet: Yuka",
            f"Mood: {self.pet.get_status()['Mood']}",
            f"Hunger: {self.pet.get_status()['Hunger']}",
            f"Thirst: {self.pet.get_status()['Thirst']}",
            f"Energy: {self.pet.get_status()['Energy']}",
            f"Cleanliness: {self.pet.get_status()['Cleanliness']}",
            f"Favorite Toy: {self.pet.favoriteToy}",
        ]

        for i in range(len(lines)):
            assert lines[i] == expected_output[i]


        