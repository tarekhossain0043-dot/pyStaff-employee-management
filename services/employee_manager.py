from models.employee import FullTimeEmployee, PartTimeEmployee


class EmployeeManager:
    """Handles employee collection and CRUD operations."""

    def __init__(self):
        self.employees = []

    def add_employee(self, employee):
        if self.find_employee(employee.employee_id):
            return False

        self.employees.append(employee)
        return True

    def get_all_employees(self):
        return self.employees

    def find_employee(self, employee_id):
        for employee in self.employees:
            if employee.employee_id == employee_id:
                return employee

        return None

    def update_employee(self, employee_id, updates):
        employee = self.find_employee(employee_id)

        if not employee:
            return False

        if updates.get("name"):
            employee.name = updates["name"]

        if updates.get("email"):
            employee.email = updates["email"]

        if updates.get("department"):
            employee.department = updates["department"]

        if "salary" in updates:
            if isinstance(employee, FullTimeEmployee):
                employee.monthly_salary = updates["salary"]
            elif isinstance(employee, PartTimeEmployee):
                employee.hourly_rate = updates["salary"]

        return True

    def delete_employee(self, employee_id):
        employee = self.find_employee(employee_id)

        if not employee:
            return False

        self.employees.remove(employee)
        return True

    def save_employees(self, file_manager):
        data = [employee.to_dict() for employee in self.employees]
        file_manager.write(data)

    def load_employees(self, file_manager):
        data = file_manager.read()

        for item in data:
            employee_type = item.get("type")

            if employee_type == "full_time":
                employee = FullTimeEmployee(
                    item["employee_id"],
                    item["name"],
                    item["email"],
                    item["department"],
                    item["monthly_salary"],
                )
            elif employee_type == "part_time":
                employee = PartTimeEmployee(
                    item["employee_id"],
                    item["name"],
                    item["email"],
                    item["department"],
                    item["hourly_rate"],
                    item["working_hours"],
                )
            else:
                continue

            self.employees.append(employee)
