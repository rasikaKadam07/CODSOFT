#  Professional Password Manager

##  Description
A secure, encrypted password manager that stores your passwords safely. Built as Task 2 for CodSoft Python Internship.

##  Features
- **Encrypted Storage** - All passwords are encrypted using Fernet (symmetric encryption)
- **Master Password** - Single master password to access your vault
- **Password Generator** - Generate strong, random passwords
- **Password Strength Checker** - Analyzes password security
- **Copy to Clipboard** - One-click password copying
- **Search & Organize** - Find passwords quickly
- **Strength Report** - See weak passwords at a glance
## Installation
1. How to install
    ```bash
    pip install cryptography rich pyperclip

## How to Run
    python password_manager.py

## Usage Guide
    First Time Setup
    Run the program

    Create a master password (remember this!)

    Your encrypted vault is created automatically

    Adding Passwords
    Select "Add New Password"

    Enter service name and username

    Generate a strong password or enter your own

    Add optional notes

    Viewing Passwords
    Passwords are masked for security

    Select any entry to view/copy the full password

## Security Features
    AES-128 encryption via Fernet

    Master password hashed with SHA-256

    Local storage only (no cloud)

    Passwords never logged or transmitted

##  Project Structure
    Task2_Password_Manager/
    ├── password_manager.py
    ├── requirements.txt
    ├── README.md
    └── data/
        ├── secret.key      (encryption key)
        ├── vault.enc       (encrypted passwords)
        └── master.hash     (hashed master password)

## Learning Outcomes
    Encryption/decryption implementation

    File handling with JSON

    Password security best practices

    Rich library for CLI UI

    Object-oriented programming

## Author
    Rasika .H. Kadam
    

## Date
    May 2026


