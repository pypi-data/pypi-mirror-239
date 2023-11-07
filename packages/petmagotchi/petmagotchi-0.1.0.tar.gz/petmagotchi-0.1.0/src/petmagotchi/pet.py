import time
import random
import pickle
import os
from PIL import Image

class Pet:
    class InvalidFoodError(Exception):
        """Raised when an invalid food is given to the pet."""
        pass

    class InvalidQuantityError(Exception):
        """Raised when the user gives too many or too little quantity"""
        
    class InvalidToyError(Exception):
        """Raised when the user gives too many or too little quantity"""

    class InvalidDrinkError(Exception):
        """Raised when an invalid drink is given to the pet."""

    class InvalidDestinationError(Exception):
        """This destination is not a valid place to bring a pet"""

    HUNGER_RATE = 3
    THIRST_RATE = 4
    CLEANLINESS_RATE = 1
    MOOD_RATE = 2
    ENERGY_RATE = 2
    VALID_FOODS = {'meat':(15,5),'vegetable':(10,2),'ice cream':(5,15),'bread':(8,8)} #meal:(hunger fill, mood increase)
    VALID_DRINKS = {'water':(15, 0), 'soda':(5, 10), 'milk':(13, 5), 'lemonade':(-5, 12)} #drink:(thirst fill, mood increase)
    TOYS = {'yarn': 10,'ball':12,'plushie':15,'bone':10} #toy: mood increase
    TRAVEL_CD = 60*60  # one hour between trips
    # stat changes for bring_to destinations
    TRAVEL_DESTS = {
        'park': {
            'res': '%s had a great time at the park, playing and enjoying the fresh air!',
            'stats': {
                'mood_level': 20,
                'sanitation_level': -10,
                'energy_level': -25,
                'food_level': -10,
                'water_level': -10,
        }},
        'hike': {
            'res': '%s really enjoyed hiking the trails and exploring the wilderness!',
            'stats': {
                'mood_level': 30,
                'sanitation_level': -15,
                'energy_level': -35,
                'food_level': -15,
                'water_level': -15,
        }},
        'vet': {
            'res': "The vet makes %s nervous, but they're feeling better already.",
            'stats': {
                'mood_level': -20,
                'energy_level': 35,
        }},
        'groomer': {
            'res': "%s had a spa day at the groomer's! They got pampered and received a fresh new look.",
            'stats': {
                'mood_level': 15,
                'sanitation_level': 100,
                'energy_level': -15,
        }},
        'cafe': {
            'res': '%s had a fun time at the pet cafe, enjoying treats and making friends.',
            'stats': {
                'mood_level': 15,
                'energy_level': -15,
                'food_level': 5,
                'water_level': 5,
        }},
    }
    # alert messages when a stat is too low.
    TRAVEL_ALERTS = {
        'mood_level': '%s refuses to leave the house! Do something to improve their mood.',
        'sanitation_level': "%s can't leave the house looking like that! They might need a bath.",
        'energy_level': '%s is too tired to go there right now.',
        'food_level': "%s is too hungry. They won't leave without a snack.",
        'water_level': "%s is too thirsty. They need a drink!",
    }
    VALID_TYPES = ["Cat","Dog"]
    
    def __init__(self, name, type):
        if not isinstance(name, str) or not isinstance(type, str):
            raise ValueError("Name and type must be strings.")
        if not isinstance(type, str) or type not in Pet.VALID_TYPES:
            raise ValueError(f"Type must be one of the following: {', '.join(Pet.VALID_TYPES)}.")
        self.name = name
        self.type = type
        self.food_level = random.randint(55, 80)
        self.water_level = random.randint(55, 80)
        self.sanitation_level = random.randint(55, 80)
        self.mood_level = 90
        self.energy_level = random.randint(55, 80)
        self.last_update_time = time.time()
        self.last_travel = time.time() - Pet.TRAVEL_CD

        self.favoriteToy = random.choice(list(Pet.TOYS.keys()))

        if type == "Cat":
            self.favoriteDrink = "milk"
        elif type == "Dog":
            valid_drinks = list(Pet.VALID_DRINKS.keys())
            valid_drinks.remove("milk")
            self.favoriteDrink = random.choice(valid_drinks)

    def get_mood(self):
        if 0 <= self.mood_level < 30:
            return f"{self.name} is upset..."
        elif 30 <= self.mood_level < 80:
            return f"{self.name} is feeling ok..."
        else:
            return f"{self.name} is excited and happy to be with you!"

    def _update_status(self):
        time_change = time.time() - self.last_update_time
        rate_of_change = time_change / 1800
        self.food_level = max(round(self.food_level - rate_of_change * Pet.HUNGER_RATE), 0)
        self.water_level = max(round(self.water_level - rate_of_change * Pet.THIRST_RATE), 0)
        self.sanitation_level = max(round(self.sanitation_level - rate_of_change * Pet.CLEANLINESS_RATE), 0)
        self.mood_level = max(round(self.mood_level - rate_of_change * Pet.MOOD_RATE), 0)
        self.energy_level = min(round(self.energy_level + rate_of_change * Pet.ENERGY_RATE), 100)
        self.last_update_time = time.time()

    def get_status(self):
        self._update_status()
        return {
            "Pet": self.name,
            "Mood": self.get_mood(),
            "Hunger": self.food_level,
            "Thirst": self.water_level,
            "Energy": self.energy_level,
            "Cleanliness": self.sanitation_level,
            "Favorite Toy": self.favoriteToy,
            "Favorite Drink": self.favoriteDrink
        }

    def print_status(self):
        status = self.get_status()
        order = ["Pet","Mood","Hunger","Thirst","Energy","Cleanliness", "Favorite Toy"]
        for key in order:
            print(key+":",status[key])

    def feed_pet(self,food,quantity):
        self._update_status()
        if not isinstance(food,str) or not isinstance(quantity,int):
            raise ValueError("Food must be a string and quantity must be an int.")
        if food not in Pet.VALID_FOODS:
            raise Pet.InvalidFoodError(f"'{food}' is not a valid food. Valid foods are: {', '.join(Pet.VALID_FOODS)}")
        if quantity>3 or quantity<1:
            raise Pet.InvalidQuantityError(f"'{quantity}' is not a valid quantity. Valid quantities are 1,2 and 3. Can't give your pet a stomachache!")
        food_fill = Pet.VALID_FOODS[food][0]
        mood_increase = Pet.VALID_FOODS[food][1]
        self.food_level = min(self.food_level + (food_fill * quantity),100)
        self.mood_level = min(self.mood_level + (mood_increase * quantity),100)

        reactions = {
            "meat": f"{self.name} pounces on the steak and gobbles it up!",
            "vegetable": f"{self.name} finished the fragrant vegetables before you knew it!",
            "ice cream": f"The sweet treat draws a smile on {self.name}'s face! He appreciates that you wiped the leftover cream from his mouth.",
            "bread": f"Perfect toasty sandwich! A comfortable meal for {self.name}."
        }

        print(reactions.get(food, f"{self.name} enjoyed the meal!"))

    def hydrate_pet(self, drink, quantity):
        self._update_status()
        if not isinstance(drink, str):
            raise ValueError("Drink must be a string")
        if not isinstance(quantity, int):
            raise ValueError("Quantity must be an int.")
        if drink not in Pet.VALID_DRINKS:
            raise Pet.InvalidDrinkError(f"'{drink}' is not a valid food. Valid drinks are: {', '.join(Pet.VALID_DRINKS)}")
        if quantity > 4:
            raise Pet.InvalidQuantityError(f"'{quantity}' is not a valid quantity!  Try to limit giving your pet up to 3 drinks at a time.")
        if quantity < 1:
            raise Pet.InvalidQuantityError(f"You cruel person... You can't not give your pet a drink or try to take drinks away from them!")

        thirst_fill = Pet.VALID_DRINKS[drink][0]
        mood_increase = Pet.VALID_DRINKS[drink][1]
        self.water_level = min(self.water_level + (thirst_fill * quantity), 100)
        self.mood_level = min(self.mood_level + (mood_increase * quantity) + (10 if drink == self.favoriteDrink else 0), 100)

        reactions = {
            "water": f"{self.name} hydrates with water.",
            "soda": f"The soda fizzes in {self.name}'s mouth with a delightful feeling.",
            "milk": f"{self.name} takes a healthy chug of milk.",
            "lemonade": f"Nothing like fresh lemonade to cool off {self.name} on this fine day!"
        }

        print(reactions.get(drink, f"{self.name} is feeling refreshed!") + (' It\'s their favorite drink! +10 hydration. ' if drink == self.favoriteDrink else ''))

    def play(self, toy):
        self._update_status()
        if not isinstance(toy, str):
            raise ValueError("Toy must be a string.")
        if toy not in Pet.TOYS:
            raise Pet.InvalidToyError(f"'{toy}' is not a valid toy. Valid toys are: {', '.join(Pet.TOYS)}")

        reationStr = ""
        if self.energy_level < 10:
            print(f"{self.name} is too tired to play. Lets give them a break!")
            return
        else:
            energy_decrease = 10
            mood_increase = Pet.TOYS[toy]
            if(self.favoriteToy == toy):
                mood_increase *= 2
                reationStr += f"{self.name} loved playing with their favorite toy! "

            if(random.randint(0,9) == 0): #10% chance of doubling the mood increase
                mood_increase *= 2
                reationStr += f"{self.name} had extra fun playing with you this time! "
            else:
                reationStr += f"{self.name} had fun playing with you! "
            self.mood_level = min(self.mood_level + mood_increase, 100)
            self.energy_level = max(self.energy_level - energy_decrease, 0)
        print(reationStr + "They can't wait to play again!")

    def wash(self):
        self._update_status()
        if self.sanitation_level == 100:
            print(f"{self.name} is really clean! No need to wash them.")
        else:
            self.sanitation_level = 100
            print(f"{self.name} is squeaky clean now!")

    def pet(self):
        self._update_status()
        
        reationStr = ""
        if self.mood_level < 30:
            print(f"{self.name} is too upset to be pet. Try playing with them!")
            return
        else:
            mood_increase = 5
            if(random.randint(0,9) == 0): #10% chance of doubling the mood increase
                mood_increase *= 2
                reationStr = f"{self.name} is really happy to be pet by you!"
            else:
                reationStr = f"{self.name} enjoyed being pet!"
        self.mood_level = min(self.mood_level + mood_increase, 100)
        print(reationStr)

    def _get_image(self, mood):
        imgAddress = "src/images/"
        if(self.type == "Cat"):
            imgAddress += "cat/cat_"
        elif(self.type == "Dog"):
            imgAddress += "dog/dog_"
        
        if mood == "upset":
            imgAddress += "upset"
        elif mood == "neutral":
            imgAddress += "neutral"
        else:
            imgAddress += "happy"
        
        imgAddress += ".png"
        return Image.open(imgAddress)

    def see_pet(self):
        if 0 <= self.mood_level < 30:
            return self._get_image("upset")
        elif 30 <= self.mood_level < 80:
            return self._get_image("neutral")
        else:
            return self._get_image("happy")

    def bring_to(self, destination):
        self._update_status()

        # bad dest
        if not isinstance(destination, str):
            raise ValueError('Destination must be a string.')

        # lower
        destination = destination.lower()

        # invalid dest
        if destination not in Pet.TRAVEL_DESTS:
            raise Pet.InvalidDestinationError(
                f"'{destination}' is not a valid place to bring {self.name}.\nValid destinations are: {', '.join(Pet.TRAVEL_DESTS.keys())}"
            )

        # traveling too soon
        now = time.time()
        if now < self.last_travel + Pet.TRAVEL_CD:
            return f"{self.name} wants to relax at home. Try waiting some time before bringing them out again!"
        self.last_travel = now

        # update stats, return res string
        stat_change = Pet.TRAVEL_DESTS[destination]['stats']
        updated_stats = []

        for stat in stat_change:
            current = getattr(self, stat)
            changed = current + stat_change[stat]
            if changed < 0:
                return Pet.TRAVEL_ALERTS[stat] % self.name
            updated_stats.append((stat, min(changed, 100)))

        for stat, updated in updated_stats:
            setattr(self, stat, updated)

        return Pet.TRAVEL_DESTS[destination]['res'] % self.name
    
    def save_pet(self):
        filename = f"{self.name.replace(' ', '_')}.pickle"
        if '/' in filename or '\\' in filename or ':' in filename:
            raise ValueError("Pet name contains invalid characters for a filename.")
        with open(filename, 'wb') as file:
            pickle.dump(self, file)
        print(f"Pet '{self.name}' saved to {filename}")
    
    @staticmethod
    def load_pet(file_path):
        pet_name = os.path.basename(file_path).rsplit('.pickle', 1)[0].replace('_', ' ')
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file for the pet named '{pet_name}' does not exist.")
        with open(file_path, 'rb') as file:
            pet = pickle.load(file)
        print(f"Pet loaded from {file_path}")
        return pet

