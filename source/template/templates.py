import boto3


ses = boto3.client('ses')

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
Thank you for checking out today's new dogs!
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
<p>Thank you for checking out today's new dogs!</p>
"""


def update_template(ses):
    template = {
        'TemplateName': 'dog_template',
        'SubjectPart': 'There are new dogs for you to view!',
        'TextPart': text_part,
        'HtmlPart': html_part,
    }
    ses.update_template(Template=template)


if __name__ == '__main__':
    update_template(ses)