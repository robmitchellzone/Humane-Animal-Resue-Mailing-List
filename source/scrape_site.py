import json
import logging

import requests
from bs4 import BeautifulSoup

logging.basicConfig(filename='har/log.log')

def list_dogs(soup: BeautifulSoup) -> list:
    """
    Get a list of dogs from the main webpage.
    :param soup: BeautifulSoup object
    :return: list of dogs
    """
    results = soup.find_all('a', attrs={'class': 'wpgb-card-layer-link'})
    dogs = []
    dog_pages = [result.attrs['href'] for result in results]
    for dog_page in dog_pages:
        dog_name, dog_id = dog_page.split('/')[-2].split('-')
        entry = {
            'id': dog_id,
            'name': dog_name,
            'url': dog_page
        }
        dogs.append(entry)
    return dogs


def get_dog_details(soup: BeautifulSoup) -> dict:
    """
    Get details of a dog from the dog's webpage.
    :param soup: BeautifulSoup object
    :return: dict of dog details
    """
    dog_details = {}

    try:
        details = soup.find('div', attrs={'class': 'animal-copy'}).contents
        pics = soup.find('div', attrs={'class': 'animal-photos'})('img')
    except AttributeError as e:
        logging.debug(soup.prettify())
        raise e

    translator = str.maketrans({chr(10): '', chr(9): ''})  # Remove \n and \t
    
    dog_details['headshot'] = pics[0].attrs['src'].strip()
    dog_details['name'] = details[1].text
    dog_details['breed'] = details[3].text
    dog_details['sex'] = details[5].text
    dog_details['age'] = details[7].text
    dog_details['weight'] = details[9].text
    dog_details['description'] = details[15].text.translate(translator)
    dog_details['pictures'] = [pic.attrs['src'].strip() for pic in pics[2:]]
    return dog_details


def load_old_dogs(fpath: str) -> dict:
    """Try to load old dogs from file."""
    try:
        with open(fpath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print('No old dogs file found.')
        return {}


def compare_dogs(all_dogs: dict, old_dogs: dict) -> tuple:
    """Given a list of all dogs and old dogs, return a list of new dogs."""
    old_dog_ids = [dog['id'] for dog in old_dogs]
    new_dogs = []
    for dog in all_dogs:
        if dog['id'] not in old_dog_ids:
            new_dogs.append(dog)
    detailed_dogs = []
    for dog in new_dogs:
        r = requests.get(dog['url'])
        if r.status_code == '200':
            logging.debug(r.text)
        else:
            logging.debug(r.status_code)
        details_page = BeautifulSoup(r.text, 'html.parser')
        detailed_dog = get_dog_details(details_page)
        detailed_dogs.append(detailed_dog)
    return new_dogs, detailed_dogs


def get_new_dogs() -> tuple:
    """Get a list of new dogs from the main page.
    :return: tuple of new dogs and detailed dogs
    """
    r = requests.get('https://humaneanimalrescue.org/adopt/?_type=dog')
    main_page = BeautifulSoup(r.text, 'html.parser')
    all_dogs = list_dogs(main_page)
    old_dogs = load_old_dogs('data/dogs.json')
    new_dogs, dog_details = compare_dogs(all_dogs, old_dogs)
    return new_dogs, dog_details


if __name__ == '__main__':
    _, dog_details = get_new_dogs()
    print(f'There are {len(dog_details)} new dogs!')