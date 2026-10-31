# PowerGuard — Electricity Theft Reporting & Vigilance Portal (Kotlin + Ktor)

A full-stack web application built with **Kotlin**, **Ktor Server (Netty)**, **Kotlinx Serialization**, **SQLite Local Persistence**, and a widescreen **HTML5/CSS3/JS** frontend implementing a **3-Role Vigilance Workflow** (**Citizen**, **Administrator**, and **Vigilance Officer**).

---

## 3-Role Workflow & Permissions

1. **Citizen (`CITIZEN`) — View & Make Reports Only**
   - Submits new Electricity Theft Reports with full name, contact mobile number, street address, nearest pole/landmark, theft category, severity, GPS coordinates, and photographic evidence.
   - Can view **"My Submitted Reports"** and track real-time status & officer audit history by Reference ID (`PG-2026-XXXX`).

2. **Administrator (`ADMIN`) — Assign Citizen Reports to Vigilance Officers**
   - Reviews all incoming Citizen electricity theft reports (`SUBMITTED`).
   - Assigns each report to a designated **Field Vigilance Officer** (`PATCH /api/reports/{refId}/assign`) along with priority severity and inspection instructions.
   - Views system-wide KPIs, category/status breakdowns, and exports CSV reports.

3. **Vigilance Officer (`OFFICER`) — Investigate Assigned Reports**
   - Views electricity theft reports **assigned to them by the Administrator** on the **Officer Investigation Desk**.
   - Inspects citizen descriptions, GPS coordinates, and photo evidence.
   - Updates investigation status (`UNDER_INVESTIGATION` $\rightarrow$ `TEAM_DISPATCHED` $\rightarrow$ `RESOLVED_CONFIRMED` or `DISMISSED`) and records official field inspection findings (`PATCH /api/reports/{refId}/investigate`).

---

## Portal Login Accounts

| Role | Username | Password | Name & Designation |
|------|----------|----------|--------------------|
| **Citizen** | `citizen` | `citizen123` | Rohan Deshmukh (Citizen User — or register a new Citizen account) |
| **Admin** | `admin` | `admin123` | Chief Vigilance Administrator |
| **Officer** | `officer1` | `officer123` | Er. Vikramaditya Deshmukh (`VIG-EI-09`) |
| **Officer** | `officer2` | `officer123` | Er. Priya Nair (`VIG-CC-01`) |
| **Officer** | `officer3` | `officer123` | Er. Rajesh Sharma (`VIG-NZ-04`) |
| **Officer** | `officer4` | `officer123` | Er. Ananya Verma (`VIG-SR-12`) |
| **Officer** | `officer5` | `officer123` | Er. Mohammed Farooq (`VIG-WR-07`) |

---

## How to Run

```powershell
.\gradlew.bat run
```

Then open **[http://localhost:8080](http://localhost:8080)** in your browser.
