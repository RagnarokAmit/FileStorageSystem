# Secure File Storage System

## Database Configuration

Before running the application, update the MySQL configuration in `app.py`.

Replace:

MYSQL_PASSWORD = "YOUR_MYSQL_PASSWORD"

with your local MySQL password.

Example:

MYSQL_PASSWORD = "your_actual_password"

Make sure the MySQL database `file_storage` is created using the provided `database.sql` file.

A simple file storage web application built using Flask and MySQL.

## Features

- User registration and login
- Password hashing
- Secure session authentication
- File upload and download
- User-specific file storage
- Protection against unauthorized file access
- File type validation
- Secure filename handling

## Technologies Used

- Python
- Flask
- MySQL
- HTML
- CSS
- Bootstrap

## Project Structure
FileStorageSystem/
│
├── app.py
├── database.sql
├── requirements.txt
│
├── uploads/
│
├── templates/
│
└── static/


## Security Measures

- Passwords are stored using hashing.
- SQL queries use parameterized statements to prevent SQL injection.
- Users can only access their own uploaded files.
- Uploaded filenames are sanitized using secure_filename().
- Unauthorized users cannot access protected pages.

## Installation

Clone the repository:
git clone <repository-link>


Install dependencies:


pip install -r requirements.txt


Create the MySQL database using:


database.sql


Update MySQL credentials in `app.py`.

Run:


python app.py


Open:


http://127.0.0.1:5000


## Demo Files

The application uses only synthetic/sample files for demonstration.
