# icsi-418y
Unambiguous Unicorns

## Tutorial Used as Inspiration

https://gearheart.io/blog/how-to-deploy-django-app-with-aws-elastic-beanstalk/

## Start Django Server

`python manage.py runserver`

## Initialize .env for Development

Create a .env file at the root of this project and paste the following lines:

```
DATABASE_NAME=nascrapd
DATABASE_USER=root
DATABASE_PASSWORD=
DATABASE_HOST=127.0.0.1
DATABASE_PORT=3306
```

NOTE: The .env file on your computer will NOT be committed to VCS. We all get our own .env as does the AWS envionment.

## Install All Required Packages

From the root of this project in a Terminal prompt (Command-Line Interface, i.e., "CLI"):

```$ pip install -r requirements.txt --ignore-installed```