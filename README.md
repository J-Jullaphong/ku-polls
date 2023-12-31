## KU Polls: Online Survey Questions Web Application

[![Django CI](https://github.com/J-Jullaphong/ku-polls/actions/workflows/django.yml/badge.svg)](https://github.com/J-Jullaphong/ku-polls/actions/workflows/django.yml)

The web application for online survey questions, wrote with Python and [Django](https://www.djangoproject.com/) web framework.
It is based on [Django Tutorial project][django-tutorial] with additional features.

This app was created as part of the [Individual Software Process](
https://cpske.github.io/ISP) course at Kasetsart University.

## Installation Instructions

Please read and follow the instructions in [Installation Instructions](Installation.md).

## How to Run Instructions

Before running the server, please make sure that the installation is completed.

1. Activate the virtual environment before using the application.
   - Linux and macOS
   ``` 
   source venv/bin/activate 
   ```
   - Windows
   ```  
   .\venv\Scripts\activate
   ```

2. Start the server. (If it doesn't work, please use `python3` instead of `python`)
   ```
   python manage.py runserver
   ```
   
3. To use this application, go to this link in your browser.
   ```
   http://localhost:8000
   ```

4. To close the running server, press `Ctrl+C` in your terminal or command prompt. 

5. After finish using the application, deactivate the virtual environment.
   ```
   deactivate
   ```

## Demo Users

Use these demo accounts to log in for testing.

|    Username     |     Password     |
|:---------------:|:----------------:|
| **demo_admin**  |  @demo_password  |
| **demo_user_1** | @demo_password_1 |
| **demo_user_2** | @demo_password_2 |

## Project Documents

All project documents are in the [Project Wiki](../../wiki/Home).

- [Vision Statement](../../wiki/Vision%20Statement)
- [Requirements](../../wiki/Requirements)
- [Development Plan](../../wiki/Development%20Plan)
- [Iteration 1 Plan](../../wiki/Iteration%201%20Plan)
- [Iteration 2 Plan](../../wiki/Iteration%202%20Plan)
- [Iteration 3 Plan](../../wiki/Iteration%203%20Plan)
- [Iteration 4 Plan](../../wiki/Iteration%204%20Plan)
- [Domain Model](../../wiki/Domain-Model)
- [Task Board](https://github.com/users/J-Jullaphong/projects/2)

[django-tutorial]: https://docs.djangoproject.com/en/4.1/intro/tutorial01/