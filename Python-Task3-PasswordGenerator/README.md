# Random Password Generator

A secure and user-friendly Random Password Generator developed using Python as part of the Oasis Infobyte Python Programming Internship.

## Task

**Task 3 - Random Password Generator**

## Description

This project is a graphical Random Password Generator developed using Python and Tkinter.

The application allows users to generate strong and customizable passwords by selecting the desired password length and character types. It also provides a password strength indicator and allows users to copy the generated password to the clipboard.

## Features

- Generate random passwords
- Minimum password length of 8 characters
- Select uppercase letters
- Select lowercase letters
- Select numbers
- Select symbols
- Requires at least two character types
- Guarantees selected character types in the password
- Secure password generation using Python's `secrets` module
- Password strength indicator
- Show/Hide password
- Copy password to clipboard
- Clear generated password
- Input validation
- User-friendly graphical interface

## Technologies Used

- Python
- Tkinter
- Secrets
- String

## Security

The application uses Python's built-in `secrets` module to generate passwords suitable for security-sensitive applications.

The generated password can contain:

- Uppercase letters (A-Z)
- Lowercase letters (a-z)
- Numbers (0-9)
- Symbols

The application also ensures that at least two selected character types are included in every generated password.

## How to Run

### 1. Install Python

Make sure Python 3.12 or later is installed on your system.

### 2. Open the project folder

Open the project folder in VS Code.

### 3. Run the application

Open the VS Code terminal and run:

```bash
python password_generator.py