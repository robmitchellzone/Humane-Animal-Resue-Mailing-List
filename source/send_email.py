import json
import boto3
import requests
from bs4 import BeautifulSoup
from source.scrape_site import get_dog_details


ses = boto3.client('ses')


def send_email(recipient: str, dogs: list):
    dogs = {'dogs': dogs}
    source = 'Rob Mitchell <rob.mitchellzone@gmail.com>'
    template_send_args = {
        'Source': source,
        'Destination': {'ToAddresses': [recipient]},
        'Template': 'dog_template',
        'TemplateData': json.dumps(dogs),
        'ConfigurationSetName': 'email_failures_to_rob'
    }
    ses.send_templated_email(**template_send_args)


if __name__ == '__main__':
    urls = [
        'https://humaneanimalrescue.org/animals/agatha-92133/',
        'https://humaneanimalrescue.org/animals/augustus-92932/'
    ]
    dogs = []
    for url in urls:
        r = requests.get(url)
        dogs.append(get_dog_details(BeautifulSoup(r.text, 'html.parser')))

    recipient = 'rob.mitchellzone@gmail.com'
    send_email(recipient, dogs)
