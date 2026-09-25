class Employee:
    """Base class representing a general employee."""

    def __init__(self, employee_id, name, email, department):
        self.employee_id = employee_id
        self.name = name
        self.email = email
        self.department = department

    @property
    def employee_type(self):
        return "General"

    def calculate_salary(self):
        raise NotImplementedError(
            "Subclasses must implement calculate_salary()."
        )

    def display_info(self):
        print(f"ID: {self.employee_id}")
        print(f"Name: {self.name}")
        print(f"Email: {self.email}")
        print(f"Department: {self.department}")

    def to_dict(self):
        raise NotImplementedError("Subclasses must implement to_dict().")


class FullTimeEmployee(Employee):
    """Employee paid a fixed monthly salary."""

    def __init__(
        self,
        employee_id,
        name,
        email,
        department,
        monthly_salary,
    ):
        super().__init__(
            employee_id,
            name,
            email,
            department,
        )
        self.monthly_salary = monthly_salary

    @property
    def employee_type(self):
        return "Full-Time"

    def calculate_salary(self):
        return self.monthly_salary

    def to_dict(self):
        return {
            "employee_id": self.employee_id,
            "name": self.name,
            "email": self.email,
            "department": self.department,
            "type": "full_time",
            "monthly_salary": self.monthly_salary,
        }


class PartTimeEmployee(Employee):
    """Employee paid according to hourly rate and working hours."""

    def __init__(
        self,
        employee_id,
        name,
        email,
        department,
        hourly_rate,
        working_hours,
    ):
        super().__init__(
            employee_id,
            name,
            email,
            department,
        )
        self.hourly_rate = hourly_rate
        self.working_hours = working_hours

    @property
    def employee_type(self):
        return "Part-Time"

    def calculate_salary(self):
        return self.hourly_rate * self.working_hours

    def to_dict(self):
        return {
            "employee_id": self.employee_id,
            "name": self.name,
            "email": self.email,
            "department": self.department,
            "type": "part_time",
            "hourly_rate": self.hourly_rate,
            "working_hours": self.working_hours,
        }
