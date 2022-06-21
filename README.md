Install `pipenv`

        pip3 install --user pipenv

Install required packages

        pipenv install

Add sender email to `.env` file in the main folder

        SENDER_EMAIL=<sender@domain.com>

Run `main.py` from the main folder

        pipenv run python source/main.py

## To start a cronjob to run on a timer:

Use screen to start the job in a background window

        screen

To exit screen:

        Ctrl+a d

To reattach to a screen:

        screen -r

To see a list of screens:

        screen -ls

To write a new cronjob:

        crontab -e

The cronjob text:

        0 7 * * * cd har && pipenv run python source/main.py >> ~/cronjob_log.txt

To exit vim:

        [ESC]
        :wq