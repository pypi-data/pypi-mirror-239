# petmagotchi/__main__.py
from pet import Pet

def main():
    # Create a pet instance
    my_Pet = Pet(name='Fido', type='Dog')

    #Load pet
    # my_Pet = Pet.load_pet("Fido.pickle")

    # Display pet status
    my_Pet.print_status()
    print()

    # Feed the pet
    my_Pet.feed_pet(food='meat', quantity=2)
    my_Pet.print_status()
    print()

    # Play with the pet
    my_Pet.play(toy='ball')
    my_Pet.print_status()
    print()

    #Hydrate pet
    my_Pet.hydrate_pet(drink='lemonade', quantity=3)
    my_Pet.print_status()
    print()

    #See pet
    my_Pet.see_pet()

    #Wash pet
    my_Pet.wash()
    my_Pet.print_status()
    print()

    #Pet pet
    my_Pet.pet()
    my_Pet.print_status()
    print()

    #Bring pet to destination
    print(my_Pet.bring_to(destination = 'park'))
    my_Pet.print_status()

    #save pet
    my_Pet.save_pet()

if __name__ == '__main__':
    main()
