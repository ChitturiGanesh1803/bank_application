# Union Bank Management System

## Overview

The Union Bank Management System is a Flask-based web application designed to simulate core banking operations. The application provides secure user authentication, account management, deposit and withdrawal transactions, transaction history tracking, and database-driven account storage using SQLite.

The project follows a modern banking workflow while maintaining a simple and user-friendly interface suitable for learning, academic projects, and portfolio demonstrations.

---

## Features

### User Authentication

* User Registration
* Secure Login
* Logout Functionality
* Session Management
* Protected Routes

### Account Management

* Create New Bank Account
* Auto-Generate Account Numbers
* Store Customer Information
* Search Account Details

### Banking Operations

* Deposit Money
* Withdraw Money
* Balance Updates
* Transaction Validation

### Transaction History

* View Complete Transaction Records
* Track Deposits and Withdrawals
* Timestamp-Based Transaction Logs

### Database Integration

* SQLite Database Support
* Persistent Data Storage
* Account Information Management
* Transaction Record Storage

### User Interface

* Professional Union Bank Inspired Design
* Responsive Layout
* Glassmorphism Components
* Modern Banking Dashboard
* Mobile Friendly Design
* Smooth Animations

---

## Technology Stack

### Backend

* Python
* Flask

### Frontend

* HTML5
* CSS3
* JavaScript

### Database

* SQLite

### Additional Libraries

* Flask
* Flask Session
* SQLite3

---

## Project Structure

```text
UnionBankManagementSystem/
│
├── app.py
├── database.db
├── requirements.txt
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── create_account.html
│   ├── deposit.html
│   ├── withdraw.html
│   └── transactions.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   ├── js/
│   │   └── script.js
│   │
│   └── images/
│
└── README.md
```

---

## Installation

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd UnionBankManagementSystem
```

### Step 2: Create Virtual Environment

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run Application

```bash
python app.py
```

### Step 5: Open Browser

```text
http://127.0.0.1:5000
```

---

## Application Workflow

### 1. Register

Create a new user account using the registration page.

### 2. Login

Login using registered credentials.

### 3. Dashboard

Access banking operations from the dashboard.

### 4. Create Account

Enter customer details and create a new bank account.

### 5. Deposit Amount

Deposit money into an existing account.

### 6. Withdraw Amount

Withdraw money from an account after balance validation.

### 7. Transaction History

View all transactions associated with accounts.

---

## Security Features

* User Authentication
* Session-Based Access Control
* Login Required Decorators
* Input Validation
* Database Transaction Safety
* Protected Banking Operations

---

## Future Enhancements

* OTP Verification
* Email Notifications
* SMS Alerts
* Loan Management Module
* Fund Transfer Between Accounts
* Admin Dashboard
* PDF Account Statements
* Online Banking Services
* UPI Integration
* Credit Card Services

---


### Home Page

Modern banking landing page with service information and navigation.

### Dashboard

Dedicated dashboard for banking operations.

### Create Account

Customer account creation interface.

### Deposit & Withdraw

Secure banking transaction pages.

### Transaction History

Detailed transaction records with timestamps.

---

## Learning Objectives

This project demonstrates:

* Flask Web Development
* Authentication Systems
* SQLite Database Operations
* CRUD Functionality
* Banking Application Workflow
* Frontend and Backend Integration
* Responsive UI Design

---

## Author

Developed by: Chitturi Sai Ganesh Kumar

Role: Python Developer

Experience: Python, Flask, Django, SQLite, HTML, CSS, JavaScript

---

## License

This project is intended for educational, learning, and portfolio purposes.

© 2026 Union Bank Management System. All Rights Reserved.
