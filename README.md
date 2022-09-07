# Melon Tasting Reservation Scheduler

## Table of Contents
* [General Info](#general-information)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Setup](#setup)
* [Todo](#todo)



## General Information
- This app aims to help users make reservations to go to a fancy melon tasting! 
- It is a take home challenge assignment
- It needed to be completed in 4 - 6 hours



## Technologies Used
- I am using Python in the backend, where I built my server, model, crud, seed and tests files
- I am Flask to build my routes
- I am also using Postgresql and Sqlalchemy for my database, where I built my User and Appointment tables.
- For the frontend I am using Jinja to populate my HTML templates.



## Features
- Login page.

- In the main page, user can select the date that they would like to go in the melon tasting, and the start and end time as well. If they select a day or time that is not available, a flash message will let the user know, so they can try it again. They can also check their scheduled appointments.

- After submitting a date and times, the user is redirected to a page where available times are displayed. Every time has a button where the user can select the time that they would like.


- After selecting the time, the user is redirected to the homepage, and a flash message will let the user know that their appointment was successfully scheduled.


https://user-images.githubusercontent.com/98921140/188916780-07fdb896-bc66-48e6-bb5f-5dc9208d3ef1.mp4

## Setup

To install it locally:

$ git clone https://github.com/BeatrizNiemeyer/Melon-Tasting-Reservation-Scheduler.git <br>
$ cd home-project <br>
$ virtualenv env <br>
$ source env/bin/activate <br>
$ pip3 install -r requirements.txt <br>
$ python3 seed_database.py <br>
$ python3 server.py <br>



## Todo

If I hade more time I would:

- Improve how to handle time appointments, so the code can be cleaner and more efficient 
- Sort appointment dates
- Enable user to cancel and edit appointments
- Add style
- Use AJAX calls or React to improve user
