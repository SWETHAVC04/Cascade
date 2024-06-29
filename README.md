# Cascade: Multi-Factor Authentication System
Cascade is a Django-based web application that enhances user security through multi-factor authentication (MFA). It provides three layers of authentication: username/password, OTP (One-Time Password), and Captcha verification. This project includes user registration, forgot password/reset password functionalities, and a secure logout mechanism.

# Features
Multi-Factor Authentication (MFA):

Username/Password authentication.
OTP via email for added security.
Captcha verification to prevent automated attacks.

# User Management:

User registration with email verification.
Forgot password/reset password functionality.

# Security:

Secure storage of user credentials using Django's built-in authentication system.

# User Interface:

Responsive design using HTML and CSS.
Intuitive user interfaces for login, registration, password reset, and profile management.

# Installation
To run Cascade locally, follow these steps:

Clone the repository:

# bash

git clone
cd cascade
Set up virtual environment (optional but recommended):

# bash

python -m venv env
source env/bin/activate  # For Windows: env\Scripts\activate

# Install dependencies:

# bash

pip install -r requirements.txt

# Run migrations:

# bash

python manage.py migrate

# Create a superuser (for admin access):

# bash

python manage.py createsuperuser

# Run the development server:

# bash

python manage.py runserver

# Access the application:
Open your web browser and go to http://localhost:8000/ to view the application.

Configuration
Environment Variables: Configure sensitive information (e.g., API keys, database credentials) using environment variables or a .env file. Refer to example.env for an example configuration.

Database: By default, Cascade uses SQLite for ease of setup. For production, consider using PostgreSQL or MySQL for better performance and scalability.

Usage
User Registration: Users can register with their email and set up their initial password.
Login: Authenticate using username/password. Upon successful authentication, users will be prompted for OTP and Captcha verification.
Forgot Password: Users can reset their password via email verification.
Logout: Securely terminate the session to prevent unauthorized access.
