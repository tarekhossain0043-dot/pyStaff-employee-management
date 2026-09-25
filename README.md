# PyStaff — Employee Management & Payroll System

A beginner-friendly full-stack Python project designed to demonstrate Python OOP through a browser-based application.

## Stack

- Python
- Flask
- HTML
- CSS
- JavaScript
- JSON

## Main Python Concepts

- Classes and objects
- Inheritance
- `super()`
- Polymorphism
- Encapsulation
- Properties
- Methods
- Lists and dictionaries
- Exception handling
- File handling
- JSON persistence
- Modular project architecture

## Features

- Dashboard
- Employee CRUD
- Full-Time and Part-Time employees
- Search
- Payroll calculation
- Department overview
- Report generation
- JSON persistence
- Responsive UI

## Architecture

```text
Browser
  |
  | HTTP / JSON
  v
Flask Application
  |
  +--> EmployeeManager
  |
  +--> Employee / FullTimeEmployee / PartTimeEmployee
  |
  +--> Payroll
  |
  +--> ReportGenerator
  |
  v
JSON Storage
```

## Project Structure

```text
PyStaff_Web_Employee_Management_System/
│
├── app.py
├── requirements.txt
├── README.md
│
├── models/
│   ├── __init__.py
│   └── employee.py
│
├── services/
│   ├── __init__.py
│   ├── employee_manager.py
│   ├── payroll.py
│   └── report_generator.py
│
├── utils/
│   ├── __init__.py
│   └── file_manager.py
│
├── templates/
│   └── index.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
│
└── data/
    ├── employees.json
    └── employee_report.txt
```

## Local Setup

Create and activate a virtual environment if desired:

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Important OOP Example

`Employee` is the base class.

`FullTimeEmployee` and `PartTimeEmployee` inherit from it.

Both implement:

```python
calculate_salary()
```

Full-time salary:

```text
monthly_salary
```

Part-time salary:

```text
hourly_rate × working_hours
```

The `Payroll` class calls:

```python
employee.calculate_salary()
```

without needing to know the exact employee subclass. This demonstrates polymorphism.

## Deployment

This project can be deployed to a Python-capable hosting platform such as Render or Railway.

For production deployment, debug mode should be disabled and a production WSGI server should be used.

## Project Goal

The goal is not to demonstrate a large enterprise system. It is a practical beginner Python project showing how Python OOP can be connected to a real browser-based interface.
