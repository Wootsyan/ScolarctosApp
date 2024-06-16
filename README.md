# ScolarctosApp

- [Overview](#overview)
- [Features](#features)
- [Stack](#stack)
- [Installation](#installation)

## Overview
This is a web application built using the Django framework. The main purpose of the application is to assist in organizing a school mathematics contest for students in Poland from primary and secondary schools. The dashboard is created using the Django template system and the [SRTdash template](https://github.com/puikinsh/srtdash-admin-dashboard), shared by [Colorlib](https://colorlib.com).

## Features

1. **Users**
    - Custom User model and 4 main types: Admin, Organizer, Guardian, Student.
    - Custom permission groups and custom permissions.
    - Registration for guardians and students, admins and organizers are created from dashboard.
    - Email verification, tested with [mailtrap](https://mailtrap.io/).
    - Authentication.
    - Profiles.
2. **GDPR**
    - GDPR consents service.
    - Parental consents service for minors.
    - File uploading.
3. **Schools**
    - CRUD operations.
    - Confirming schools.
    - Connecting schools with guardians.
4. **Teams**
    - CRUD operations.
    - CRUD operations for members.
    - Connecting files with GDPR i parental consents.
5. **Invitations**
    - Sending invitations from team leader to guardian and gurdian to team leader from same school.
    - Accepting invitations then connecting team with guardian.

**Next features**
    - [] Contest stages.
    - [] Tasks, marking and teams rankings.

## Stack

**Back-end:** Python 3.8.10, Django 4.2.4, 

**Database:** PostgreSQL 12+

**Front-end:** HTML5, CSS3, Bootstrap 4, JavaScript, jQuery

## Installation

### Steps

1. Install Python 3.8 and clone the GitHub repository.
    ```bash
    $ git clone https://github.com/Wootsyan/ScolarctosApp.git
    $ cd ScolarctosApp
    ```

2. Create a virtual environment and activate it:
    ```bash
    $ python3 -m venv venv
    $ source venv/bin/activate
    ```

3. Install the required packages:
    ```bash
    $ pip install -r requirements.txt
    ```

4. Rename file .env-example to .env and fill it with needed information. To generate SECRET_KEY you can use:
    ```bash
    $ python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
    ```

5. Apply the database migrations:
    ```bash
    $ python manage.py migrate
    ```

## Running the Application

To start the development server, use the following command:
    ```bash
    $ python manage.py runserver
    ```

The application will be available at http://127.0.0.1:8000/dashboard/.
