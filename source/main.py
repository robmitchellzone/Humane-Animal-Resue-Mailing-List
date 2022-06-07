from source.scrape_site import get_new_dogs
from source.send_email import send_email
import json


def save_dogs(new_dogs):
    with open('data/dogs.json', 'r') as f:
        old_dogs = json.load(f)
    old_dogs.extend(new_dogs)
    with open('data/dogs.json', 'w') as f:
        json.dump(old_dogs, f, indent=4)


if __name__ == '__main__':
    new_dogs, dog_details = get_new_dogs()
    send_email('rob.mitchellzone@gmail.com', dog_details)
    save_dogs(new_dogs)