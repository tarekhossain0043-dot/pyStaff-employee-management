class Payroll:
    """Handles salary calculations."""

    def calculate_employee_salary(self, employee):
        # Polymorphism: employee decides how salary is calculated.
        return employee.calculate_salary()

    def calculate_total_payroll(self, employees):
        total = 0

        for employee in employees:
            total += self.calculate_employee_salary(employee)

        return total
