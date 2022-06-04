import json
import boto3
import requests
from bs4 import BeautifulSoup
from soup import get_dog_details


text_part = """
{{#dogs}}
{{headshot}}
{{name}}
{{breed}}
{{sex}}
{{age}}
{{weight}}
{{description}}
{{#pictures}}
{{this}}
{{/pictures}}
{{/dogs}}
"""

html_part = """
<head>
    <style>
        img {
            max-height:300px;
            max-width:300px;
            height:auto;
            width:auto; 
        }
    </style>
</head>
{{#dogs}}
    <img src="{{headshot}}" alt="{{name}}'s headshot">
    <h1>{{name}}</h1>
    <ul>
        <li>{{breed}}</li>
        <li>{{sex}}</li>
        <li>{{age}}</li>
        <li>{{weight}}</li>
    </ul>
    <p>{{description}}</p>
    {{#pictures}}
        <img src="{{this}}" alt="A picture of {{name}}">
    {{/pictures}}
    <hr>
{{/dogs}}
"""


def update_template(ses):
    template = {
        'TemplateName': 'dog_template',
        'SubjectPart': 'There are new dogs for you to view!',
        'TextPart': text_part,
        'HtmlPart': html_part,
    }
    ses.update_template(Template=template)


def send_email(recipient: str, dogs: dict):
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
    dogs = {'dogs': []}
    for url in urls:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        dog = get_dog_details(soup)
        dogs['dogs'].append(dog)
    
    ses = boto3.client('ses')
    recipient = 'rob.mitchellzone@gmail.com'
    send_email(recipient, dogs)
