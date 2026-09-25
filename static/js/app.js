const state = {
    employees: [],
    currentSection: "dashboard",
};

const $ = (selector) => document.querySelector(selector);

const formatMoney = (value) => {
    return `৳${Number(value || 0).toLocaleString("en-BD", {
        maximumFractionDigits: 2,
    })}`;
};

const showToast = (message) => {
    const toast = $("#toast");
    toast.textContent = message;
    toast.classList.add("show");

    setTimeout(() => {
        toast.classList.remove("show");
    }, 2600);
};

const api = async (url, options = {}) => {
    const response = await fetch(url, {
        headers: {
            "Content-Type": "application/json",
            ...(options.headers || {}),
        },
        ...options,
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.message || "Something went wrong.");
    }

    return data;
};

const switchSection = async (section) => {
    state.currentSection = section;

    document.querySelectorAll(".nav-item").forEach((button) => {
        button.classList.toggle(
            "active",
            button.dataset.section === section
        );
    });

    document.querySelectorAll(".section").forEach((element) => {
        element.classList.toggle(
            "active",
            element.id === `${section}-section`
        );
    });

    const titles = {
        dashboard: "Dashboard",
        employees: "Employees",
        payroll: "Payroll",
        reports: "Reports",
    };

    $("#page-title").textContent = titles[section];

    if (section === "dashboard") {
        await loadDashboard();
    }

    if (section === "employees") {
        await loadEmployees();
    }

    if (section === "payroll") {
        await loadPayroll();
    }
};

const loadDashboard = async () => {
    const data = await api("/api/dashboard");

    $("#total-employees").textContent = data.total_employees;
    $("#full-time").textContent = data.full_time;
    $("#part-time").textContent = data.part_time;
    $("#total-payroll").textContent = formatMoney(data.total_payroll);

    const departments = Object.entries(data.departments);
    const max = Math.max(...departments.map(([, count]) => count), 1);

    if (!departments.length) {
        $("#department-list").innerHTML =
            '<div class="empty">No employee data available.</div>';
        return;
    }

    $("#department-list").innerHTML = departments
        .map(([department, count]) => {
            const width = (count / max) * 100;

            return `
                <div class="department-row">
                    <span>${escapeHtml(department)}</span>
                    <div class="progress">
                        <span style="width:${width}%"></span>
                    </div>
                    <strong>${count}</strong>
                </div>
            `;
        })
        .join("");
};

const loadEmployees = async () => {
    const data = await api("/api/employees");
    state.employees = data.employees;

    renderEmployees(state.employees);
};

const renderEmployees = (employees) => {
    const table = $("#employee-table");

    if (!employees.length) {
        table.innerHTML =
            '<tr><td colspan="6" class="empty">No employees found.</td></tr>';
        return;
    }

    table.innerHTML = employees
        .map(
            (employee) => `
            <tr>
                <td><strong>${escapeHtml(employee.employee_id)}</strong></td>
                <td>
                    <strong>${escapeHtml(employee.name)}</strong><br>
                    <small>${escapeHtml(employee.email)}</small>
                </td>
                <td>${escapeHtml(employee.department)}</td>
                <td><span class="badge">${escapeHtml(employee.employee_type)}</span></td>
                <td>${formatMoney(employee.salary)}</td>
                <td>
                    <button class="action-btn" onclick="openEditModal('${employee.employee_id}')">
                        Edit
                    </button>
                    <button class="action-btn delete" onclick="deleteEmployee('${employee.employee_id}')">
                        Delete
                    </button>
                </td>
            </tr>
        `
        )
        .join("");
};

const loadPayroll = async () => {
    const data = await api("/api/payroll");

    if (!data.rows.length) {
        $("#payroll-table").innerHTML =
            '<tr><td colspan="4" class="empty">No payroll records.</td></tr>';
    } else {
        $("#payroll-table").innerHTML = data.rows
            .map(
                (row) => `
                <tr>
                    <td><strong>${escapeHtml(row.employee_id)}</strong></td>
                    <td>${escapeHtml(row.name)}</td>
                    <td><span class="badge">${escapeHtml(row.employee_type)}</span></td>
                    <td>${formatMoney(row.salary)}</td>
                </tr>
            `
            )
            .join("");
    }

    $("#payroll-total").textContent = formatMoney(data.total);
};

const openAddModal = () => {
    $("#modal-title").textContent = "Add Employee";
    $("#employee-form").reset();
    $("#editing-id").value = "";
    $("#employee-id").disabled = false;
    updateTypeFields();
    $("#modal").classList.add("open");
};

window.openEditModal = (employeeId) => {
    const employee = state.employees.find(
        (item) => item.employee_id === employeeId
    );

    if (!employee) return;

    $("#modal-title").textContent = "Edit Employee";
    $("#editing-id").value = employee.employee_id;
    $("#employee-id").value = employee.employee_id;
    $("#employee-id").disabled = true;
    $("#name").value = employee.name;
    $("#email").value = employee.email;
    $("#department").value = employee.department;

    if (employee.type === "part_time") {
        $("#type").value = "part_time";
        $("#hourly-rate").value = employee.hourly_rate;
        $("#working-hours").value = employee.working_hours;
    } else {
        $("#type").value = "full_time";
        $("#salary").value = employee.monthly_salary;
    }

    updateTypeFields();
    $("#modal").classList.add("open");
};

const closeModal = () => {
    $("#modal").classList.remove("open");
};

const updateTypeFields = () => {
    const type = $("#type").value;
    const isPartTime = type === "part_time";
    const isEditing = Boolean($("#editing-id").value);

    $("#salary-label").classList.toggle("hidden", isPartTime);
    $("#hourly-label").classList.toggle("hidden", !isPartTime);
    $("#hours-label").classList.toggle("hidden", !isPartTime);

    $("#salary").required = !isPartTime && !isEditing;
    $("#hourly-rate").required = isPartTime && !isEditing;
    $("#working-hours").required = isPartTime && !isEditing;
};

const submitEmployee = async (event) => {
    event.preventDefault();

    const editingId = $("#editing-id").value;
    const type = $("#type").value;

    try {
        if (editingId) {
            const salary = type === "full_time"
                ? $("#salary").value
                : $("#hourly-rate").value;

            await api(`/api/employees/${editingId}`, {
                method: "PUT",
                body: JSON.stringify({
                    name: $("#name").value,
                    email: $("#email").value,
                    department: $("#department").value,
                    salary,
                }),
            });

            showToast("Employee updated successfully.");
        } else {
            const payload = {
                employee_id: $("#employee-id").value,
                name: $("#name").value,
                email: $("#email").value,
                department: $("#department").value,
                type,
            };

            if (type === "full_time") {
                payload.monthly_salary = $("#salary").value;
            } else {
                payload.hourly_rate = $("#hourly-rate").value;
                payload.working_hours = $("#working-hours").value;
            }

            await api("/api/employees", {
                method: "POST",
                body: JSON.stringify(payload),
            });

            showToast("Employee added successfully.");
        }

        closeModal();
        await loadEmployees();
        await loadDashboard();
    } catch (error) {
        showToast(error.message);
    }
};

window.deleteEmployee = async (employeeId) => {
    const confirmed = window.confirm(
        `Delete employee ${employeeId}?`
    );

    if (!confirmed) return;

    try {
        await api(`/api/employees/${employeeId}`, {
            method: "DELETE",
        });

        showToast("Employee deleted successfully.");
        await loadEmployees();
        await loadDashboard();
    } catch (error) {
        showToast(error.message);
    }
};

const generateReport = async () => {
    try {
        const data = await api("/api/report");
        showToast(data.message);
    } catch (error) {
        showToast(error.message);
    }
};

const escapeHtml = (value) => {
    return String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
};

document.querySelectorAll(".nav-item").forEach((button) => {
    button.addEventListener("click", () => {
        switchSection(button.dataset.section);
    });
});

$("#header-add-btn").addEventListener("click", openAddModal);
$("#employee-add-btn").addEventListener("click", openAddModal);
$("#quick-manage-btn").addEventListener("click", () => {
    switchSection("employees");
});

$("#close-modal").addEventListener("click", closeModal);
$("#cancel-btn").addEventListener("click", closeModal);
$("#type").addEventListener("change", updateTypeFields);
$("#employee-form").addEventListener("submit", submitEmployee);
$("#generate-report-btn").addEventListener("click", generateReport);

$("#search-input").addEventListener("input", (event) => {
    const query = event.target.value.toLowerCase().trim();

    const filtered = state.employees.filter((employee) => {
        return [
            employee.employee_id,
            employee.name,
            employee.email,
            employee.department,
            employee.employee_type,
        ].some((value) =>
            String(value).toLowerCase().includes(query)
        );
    });

    renderEmployees(filtered);
});

window.addEventListener("click", (event) => {
    if (event.target === $("#modal")) {
        closeModal();
    }
});

loadDashboard();
loadEmployees();
