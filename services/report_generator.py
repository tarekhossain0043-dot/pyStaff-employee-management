from datetime import datetime
from services.payroll import Payroll


class ReportGenerator:
    """Creates a text report from employee data."""

    def __init__(self):
        self.payroll = Payroll()

    def generate(self, employees):
        total_payroll = self.payroll.calculate_total_payroll(employees)

        departments = {}

        for employee in employees:
            department = employee.department
            departments[department] = departments.get(department, 0) + 1

        report_lines = [
            "========================================",
            "           EMPLOYEE REPORT",
            "========================================",
            "",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Total Employees: {len(employees)}",
            "",
            "Employees by Department:",
        ]

        if departments:
            for department, count in departments.items():
                report_lines.append(f"- {department}: {count}")
        else:
            report_lines.append("- No employees found.")

        report_lines.extend([
            "",
            f"Total Monthly Payroll: {total_payroll:,.2f} BDT",
            "",
            "========================================",
        ])

        report = "\n".join(report_lines)

        with open(
            "data/employee_report.txt",
            "w",
            encoding="utf-8"
        ) as file:
            file.write(report)

        return "data/employee_report.txt"
