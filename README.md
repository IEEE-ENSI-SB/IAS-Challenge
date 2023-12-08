E-Transport Django App:
The E-Transport Django app serves as the core platform connecting electric vehicle owners with available charging points.
This web application offers a user-friendly interface accessible to both electric vehicle owners and charging point providers.
Leveraging the Django framework's robustness, the app provides functionalities for seamless interaction, efficient route planning,
transparent transactions, and comprehensive monitoring tools.

Tech Stack:
Framework: Django (Python)
Database: PostgreSQL + Postgis extension
Frontend: HTML, CSS, JavaScript, Bootstrap, HTMX
Other Technologies: Utilization of blockchain technology for transaction transparency

The core functionality of the app resides within the Django app named "Functionalities" :

Models (models.py):
CustomUserManager & User models: Custom user model extending AbstractBaseUser for managing
user authentication and authorization. Includes fields for user details, such as:
email, username, phone, vehicle type, charger type, etc..

Blockchain Transactions (block.py):
Blockchain Transactions Class: Implements a simple blockchain structure to handle transactions between users and chargers.
Manages block creation, proof of work, block hashing, and chain validation.

URL Routing (urls.py):
Defines URL patterns for various views like Login, Register, Dashboard, Access, Logout, and Home.
HTMX URL Routing (urls.py):
Contains HTMX-specific URL patterns for searching user and charger transactions dynamically.

Views (views.py):
Login: Authenticates users based on email and password.
Register: Registers new users, storing necessary information.
user_logout: Logs out users from the system.
Home: Renders the home page.
Dashboard_User: Manages the user dashboard, transaction processing, and displays transactions made by the user and chargers.
search_User_transactions & search_Charger_transactions: AJAX endpoints for searching user and charger transactions respectively.

Templates (Authentication.html, Dashboard.html, Form.html, Home.html):
Authentication: Handles user login and registration forms.
Dashboard: Displays user-specific or charger-specific dashboard based on the user's role.
Form: Provides access to become a charging point.
Home: The home page of the web application.

Dependencies:
django 4.2.7 , psycopg2, pillow, django-htmx, GDAL-3.4.3-cp310-cp310-win_amd64.whl
