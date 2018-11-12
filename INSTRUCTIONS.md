    ICSI-418 Software Engineering
    Fall 2018 Semester Project
    Due December 14, 2018

## Overview

The semester project for ICSI-418 consists of a base level of required functionality that can be implemented using one of
several development platforms. There is one platform that is required for implementation that one team will be
responsible for. More on the platforms below. This project will be the final for the course and must be complete by the
date indicated above.


## Required Functionality

The required functionality consists of a web scraping function, user interface, search, business logic and a database. The
user interface must be developed so that the user can enter search parameters and click a button that will retrieve the
search data from the database and produce a page with the results. Each of the data entry fields on the user interface
must be searchable on the database. The user should be required to log on to the application with a user id and
password.

As a search is executed and multiple results are found, the user interface must allow the user to scroll through the
search results. The user interface will need to allow the data from the screen to be printed to PDF.
The application also needs to be able to export the data that was retrieved to a CSV file. Prompt the user for the
location and name of the export file.


## Platforms

There are many choices of platforms that the application can be implemented on. Below is a sample of three. However,
1 team must implement the application on Platform Choice 1.

###### Choice 1

* ASP.NET, C# preferably in an
MVC design pattern but .NET
Core can be used
* Web application developed and
then implemented on the AWS
or Microsoft Azure Cloud
Platform
* Database: SQL Server (express)
* Backup of code base and
documentation to Git or related
repository

###### Choice 2

* Choice of Java, PHP or Python
* Web application developed and
implemented on the AWS or
Microsoft Azure Cloud Platform
* Database: SQL Server (express) or
MySQL
* Backup of code base and
documentation to Git or related
repository


###### Choice 3

* Another Open Source Tool, please
discuss with me first
* Web application developed and
implemented on the AWS or
Microsoft Azure Cloud Platform
* Database: Database choice, please
discuss with me first
* Backup of code base and
documentation to Git or related
repository


## Data Content

The data content is going to come from a public facing website. The website URL is:

https://www.nasdaq.com/options/

The application will need to follow links on the page and web screen scrape content from the page and place the data
into the database. The scrape will be of the headline, the symbols in the headline and the associated text for each of the
symbols in the headline. This data will be stored to the database along with the date of the scrape.


## Search Data UI

The user will be able to search each of the data elements via a search page and a results page will be displayed showing
all of the data in the row. The search page should have a submit button, reset button and exit button that will log the
user off the application.


## Deliverables

The deliverables for this project are as follows:

* Requirements documentation
* Appropriate level of design documentation
* Product Backlog
* Project Plan
* Code Repository
* Testing Plan and Results
* Deployment Plan Including Install Scripts
* Maintenance Plan


## Project Presentation

The project presentation, which will be due the last day of classes, is a wrap-up of what went well, what you would have
done differently and lessons learned from the project. All team members should contribute on the presentation. Use
PowerPoint, sheets or some other similar presentation tool.


## Grading

Working application – 30%

Deliverables – 50%

Project Presentation Last Day of Classes – 20%