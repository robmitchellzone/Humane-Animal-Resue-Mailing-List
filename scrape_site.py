import requests
import bs4 as BeautifulSoup


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

    details = soup.find('div', attrs={'class': 'animal-copy'}).contents
    pics = soup.find('div', attrs={'class': 'animal-photos'})('img')
    
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


if __name__ == '__main__':
    url = 'https://humaneanimalrescue.org/adopt/?_type=dog'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    current_dogs = list_dogs('https://humaneanimalrescue.org/adopt/?_type=dog')

    url = 'https://humaneanimalrescue.org/animals/agatha-92133/'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    dog_details = get_dog_details(soup)