import os
import json

from scrape_site import get_new_dogs
from send_email import send_dog_email, send_no_dog_email

RECIPIENT_EMAIL = os.getenv('SENDER_EMAIL')  # For development only
DOG_FILE = os.getenv('DOG_FILE')


def save_dogs(new_dogs):
    try:
        with open(DOG_FILE, 'r') as f:
            old_dogs = json.load(f)
    except FileNotFoundError:
        os.mkdir('data')
        old_dogs = []
    old_dogs.extend(new_dogs)
    print(f'Saving {len(new_dogs)} new dogs')
    with open(DOG_FILE, 'w') as f:
        json.dump(old_dogs, f, indent=4)


if __name__ == '__main__':
    new_dogs, dog_details = get_new_dogs()
    if dog_details:
        send_dog_email(RECIPIENT_EMAIL, dog_details)
        save_dogs(new_dogs)
    else:
        send_no_dog_email(RECIPIENT_EMAIL)