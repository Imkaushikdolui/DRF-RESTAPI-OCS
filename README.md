# DRF-RESTAPI-OCS

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Description
Django Rest Framework - API for a online course application , having the following features

## Features
- User Registration and JWT Authentication
- Admin panel for managing courses, users, and content
- all the available features in `https://github.com/Imkaushikdolui/online_course_system_django.git`

## Installation and Usage
1. Clone the repository: `[git clone https://github.com/Imkaushikdolui/DRF-RESTAPI-OCS.git]`
2. Navigate to the project directory: `cd DRF-RESTAPI-OCS`
3. Create a virtual environment: `python -m venv env`
4. Activate the virtual environment:
   - For Windows: `.\env\Scripts\activate`
   - For macOS/Linux: `source env/bin/activate`
5. Install the dependencies: `pip install -r requirements.txt`
6. Apply database migrations: `python manage.py migrate`
7. Start the development server: `python manage.py runserver`
8. Access the application in your web browser at `http://localhost:8000`

## Configuration
- Database: By default, the project uses an SQLite database. Update the `DATABASES` settings in `settings.py` for production deployment.
- Email: Modify the email settings in `settings.py` to enable email functionality for user registration and notifications.

## Contributing
Contributions are welcome! If you have suggestions, bug reports, or feature requests, please open an issue or submit a pull request.

## License
This project is licensed under the [MIT License](LICENSE).
