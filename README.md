# SixtySec Pitch

## Author

[rosekairu](https://github.com/rosekairu)

### Description

A python-flask based web-app where users can share, read and comment on each others' pitch posts.
It also allows users who have signed up to comment and upvote or downvote a pitch.

## Live Link

[View Site](.herokuapp.com/)

### Setup/Installation Requirements

* Github and Heroku account - from where the application can be cloned or downloaded
* Git installed in pc - for downloading the application to interact with it locally i.e. on one's device
* Text Editor e.g. Visual Studio or Atom or pycharm - for creating, viewing and editing the code.
* A CLI (Command Line Interface) or terminal where the user can interact with the application using the various python commands e.g. python3.6 run.py or test commands.
* Browser - from where to view and further interact with the application

## Development Installation

To get the code...

1. Clone the repository:

  ```bash
  https://github.com/rosekairu/A-SixtySec-Pitch.git
    ```
2. Move to the folder:

  ```bash
  cd A-SixtySec-Pitch
  ```

3. Install requirements:

  ```bash
  pip install -r requirements.txt
  ```

4.Exporting Configurations:

  ```bash
  export SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://{User Name}:{password}@localhost/{database name}
  ```

5.Running the application

  ```bash
  python3.6 manage.py server
  ```

6.Testing the application

  ```bash
  python3.6 manage.py test
  ```
 Open the application on your browser `127.0.0.1:5000`

## BDD

| Behaviour | Input | Output |
| :---------------- | :---------------: | ------------------: |
| Load the page | **On page load** | Get all posts, Select between signup and login|
| Select SignUp| **Email**,**Username**,**Password** | Redirect to login|
| Select Login | **Username** and **password** | Redirect to page with app pitches based on categories and commenting section|
| Select comment button | **Comment** | Form that you input your comment|
| Click on submit |  | Redirect to all comments template with your comment and other comments|

### Known Bugs

No known bugs

### Technologies Used

1. Python3.6
2. Flask
3. Postgres
4. HTML
5. CSS

### Support and contact details

If you have any comments, suggestions, questions, or contributions, please email me at [rosekairu@gmail.com]

### [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/rosekairu/NewsFeed/blob/master/LICENSE) <br>

Copyright (c) **Rose Kairu June 2020**