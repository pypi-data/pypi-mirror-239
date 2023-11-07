import pytest
from unittest.mock import patch
from petmagotchi.pet import Pet

TRAVEL_CD_PATCH = 100
TRAVEL_DESTS_PATCH = {
    'park': {
        'res': 'test %s park',
        'stats': {
            'mood_level': 10,
            'sanitation_level': 20,
            'energy_level': 30,
            'food_level': 40,
            'water_level': 50,
    }},
    'hike': {
        'res': 'test %s hike',
        'stats': {
            'mood_level': -10,
            'sanitation_level': -20,
            'energy_level': -30,
            'food_level': -40,
            'water_level': -50,
    }},
}
TRAVEL_ALERTS_PATCH = {
    'mood_level': 'test %s mood_level',
    'sanitation_level': 'test %s sanitation_level',
    'energy_level': 'test %s energy_level',
    'food_level': 'test %s food_level',
    'water_level': 'test %s water_level',
}


# testing pet, patched config
@pytest.fixture
def pet() -> Pet:
    with patch('petmagotchi.pet.Pet.TRAVEL_CD', TRAVEL_CD_PATCH),\
    patch('petmagotchi.pet.Pet.TRAVEL_DESTS', TRAVEL_DESTS_PATCH),\
    patch('petmagotchi.pet.Pet.TRAVEL_ALERTS', TRAVEL_ALERTS_PATCH):
        with patch('time.time', return_value=0):  # create at time 0
            pet0 = Pet('Moana', 'Dog')  # (my dawg 🐕🐕🐶🌊)
        yield pet0


# side effect to set stats
def set_stats(p: Pet, mood_level=0, sanitation_level=0, energy_level=0, food_level=0, water_level=0):
    def p_set_stats():
        p.mood_level = mood_level
        p.sanitation_level = sanitation_level
        p.energy_level = energy_level
        p.food_level = food_level
        p.water_level = water_level

    return p_set_stats


# patch _update_status to set stats
def set_stats_on_update(p: Pet, mood_level=0, sanitation_level=0, energy_level=0, food_level=0, water_level=0):
    return patch.object(Pet, '_update_status',
        side_effect=set_stats(p, mood_level, sanitation_level, energy_level, food_level, water_level))


# assert expected stats
def expect_stats(p: Pet, mood_level=0, sanitation_level=0, energy_level=0, food_level=0, water_level=0):
    assert p.mood_level == mood_level
    assert p.sanitation_level == sanitation_level
    assert p.energy_level == energy_level
    assert p.food_level == food_level
    assert p.water_level == water_level


class TestBringTo():

    def test_bring_to_bad_destination(self, pet: Pet):
        with pytest.raises(ValueError), set_stats_on_update(pet):
            pet.bring_to(123)
        expect_stats(pet)  # should not change stats


    def test_bring_to_invalid_destination(self, pet: Pet):
        with pytest.raises(Pet.InvalidDestinationError), set_stats_on_update(pet):
            pet.bring_to('movies')
        expect_stats(pet)  # should not change stats


    def test_bring_to_lower(self, pet: Pet):
        assert pet.bring_to('PaRk') == 'test Moana park'


    def test_bring_to_travel_cooldown(self, pet: Pet):
        with patch('time.time', return_value=10):
            assert pet.bring_to('park') == 'test Moana park'

        with patch('time.time', return_value=50), set_stats_on_update(pet):
            assert pet.bring_to('park') == "Moana wants to relax at home. Try waiting some time before bringing them out again!"
        expect_stats(pet)  # should not change stats

        with patch('time.time', return_value=110):
            assert pet.bring_to('park') == 'test Moana park'


    def test_bring_to_update_stats(self, pet: Pet):
        with patch('time.time', return_value=0), set_stats_on_update(pet):
            assert pet.bring_to('park') == 'test Moana park'
        expect_stats(pet, 10, 20, 30, 40, 50)

        with patch('time.time', return_value=100), set_stats_on_update(pet, *(100,)*5):
            assert pet.bring_to('hike') == 'test Moana hike'
        expect_stats(pet, 90, 80, 70, 60, 50)


    def test_bring_to_update_maxed_stats(self, pet: Pet):
        with set_stats_on_update(pet, *(90,)*5):
            assert pet.bring_to('park') == 'test Moana park'
        expect_stats(pet, *(100,)*5)


    def test_bring_to_require_stats(self, pet: Pet):
        tired_stats = 10, 100, 20, 100, 100
        with set_stats_on_update(pet, *tired_stats):
            assert pet.bring_to('hike') == 'test Moana energy_level'
        expect_stats(pet, *tired_stats)  # should not change stats


    def test_validate_travel_config(self):
        pet = Pet('Moana', 'Dog')  # no patch

        assert isinstance(Pet.TRAVEL_CD, int) and Pet.TRAVEL_CD >= 0

        for stat, alert in Pet.TRAVEL_ALERTS.items():
            assert hasattr(pet, stat)  # valid stat
            assert isinstance(alert, str)  # alert is string
            assert alert.count('%') == 1  # alert has exactly one placeholder

        safe_stats = set(Pet.TRAVEL_ALERTS.keys())

        for dest in Pet.TRAVEL_DESTS.values():
            assert set(dest.keys()) == set(('res', 'stats'))  # response and stats change
            assert isinstance(dest['res'], str)  # response is string
            assert dest['res'].count('%') == 1  # response has exactly one placeholder
            for stat, change in dest['stats'].items():
                assert hasattr(pet, stat)  # valid stat
                assert stat in safe_stats  # stat has corresponding alert
                assert isinstance(change, int)  # change is int
