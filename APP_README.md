# icsi-418y
Unambiguous Unicorns

[![Build Status](https://travis-ci.com/matthewzimmer/icsi-418y.svg?token=i6DMr7AwFhJzsWtwz8NY&branch=master)](https://travis-ci.com/matthewzimmer/icsi-418y)

## Tutorial Used as Inspiration

https://gearheart.io/blog/how-to-deploy-django-app-with-aws-elastic-beanstalk/

## Start Django Server

`python manage.py runserver`

## Initialize .env for Development

Create a .env file at the root of this project and paste the following lines:

```
DATABASE_NAME=csi418y
DATABASE_USER=root
DATABASE_PASSWORD=
DATABASE_HOST=127.0.0.1
DATABASE_PORT=3306
```

NOTE: The .env file on your computer will NOT be committed to VCS. We all get our own .env as does the AWS envionment.

## Install All Required Packages

From the root of this project in a Terminal prompt (Command-Line Interface, i.e., "CLI"):

```$ pip install -r requirements.txt --ignore-installed```


## Run Migrations

```$ python manage.py migrate```

## Making Migrations

```$ python manage.py makemigrations```

## Check Django Config

```$ python manage.py check```

## Running Tests
```$ python manage.py test```


## cd to the django app on AWS once sshed

```
$ eb ssh
$ cd /opt/python/current/app
```


## ssh to MySQL in AWS

```$ mysql -h aa1kr6e0tk96fn8.cfmc7gg03dsl.us-east-1.rds.amazonaws.com -P 3306 -u unicorn -p```