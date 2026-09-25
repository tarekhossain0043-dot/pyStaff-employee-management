from flask import Flask, jsonify, render_template, request

from models.employee import FullTimeEmployee, PartTimeEmployee
from services.employee_manager import EmployeeManager
from services.payroll import Payroll
from services.report_generator import ReportGenerator
from utils.file_manager import FileManager


app = Flask(__name__)

DATA_FILE = "data/employees.json"

file_manager = FileManager(DATA_FILE)
employee_manager = EmployeeManager()
payroll = Payroll()
report_generator = ReportGenerator()

employee_manager.load_employees(file_manager)


def employee_to_dict(employee):
    data = employee.to_dict()
    data["employee_type"] = employee.employee_type
    data["salary"] = employee.calculate_salary()
    return data


@app.route("/")
def index():
    return render_template("index.html")


@app.get("/api/employees")
def get_employees():
    employees = employee_manager.get_all_employees()

    return jsonify({
        "success": True,
        "employees": [employee_to_dict(e) for e in employees]
    })


@app.post("/api/employees")
def add_employee():
    data = request.get_json() or {}

    required = ["employee_id", "name", "email", "department", "type"]

    if any(not data.get(field) for field in required):
        return jsonify({
            "success": False,
            "message": "Please fill in all required fields."
        }), 400

    try:
        if data["type"] == "full_time":
            salary = float(data["monthly_salary"])

            employee = FullTimeEmployee(
                data["employee_id"].strip(),
                data["name"].strip(),
                data["email"].strip(),
                data["department"].strip(),
                salary
            )

        elif data["type"] == "part_time":
            hourly_rate = float(data["hourly_rate"])
            working_hours = float(data["working_hours"])

            employee = PartTimeEmployee(
                data["employee_id"].strip(),
                data["name"].strip(),
                data["email"].strip(),
                data["department"].strip(),
                hourly_rate,
                working_hours
            )

        else:
            return jsonify({
                "success": False,
                "message": "Invalid employee type."
            }), 400

    except (ValueError, TypeError):
        return jsonify({
            "success": False,
            "message": "Salary and working hours must be valid numbers."
        }), 400

    if not employee_manager.add_employee(employee):
        return jsonify({
            "success": False,
            "message": "Employee ID already exists."
        }), 409

    employee_manager.save_employees(file_manager)

    return jsonify({
        "success": True,
        "message": "Employee added successfully.",
        "employee": employee_to_dict(employee)
    }), 201


@app.put("/api/employees/<employee_id>")
def update_employee(employee_id):
    employee = employee_manager.find_employee(employee_id)

    if not employee:
        return jsonify({
            "success": False,
            "message": "Employee not found."
        }), 404

    data = request.get_json() or {}

    updates = {
        "name": data.get("name", "").strip(),
        "email": data.get("email", "").strip(),
        "department": data.get("department", "").strip(),
    }

    try:
        if "salary" in data and data["salary"] != "":
            updates["salary"] = float(data["salary"])
    except (ValueError, TypeError):
        return jsonify({
            "success": False,
            "message": "Salary must be a valid number."
        }), 400

    employee_manager.update_employee(employee_id, updates)
    employee_manager.save_employees(file_manager)

    return jsonify({
        "success": True,
        "message": "Employee updated successfully.",
        "employee": employee_to_dict(employee)
    })


@app.delete("/api/employees/<employee_id>")
def delete_employee(employee_id):
    if not employee_manager.delete_employee(employee_id):
        return jsonify({
            "success": False,
            "message": "Employee not found."
        }), 404

    employee_manager.save_employees(file_manager)

    return jsonify({
        "success": True,
        "message": "Employee deleted successfully."
    })


@app.get("/api/payroll")
def get_payroll():
    employees = employee_manager.get_all_employees()

    rows = [
        {
            "employee_id": e.employee_id,
            "name": e.name,
            "employee_type": e.employee_type,
            "salary": payroll.calculate_employee_salary(e)
        }
        for e in employees
    ]

    return jsonify({
        "success": True,
        "rows": rows,
        "total": payroll.calculate_total_payroll(employees)
    })


@app.get("/api/report")
def generate_report():
    employees = employee_manager.get_all_employees()
    path = report_generator.generate(employees)

    return jsonify({
        "success": True,
        "message": "Report generated successfully.",
        "path": path
    })


@app.get("/api/dashboard")
def dashboard():
    employees = employee_manager.get_all_employees()

    full_time = sum(
        1 for employee in employees
        if employee.employee_type == "Full-Time"
    )

    part_time = sum(
        1 for employee in employees
        if employee.employee_type == "Part-Time"
    )

    departments = {}

    for employee in employees:
        departments[employee.department] = (
            departments.get(employee.department, 0) + 1
        )

    return jsonify({
        "success": True,
        "total_employees": len(employees),
        "full_time": full_time,
        "part_time": part_time,
        "total_payroll": payroll.calculate_total_payroll(employees),
        "departments": departments
    })


if __name__ == "__main__":
    app.run(debug=True)
