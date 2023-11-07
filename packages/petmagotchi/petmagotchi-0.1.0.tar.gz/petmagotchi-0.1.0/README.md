# Petmagotchi Package

![Build Status](https://github.com/software-students-fall2023/3-python-package-exercise-leftovers3/actions/workflows/build.yaml/badge.svg)

## What is Petmagotchi?

Petmagotchi is a package that allows you to simulate taking care of your own virutal pet! Inspired by the Tamagotchi, you can create your own pet and interact with it in various ways. Take care of him/her by feeding, cleaning and playing with him!

## Features

- **Create Your Pet**: Choose from a variety of pet types and give it a name to start your journey together.
- **Feed Your Pet**: Give an assortment of foods and drinks to your pet to keep their tummy full and hydrated.
- **Hygiene Maintenance**: Clean your pet so they are ready for cuddles!
- **Playtime**: Engage in fun activities with your pet to share a wonderful time together.

## Installation

To install Petmagotchi, use the following pip command: pip install petmagotchi

## Functions and usage

Create a new python file and install petmagotchi. Then, import the package with the following line of code:

from petmagotchi import Pet

### Create Pet: `Pet(name,type)`

Create your pet instance with the following command: `my_Pet = Pet(name = 'pet_name', type = 'type')`

Any pet name is allowed, given that the pet name is a string.

The current version only supports two types of pets: Dog, Cat

Therefore, valid commands look like:
```python
my_Pet = Pet(name = 'Yuka', type = 'Cat')
my_Pet = Pet(name = 'Kylo', type = 'Dog')
```

### See the status of your pet: `print_status()`

To see the status of your pet, use the print_status() method. Example below:

```python
my_Pet.print_status()
```

This will automatically update your pet status based on the the time since the last action, and show you the status of your pet.

### Feed your pet: `feed_pet(food, quantity)`

To feed your pet, use the feed_pet(food,quantity) method. This will fill your pet's hunger meter and mood. The method will also print out a reaction!

- The valid food selections are: meat, vegetable, ice cream, bread
- The valid quantity range is: [1,3]

Example below:
```python
my_Pet.feed_pet(food = 'meat', quantity = 2)
```

### Hydrate your pet: `hydrate_pet(drink, quantity)`

Same as feed, but for drinks!

- The valid food selections are: water, soda, milk, lemonade
- The valid quantity range is: [1,3]

Example below:

```python
my_Pet.feed_pet(drink = 'lemonade', quantity = 3)
```

### Play with your pet: `play(toy)`

Play with your pet by giving it a toy. This will consume some energy but raise their mood. Pets also have a favorite toy!

- The valid toy selections are: yarn, ball, plushie, bone
- Pets that have low energy will be too tired to play

Example below:

```python
my_Pet.play(toy = 'plushie')
```

### Keep your pet clean: `wash()`

Keep your pet clean by washing him with: 

```python
my_Pet.wash()
```

### Pet your pet: `pet()`

Pet your pet with: 

```python
my_Pet.pet()
```

A pet that is too unhappy may not be willing to come for pets. Keep them happy by playing with them!

### See your pet: `see_pet()`

Want to see a picture of your pet? Use the see_pet() method: 

```python
my_Pet.see_pet()
```

The image you see will depend on your pet's mood.


### Bring them somewhere: `bring_to(destination)`

Take your pet somewhere fun!

You can take them to the `park`, on a `hike`, to the `vet`, to the `groomer`, or lastly to a pet `cafe`.

```python
my_Pet.bring_to('park')
```

### Save your pet: `save_pet()`

Save your pet for the future!

```
my_Pet.save_pet()
```

The file will automatically be called petName.pickle, where petName will be the name of your pet, with underscores representing spaces.

### Load your pet: `load_pet(file_path)`

Load a previous pet:

```
my_Pet = Pet.load_pet(file_path = 'Fido.pickle')
```

Ensure to enter the file name correctly!


### Example file
To see an example file with the above methods, click [here](https://github.com/software-students-fall2023/3-python-package-exercise-leftovers3/blob/main/src/petmagotchi/__main__.py).

## Contributing to the package

Feel free to contribute to the project! Here are the steps you can take to contribute.

### Fork the repository

Fork the repository to your own account by visiting our [GitHub page](https://github.com/software-students-fall2023/3-python-package-exercise-leftovers3/tree/main).

### Clone the repository to your local computer

Use Git Bash or something similar to clone the repository to your local computer. The command for Git Bash is: 

```
git clone ...
```

Where you replace ... with the url of the repository.

### Set up your Development Environment

1. Open a terminal with python.
2. If you do not have pipenv, install the package with the command: 

```
pip install pipenv
```
3. Once pipenv is installed, install the package dependencies by running: 
```
pipenv install --dev
```

To activate the virtual environment, run: 

```
pipenv shell
```

You can now write your code to contribute to the project.

### Rest of the workflow: branch creation, creating a PR

Create your own feature branch, then add and commit your changes. Once that is completed, feel free to create a pull request to the main repository.

We will review the changes as soon as possible!

### Other notes

- Make sure to add and run additional unit tests for newly written functions in /src/tests.
- Add documentation to the README.md for new functions.

You can run tests in the terminal with the command: pipenv run pytest

## Contributors

- [Capksz](https://github.com/Capksz)
- [tinybitofheaven](https://github.com/tinybitofheaven)
- [FrozenEclipse](https://github.com/FrozenEclipse)
- [BradFeng02](https://github.com/BradFeng02)




