import os
import json

import boto3
from botocore.config import Config
import requests
from bs4 import BeautifulSoup

from scrape_site import get_dog_details


SENDER_EMAIL = os.getenv('SENDER_EMAIL')

my_config = Config(
    region_name = 'us-east-2'
)
ses = boto3.client('ses', config=my_config)


def send_dog_email(recipient: str, dogs: list):
    dogs = {'dogs': dogs}
    source = f'Rob Mitchell <{SENDER_EMAIL}>'
    template_send_args = {
        'Source': source,
        'Destination': {'ToAddresses': [recipient]},
        'Template': 'dog_template',
        'TemplateData': json.dumps(dogs),
        'ConfigurationSetName': 'email_failures_to_rob'
    }
    ses.send_templated_email(**template_send_args)


def send_no_dog_email(recipient: str):
    source = f'Rob Mitchell <{SENDER_EMAIL}>'
    ses.send_email(
        Source=source,
        Destination={'ToAddresses': [recipient]},
        Message={
            'Subject': {
                'Data': 'There are no new dogs for you to view :('
            },
            'Body': {
                'Text': {
                    'Data': """Sorry, there are no new dogs for you to view
                            today. We'll send you another email tomorrow!"""
                },
                'Html': {
                    'Data': """<p>Sorry, there are no new dogs for you to view
                            today. We'll send you another email tomorrow!</p>
                            """
                }
            },
        },
        ConfigurationSetName='email_failures_to_rob'
    )


if __name__ == '__main__':
    urls = [
        'https://humaneanimalrescue.org/animals/agatha-92133/',
        'https://humaneanimalrescue.org/animals/augustus-92932/'
    ]
    dogs = []
    for url in urls:
        r = requests.get(url)
        dogs.append(get_dog_details(BeautifulSoup(r.text, 'html.parser')))

    recipient = SENDER_EMAIL
    send_dog_email(recipient, dogs)
