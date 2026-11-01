import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def create_report():
    doc = Document()

    # Set standard 1-inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
        # Configure footer
        footer = section.footer
        f_p = footer.paragraphs[0]
        f_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        f_run = f_p.add_run("Department of Computer Science & Engineering-(AI&ML) | APSIT")
        f_run.font.name = "Times New Roman"
        f_run.font.size = Pt(9.5)
        f_run.font.bold = True
        f_run.font.color.rgb = RGBColor(100, 116, 139)

    def set_run_font(run, name="Times New Roman", size=12, bold=False, italic=False, color=None):
        run.font.name = name
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.italic = italic
        if color:
            run.font.color.rgb = color

    def add_page_header(doc):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2)
        r1 = p.add_run("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING\n(ARTIFICIAL INTELLIGENCE AND MACHINE LEARNING)")
        set_run_font(r1, name="Times New Roman", size=11, bold=True, color=RGBColor(30, 41, 59))
        
        p_div = doc.add_paragraph()
        p_div.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_div.paragraph_format.space_before = Pt(0)
        p_div.paragraph_format.space_after = Pt(14)
        r_div = p_div.add_run("_________________________________________________________________________________")
        set_run_font(r_div, name="Times New Roman", size=8, color=RGBColor(203, 213, 225))

    # =========================================================================
    # PAGE 1: COVER PAGE
    # =========================================================================
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(10)
    p_inst.paragraph_format.space_after = Pt(2)
    r_trust = p_inst.add_run("Parshvanath Charitable Trust's\n")
    set_run_font(r_trust, name="Times New Roman", size=11, italic=True)
    r_college = p_inst.add_run("A. P. SHAH INSTITUTE OF TECHNOLOGY\n")
    set_run_font(r_college, name="Times New Roman", size=16, bold=True, color=RGBColor(15, 23, 42))
    r_app = p_inst.add_run("(Approved by AICTE New Delhi & Govt. of Maharashtra, Affiliated to University of Mumbai)\n(Religious Jain Minority)")
    set_run_font(r_app, name="Times New Roman", size=9.5, italic=True, color=RGBColor(71, 85, 105))

    p_dept = doc.add_paragraph()
    p_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dept.paragraph_format.space_before = Pt(14)
    p_dept.paragraph_format.space_after = Pt(24)
    r_d = p_dept.add_run("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING\n(ARTIFICIAL INTELLIGENCE AND MACHINE LEARNING)")
    set_run_font(r_d, name="Times New Roman", size=12, bold=True, color=RGBColor(30, 41, 59))

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(18)
    p_title.paragraph_format.space_after = Pt(12)
    r_t_label = p_title.add_run("Title — ")
    set_run_font(r_t_label, name="Times New Roman", size=14, bold=True)
    r_t_val = p_title.add_run("POWERGUARD: ELECTRICITY THEFT REPORTING & VIGILANCE PORTAL")
    set_run_font(r_t_val, name="Times New Roman", size=15, bold=True, color=RGBColor(2, 132, 199))

    p_rep = doc.add_paragraph()
    p_rep.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_rep.paragraph_format.space_before = Pt(16)
    p_rep.paragraph_format.space_after = Pt(6)
    r_rep = p_rep.add_run("MINI PROJECT REPORT")
    set_run_font(r_rep, name="Times New Roman", size=14, bold=True, color=RGBColor(15, 23, 42))

    p_ay = doc.add_paragraph()
    p_ay.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ay.paragraph_format.space_before = Pt(4)
    p_ay.paragraph_format.space_after = Pt(24)
    r_ay = p_ay.add_run("Academic Year: 2026-27")
    set_run_font(r_ay, name="Times New Roman", size=12, bold=True)

    p_topic = doc.add_paragraph()
    p_topic.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_topic.paragraph_format.space_before = Pt(10)
    p_topic.paragraph_format.space_after = Pt(4)
    r_top_lbl = p_topic.add_run("Topic:\n")
    set_run_font(r_top_lbl, name="Times New Roman", size=13, bold=True)
    r_top_val = p_topic.add_run("Role-Based Web Platform for Electricity Theft Reporting, Evidence Verification & Field Investigation Management")
    set_run_font(r_top_val, name="Times New Roman", size=12, italic=True)

    p_stud = doc.add_paragraph()
    p_stud.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_stud.paragraph_format.space_before = Pt(24)
    p_stud.paragraph_format.space_after = Pt(28)
    r_s_lbl = p_stud.add_run("Submitted by:\n")
    set_run_font(r_s_lbl, name="Times New Roman", size=11, bold=True)
    r_s_val = p_stud.add_run("Pratik Mali\n(Moodle ID: 22104037)")
    set_run_font(r_s_val, name="Times New Roman", size=13, bold=True, color=RGBColor(15, 23, 42))

    p_guide = doc.add_paragraph()
    p_guide.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_guide.paragraph_format.space_before = Pt(20)
    p_guide.paragraph_format.space_after = Pt(10)
    r_g_lbl = p_guide.add_run("Under the guidance of:\n")
    set_run_font(r_g_lbl, name="Times New Roman", size=11, bold=True)
    r_g_val = p_guide.add_run("Prof. Vijesh Mundokalam")
    set_run_font(r_g_val, name="Times New Roman", size=13, bold=True, color=RGBColor(15, 23, 42))

    doc.add_page_break()

    # =========================================================================
    # PAGE 2: TABLE OF CONTENTS
    # =========================================================================
    add_page_header(doc)

    p_toc_title = doc.add_paragraph()
    p_toc_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_toc_title.paragraph_format.space_before = Pt(10)
    p_toc_title.paragraph_format.space_after = Pt(20)
    r_toc = p_toc_title.add_run("TABLE OF CONTENTS")
    set_run_font(r_toc, name="Times New Roman", size=14, bold=True, color=RGBColor(15, 23, 42))

    toc_table = doc.add_table(rows=1, cols=3)
    toc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_cells = toc_table.rows[0].cells
    hdr_cells[0].text = "Sr. No."
    hdr_cells[1].text = "Chapter Title"
    hdr_cells[2].text = "Page No."

    for cell in hdr_cells:
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                set_run_font(r, name="Times New Roman", size=11, bold=True, color=RGBColor(15, 23, 42))

    toc_data = [
        ("1", "CHAPTER 1: INTRODUCTION", "3"),
        ("2", "CHAPTER 2: PROBLEM STATEMENT", "4"),
        ("3", "CHAPTER 3: TECHNOLOGY & TOOLS", "5"),
        ("4", "CHAPTER 4: IMPLEMENTATION & SOURCE CODE", "6"),
        ("5", "CHAPTER 5: CONCLUSION & FUTURE SCOPE", "7"),
        ("6", "CHAPTER 6: SUSTAINABLE DEVELOPMENT GOALS (SDG) MAPPING", "8"),
        ("7", "CHAPTER 7: REFERENCES", "9")
    ]

    for sr, ch, pg in toc_data:
        row_cells = toc_table.add_row().cells
        row_cells[0].text = sr
        row_cells[1].text = ch
        row_cells[2].text = pg
        row_cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        row_cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT
        row_cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        for cell in row_cells:
            for p in cell.paragraphs:
                for r in p.runs:
                    set_run_font(r, name="Times New Roman", size=11)

    p_note = doc.add_paragraph()
    p_note.paragraph_format.space_before = Pt(40)
    r_note = p_note.add_run("[Note: The report follows the Department of Computer Science & Engineering (AI&ML), A. P. Shah Institute of Technology prescribed academic mini project documentation standard.]")
    set_run_font(r_note, name="Times New Roman", size=10, italic=True, color=RGBColor(100, 116, 139))

    doc.add_page_break()

    # =========================================================================
    # PAGE 3: CHAPTER 1: INTRODUCTION
    # =========================================================================
    add_page_header(doc)

    p_c1 = doc.add_paragraph()
    p_c1.paragraph_format.space_before = Pt(10)
    p_c1.paragraph_format.space_after = Pt(12)
    r_c1 = p_c1.add_run("CHAPTER 1: INTRODUCTION")
    set_run_font(r_c1, name="Times New Roman", size=14, bold=True, color=RGBColor(15, 23, 42))

    p_i_lbl = doc.add_paragraph()
    p_i_lbl.paragraph_format.space_after = Pt(8)
    r_i_lbl = p_i_lbl.add_run("⮚ Introduction:")
    set_run_font(r_i_lbl, name="Times New Roman", size=12, bold=True)

    intro_p1 = doc.add_paragraph()
    intro_p1.paragraph_format.space_after = Pt(10)
    intro_p1.paragraph_format.line_spacing = 1.15
    r_ip1 = intro_p1.add_run(
        "Electrical power distribution is one of the most vital arteries of modern economic and civil infrastructure. "
        "However, power distribution utilities worldwide—and particularly across emerging economies—face persistent operational "
        "and revenue distress attributable to non-technical losses (NTL), predominantly driven by electricity theft. "
        "Electricity theft manifests through multiple clandestine mechanisms, including direct wire hooking into overhead low-tension (LT) lines "
        "(commonly termed 'kundi' connections), physical meter tampering, internal shunt bypasses, unauthorized transformer taps, broken seals, "
        "and illegal commercial sub-metering. Beyond causing staggering financial deficits that cripple utility reinvestment in grid modernization, "
        "unregulated electrical tampering induces severe transformer overloads, voltage instability, localized blackouts, and grave public safety "
        "hazards such as residential electrical fires and fatal electrocutions."
    )
    set_run_font(r_ip1, name="Times New Roman", size=11.5)

    intro_p2 = doc.add_paragraph()
    intro_p2.paragraph_format.space_after = Pt(10)
    intro_p2.paragraph_format.line_spacing = 1.15
    r_ip2 = intro_p2.add_run(
        "To mitigate these challenges, this project introduces PowerGuard—an automated, full-stack, role-based electricity theft reporting "
        "and vigilance management platform engineered using Kotlin, Ktor Server, SQLite local persistence, and an interactive, responsive web frontend. "
        "The system replaces conventional, error-prone manual complaint registries with a transparent, closed-loop vigilance ecosystem structured around "
        "three distinct stakeholder roles: Citizens, Central Administrators, and Field Vigilance Officers. "
        "Citizens can swiftly register verified complaints with nearest pole numbers, geo-coordinates, and photographic evidence. "
        "The Central Administrator monitors real-time Key Performance Indicators (KPIs), triages complaints by hazard severity, and delegates cases to "
        "designated Field Vigilance Officers. In turn, Officers inspect field sites, review attached evidence, update digital investigation logs, and serve "
        "penalty assessments. By digitizing the end-to-end audit trail, PowerGuard establishes accountability, preserves digital evidence chains of custody, "
        "and drastically reduces the turnaround time for power theft remediation."
    )
    set_run_font(r_ip2, name="Times New Roman", size=11.5)

    doc.add_page_break()

    # =========================================================================
    # PAGE 4: CHAPTER 2: PROBLEM STATEMENT
    # =========================================================================
    add_page_header(doc)

    p_c2 = doc.add_paragraph()
    p_c2.paragraph_format.space_before = Pt(10)
    p_c2.paragraph_format.space_after = Pt(12)
    r_c2 = p_c2.add_run("CHAPTER 2: PROBLEM STATEMENT")
    set_run_font(r_c2, name="Times New Roman", size=14, bold=True, color=RGBColor(15, 23, 42))

    p_ps_lbl = doc.add_paragraph()
    p_ps_lbl.paragraph_format.space_after = Pt(8)
    r_ps_lbl = p_ps_lbl.add_run("⮚ Problem Statement:")
    set_run_font(r_ps_lbl, name="Times New Roman", size=12, bold=True)

    ps_p1 = doc.add_paragraph()
    ps_p1.paragraph_format.space_after = Pt(10)
    ps_p1.paragraph_format.line_spacing = 1.15
    r_psp1 = ps_p1.add_run(
        "In contemporary electrical power distribution networks, non-technical losses caused by electricity theft account for an estimated "
        "20% to 30% of total generated power, leading to annual commercial revenue leakages in the billions of rupees for State Electricity Distribution "
        "Companies (DISCOMs). Despite the severity of this issue, existing grievance and vigilance mechanisms suffer from acute systemic bottlenecks:\n\n"
        "1. Absence of Citizen Whistleblower Accessibility: Consumers who witness hazardous illegal hookings or meter tampering lack an accessible, "
        "instantaneous, and transparent digital channel to file complaints directly with vigilance enforcement squads.\n"
        "2. Lack of Verifiable Photographic Evidence: Traditional helpline or paper-based complaints are purely textual and frequently lack precise electric "
        "pole identifiers, landmarks, and visual evidence, resulting in high rates of dismissed inquiries or futile field inspections.\n"
        "3. Fragmented Administrative Allocation & Delays: Central vigilance control rooms lack a centralized automated triage system to categorize "
        "complaint severity, track pending cases, and assign them systematically to designated field vigilance officers according to operational zones.\n"
        "4. Broken Chain-of-Custody and Auditability: Manual paper records fail to maintain immutable chronological logs of site inspections, seizure "
        "findings, and status updates, creating vulnerabilities to bureaucratic inertia, lack of accountability, and tampering.\n\n"
        "Therefore, the core objective of this project is to develop PowerGuard—a secure, role-based, closed-loop web application that enables verified "
        "citizens to submit geo-tagged complaints with photo evidence, empowers administrators to assign and monitor cases in real-time, and equips "
        "vigilance officers with a digital desk to conduct field inspections, confirm violations, and record legal audit histories."
    )
    set_run_font(r_psp1, name="Times New Roman", size=11.5)

    doc.add_page_break()

    # =========================================================================
    # PAGE 5: CHAPTER 3: TECHNOLOGY & TOOLS
    # =========================================================================
    add_page_header(doc)

    p_c3 = doc.add_paragraph()
    p_c3.paragraph_format.space_before = Pt(10)
    p_c3.paragraph_format.space_after = Pt(12)
    r_c3 = p_c3.add_run("CHAPTER 3: TECHNOLOGY & TOOLS")
    set_run_font(r_c3, name="Times New Roman", size=14, bold=True, color=RGBColor(15, 23, 42))

    p_tt_lbl = doc.add_paragraph()
    p_tt_lbl.paragraph_format.space_after = Pt(8)
    r_tt_lbl = p_tt_lbl.add_run("⮚ Tools & Methodologies:")
    set_run_font(r_tt_lbl, name="Times New Roman", size=12, bold=True)

    tech_p = doc.add_paragraph()
    tech_p.paragraph_format.space_after = Pt(10)
    tech_p.paragraph_format.line_spacing = 1.15
    r_tp = tech_p.add_run(
        "The PowerGuard platform is built upon a resilient, modern, and lightweight technology stack selected to maximize execution performance, "
        "ensure thread safety, and provide seamless responsiveness across devices without redundant framework bloat:\n\n"
        "1. Backend Programming Language — Kotlin (v2.2.20):\n"
        "Kotlin provides complete null safety, concise syntax, expressive data classes, and native coroutines. Its strong type system prevents runtime "
        "null pointer exceptions, ensuring high stability in critical utility infrastructure services.\n\n"
        "2. Asynchronous Server Framework — Ktor Server (Netty Engine):\n"
        "Ktor is a lightweight, non-blocking asynchronous web framework designed by JetBrains. Powered by the Netty engine, Ktor handles concurrent HTTP "
        "requests with low memory footprint and high throughput, making it ideal for event-driven vigilance alerting and real-time dashboard telemetry.\n\n"
        "3. Serialization & Content Negotiation — kotlinx.serialization:\n"
        "Employed for JSON data serialization and deserialization, converting complex Kotlin domain models into structured JSON payloads for seamless REST API communication.\n\n"
        "4. Database & Persistence Layer — SQLite Engine:\n"
        "A relational SQLite database (data/powerguard.db) provides local ACID-compliant persistence for user credentials, role permissions, and complaint records. "
        "To ensure continuous data durability and visual auditing, the storage layer implements a dual-persistence mechanism that synchronizes SQLite rows with "
        "a human-readable JSON mirror (data/reports_mirror.json) and extracts uploaded evidence images into a dedicated filesystem folder (data/evidence_images/).\n\n"
        "5. Frontend Presentation Layer — Responsive HTML5, Modern CSS3, & Vanilla JavaScript:\n"
        "The single-page web interface uses modern CSS custom properties (variables), flexible box/grid layouts, and reactive DOM manipulation without bloated "
        "frontend dependencies. It includes an embedded SQLite Database Visual Inspector (data/view_database.html) with image lightbox capabilities.\n\n"
        "6. Development Environment & Build Automation:\n"
        "Built using Gradle 9.1 Wrapper (Kotlin DSL), IntelliJ IDEA / Visual Studio Code, Git Version Control, and hosted on GitHub."
    )
    set_run_font(r_tp, name="Times New Roman", size=11.5)

    doc.add_page_break()

    # =========================================================================
    # PAGE 6: CHAPTER 4: IMPLEMENTATION & SOURCE CODE
    # =========================================================================
    add_page_header(doc)

    p_c4 = doc.add_paragraph()
    p_c4.paragraph_format.space_before = Pt(10)
    p_c4.paragraph_format.space_after = Pt(12)
    r_c4 = p_c4.add_run("CHAPTER 4: IMPLEMENTATION & SOURCE CODE")
    set_run_font(r_c4, name="Times New Roman", size=14, bold=True, color=RGBColor(15, 23, 42))

    p_imp_lbl = doc.add_paragraph()
    p_imp_lbl.paragraph_format.space_after = Pt(8)
    r_imp_lbl = p_imp_lbl.add_run("⮚ Implementation and source code:")
    set_run_font(r_imp_lbl, name="Times New Roman", size=12, bold=True)

    imp_p1 = doc.add_paragraph()
    imp_p1.paragraph_format.space_after = Pt(8)
    imp_p1.paragraph_format.line_spacing = 1.15
    r_im1 = imp_p1.add_run(
        "PowerGuard implements a modular, three-tier Role-Based Access Control (RBAC) architecture separating presentation, "
        "business logic, and persistent storage. The operational flow and core code modules are detailed below:"
    )
    set_run_font(r_im1, name="Times New Roman", size=11.5)

    # Architectural flow box
    p_arch = doc.add_paragraph()
    p_arch.paragraph_format.space_after = Pt(10)
    p_arch.paragraph_format.line_spacing = 1.15
    r_arch = p_arch.add_run(
        "Figure 4.1: System Operational Architecture & Stakeholder Workflow\n"
        "[Citizen Portal]  --> Registers theft report with GPS, landmark & Base64 photo --> [POST /api/reports]\n"
        "                             ↓\n"
        "[SQLite Database] --> Assigns unique Reference ID (e.g. PG-2026-1084), stores row & extracts image file\n"
        "                             ↓\n"
        "[Admin Center]   --> Reviews incoming cases, inspects photo & assigns Officer --> [PATCH /api/reports/{id}/assign]\n"
        "                             ↓\n"
        "[Officer Desk]   --> Field inspection, updates state (Under Investigation -> Resolved) --> [PATCH /api/reports/{id}/investigate]\n"
        "                             ↓\n"
        "[Citizen Tracker]--> Public tracking with 4-stage visual milestone stepper and official inspection remarks"
    )
    set_run_font(r_arch, name="Consolas", size=9.5, color=RGBColor(30, 41, 59))

    # Core Data Models Code
    p_code_lbl = doc.add_paragraph()
    p_code_lbl.paragraph_format.space_before = Pt(6)
    p_code_lbl.paragraph_format.space_after = Pt(4)
    r_cl = p_code_lbl.add_run("Listing 4.1: Core Data Models in Models.kt (Kotlin Serialization):")
    set_run_font(r_cl, name="Times New Roman", size=11, bold=True)

    p_code1 = doc.add_paragraph()
    p_code1.paragraph_format.space_after = Pt(8)
    r_c1_code = p_code1.add_run(
        "@Serializable\n"
        "data class TheftReport(\n"
        "    val referenceId: String,\n"
        "    val title: String,\n"
        "    val category: TheftCategory,\n"
        "    val severity: SeverityLevel,\n"
        "    val status: ReportStatus,\n"
        "    val address: String,\n"
        "    val landmark: String,\n"
        "    val gpsCoordinates: String? = null,\n"
        "    val suspectConsumerNumber: String? = null,\n"
        "    val description: String,\n"
        "    val evidenceImageData: String? = null,\n"
        "    val evidenceFileName: String? = null,\n"
        "    val isAnonymous: Boolean = false,\n"
        "    val submittedByUsername: String? = null,\n"
        "    val reporterName: String? = null,\n"
        "    val reporterPhone: String? = null,\n"
        "    val reporterEmail: String? = null,\n"
        "    val assignedOfficer: String? = null,\n"
        "    val assignedOfficerUsername: String? = null,\n"
        "    val inspectionNotes: String? = null,\n"
        "    val createdAt: String,\n"
        "    val updatedAt: String,\n"
        "    val history: List<StatusHistoryEntry> = emptyList()\n"
        ")"
    )
    set_run_font(r_c1_code, name="Consolas", size=9, color=RGBColor(30, 41, 59))

    p_ui_lbl = doc.add_paragraph()
    p_ui_lbl.paragraph_format.space_before = Pt(6)
    p_ui_lbl.paragraph_format.space_after = Pt(4)
    r_ui_lbl = p_ui_lbl.add_run("Implementation Highlights & User Interface Verification:")
    set_run_font(r_ui_lbl, name="Times New Roman", size=11, bold=True)

    p_screens = doc.add_paragraph()
    p_screens.paragraph_format.space_after = Pt(10)
    p_screens.paragraph_format.line_spacing = 1.15
    r_sc = p_screens.add_run(
        "• Screenshot 4.1: Citizen Complaint Portal (index.html)\n"
        "  - Permanent reporter identification section (Full Name, Contact Mobile Number, optional Email).\n"
        "  - Incident taxonomy selection (Direct Hooking, Meter Bypass, Sub-metering, Transformer Tap, Splicing).\n"
        "  - Client-side drag-and-drop evidence image upload with base64 encoding and thumbnail preview.\n\n"
        "• Screenshot 4.2: Administrator Case Management Desk (tab-admin)\n"
        "  - Real-time KPI summary banner (Total Reports, Pending Assignment, Active Investigations, Resolved Cases).\n"
        "  - Dynamic horizontal category distribution bars and severity hazard breakdown.\n"
        "  - Evidence thumbnail rendered directly beside each complaint row in the table.\n"
        "  - Officer Assignment Modal with drop-down vigilance officer roster and instruction input.\n\n"
        "• Screenshot 4.3: Vigilance Officer Investigation Desk (tab-officer)\n"
        "  - Filtered desk displaying complaints assigned to the logged-in officer.\n"
        "  - Full-resolution evidence image lightbox modal with nearest landmark and suspect consumer ID.\n"
        "  - Digital status transition selector with official field inspection remarks submission.\n\n"
        "• Screenshot 4.4: Standalone SQLite Database Inspector (data/view_database.html)\n"
        "  - Interactive table displaying all rows from theft_reports table in powerguard.db.\n"
        "  - Direct image rendering in table cells with click-to-enlarge modal preview."
    )
    set_run_font(r_sc, name="Times New Roman", size=10.5)

    doc.add_page_break()

    # =========================================================================
    # PAGE 7: CHAPTER 5: CONCLUSION & FUTURE SCOPE
    # =========================================================================
    add_page_header(doc)

    p_c5 = doc.add_paragraph()
    p_c5.paragraph_format.space_before = Pt(10)
    p_c5.paragraph_format.space_after = Pt(12)
    r_c5 = p_c5.add_run("CHAPTER 5: CONCLUSION & FUTURE SCOPE")
    set_run_font(r_c5, name="Times New Roman", size=14, bold=True, color=RGBColor(15, 23, 42))

    p_c_lbl = doc.add_paragraph()
    p_c_lbl.paragraph_format.space_after = Pt(8)
    r_c_lbl = p_c_lbl.add_run("⮚ Learnings from Web & Mobile Application Development Project:")
    set_run_font(r_c_lbl, name="Times New Roman", size=12, bold=True)

    conc_p1 = doc.add_paragraph()
    conc_p1.paragraph_format.space_after = Pt(10)
    conc_p1.paragraph_format.line_spacing = 1.15
    r_cp1 = conc_p1.add_run(
        "The conceptualization and implementation of the PowerGuard Electricity Theft Reporting & Vigilance Portal provided comprehensive "
        "practical exposure to modern full-stack software engineering, reactive web design, and asynchronous server architectures. "
        "Working with Kotlin 2.2 and the Ktor Server framework underscored the practical advantages of type-safety, null-safe idioms, "
        "and coroutine-driven non-blocking I/O over traditional heavyweight enterprise frameworks. Establishing a three-tier Role-Based "
        "Access Control (RBAC) model provided deep insights into designing secure multi-stakeholder workflows, ensuring that citizen reporters, "
        "central administrators, and field vigilance officers interact with distinct operational endpoints. Furthermore, designing the dual-persistence "
        "storage strategy—combining SQLite relational integrity with automated JSON mirroring and filesystem evidence image extraction—demonstrated "
        "how to maintain high auditability and human-verifiable data transparency in public utility applications."
    )
    set_run_font(r_cp1, name="Times New Roman", size=11.5)

    conc_p2 = doc.add_paragraph()
    conc_p2.paragraph_format.space_after = Pt(10)
    conc_p2.paragraph_format.line_spacing = 1.15
    r_cp2 = conc_p2.add_run(
        "From an operational standpoint, the project demonstrates how civic engagement and digital oversight can dramatically streamline public "
        "infrastructure security. By eliminating opaque manual complaint books and providing citizens with an instant, verified mechanism to submit "
        "photographic evidence, PowerGuard eliminates false alarms, enforces administrative accountability, and preserves a legal chain of custody. "
        "Vigilance squads can be dispatched systematically based on hazard triage, directly protecting electricity distribution transformers from "
        "overload-induced burnouts, safeguarding public life from hazardous direct hookings, and curbing immense commercial revenue leakage."
    )
    set_run_font(r_cp2, name="Times New Roman", size=11.5)

    conc_p3 = doc.add_paragraph()
    conc_p3.paragraph_format.space_after = Pt(10)
    conc_p3.paragraph_format.line_spacing = 1.15
    r_cp3 = conc_p3.add_run(
        "Future Scope: Building upon this robust architectural foundation, several transformative technological enhancements are envisioned for "
        "future iterations of the platform. First, integrating Edge-AI and Computer Vision models can automate the pre-screening of uploaded evidence "
        "images to immediately detect illegal line tapings, bypassed meter seals, and shunt wires with confidence scoring before officer dispatch. "
        "Second, integrating Advanced Metering Infrastructure (AMI) smart meter telemetry hooks via MQTT/Kafka will enable the system to automatically "
        "correlate citizen complaints with localized transformer distribution load anomalies in real-time. Third, developing dedicated cross-platform "
        "mobile applications (Android/iOS) with offline caching and GPS geofencing will empower field vigilance squads to perform site inspections in remote "
        "rural areas without continuous cellular connectivity, automatically syncing audit data upon network reconnection."
    )
    set_run_font(r_cp3, name="Times New Roman", size=11.5)

    doc.add_page_break()

    # =========================================================================
    # PAGE 8: CHAPTER 6: SUSTAINABLE DEVELOPMENT GOALS (SDG) MAPPING
    # =========================================================================
    add_page_header(doc)

    p_c6 = doc.add_paragraph()
    p_c6.paragraph_format.space_before = Pt(10)
    p_c6.paragraph_format.space_after = Pt(12)
    r_c6 = p_c6.add_run("CHAPTER 6: SUSTAINABLE DEVELOPMENT GOALS (SDG) MAPPING")
    set_run_font(r_c6, name="Times New Roman", size=14, bold=True, color=RGBColor(15, 23, 42))

    p_sdg_lbl = doc.add_paragraph()
    p_sdg_lbl.paragraph_format.space_after = Pt(8)
    r_sdg_lbl = p_sdg_lbl.add_run("⮚ SDG Goals No. along with description:")
    set_run_font(r_sdg_lbl, name="Times New Roman", size=12, bold=True)

    sdg_intro = doc.add_paragraph()
    sdg_intro.paragraph_format.space_after = Pt(8)
    sdg_intro.paragraph_format.line_spacing = 1.15
    r_si = sdg_intro.add_run(
        "The PowerGuard platform directly aligns with and contributes to the United Nations Sustainable Development Goals (SDGs), "
        "addressing clean energy reliability, sustainable urban infrastructure, responsible resource consumption, and institutional transparency:"
    )
    set_run_font(r_si, name="Times New Roman", size=11.5)

    sdgs = [
        ("SDG 7: Affordable and Clean Energy (Target 7.1, 7.b)",
         "Electricity theft destabilizes power grids and results in massive unmetered energy waste, increasing utility generation burdens from fossil fuels. "
         "By curbing illegal taps and non-technical distribution losses, PowerGuard improves grid operational efficiency, stabilizes local electrical supply, "
         "and prevents transformer overloads, thereby ensuring more reliable, affordable, and sustainable electricity access for legitimate consumers."),
        
        ("SDG 9: Industry, Innovation, and Infrastructure (Target 9.1, 9.4)",
         "PowerGuard modernizes traditional, aging power distribution infrastructure through digital innovation. By transitioning utilities from archaic paper-based "
         "complaint books to an automated, asynchronous, cloud-ready RESTful vigilance platform, it upgrades distribution network monitoring and builds resilient "
         "utility infrastructure capable of swift grievance response."),
        
        ("SDG 11: Sustainable Cities and Communities (Target 11.5, 11.b)",
         "Unregulated direct line hooking (kundi) into overhead distribution cables poses critical fire hazards and life-threatening electrocution risks in dense urban "
         "settlements and residential localities. PowerGuard enables prompt reporting, hazard severity triage, and field team dispatch, safeguarding urban neighborhoods "
         "from catastrophic electrical accidents and fires."),
        
        ("SDG 12: Responsible Consumption and Production (Target 12.2)",
         "Unauthorized power consumption in commercial establishments (e.g. banquet halls, welding units, and industrial workshops) leads to unchecked, reckless energy "
         "utilization. Enforcing strict vigilance inspections and digital evidence recording fosters accountability and promotes responsible electrical consumption."),
        
        ("SDG 16: Peace, Justice, and Strong Institutions (Target 16.5, 16.6)",
         "By establishing an immutable digital chain-of-custody with chronological timestamps, assigned officer IDs, and public audit history tracking, PowerGuard "
         "eliminates bureaucratic opacity, prevents bribery, and combats administrative corruption, fostering transparent and accountable public utility governance.")
    ]

    for title, desc in sdgs:
        p_s = doc.add_paragraph()
        p_s.paragraph_format.space_after = Pt(8)
        p_s.paragraph_format.line_spacing = 1.15
        r_st = p_s.add_run(f"• {title}:\n")
        set_run_font(r_st, name="Times New Roman", size=11.5, bold=True, color=RGBColor(2, 132, 199))
        r_sd = p_s.add_run(desc)
        set_run_font(r_sd, name="Times New Roman", size=11)

    doc.add_page_break()

    # =========================================================================
    # PAGE 9: CHAPTER 7: REFERENCES
    # =========================================================================
    add_page_header(doc)

    p_c7 = doc.add_paragraph()
    p_c7.paragraph_format.space_before = Pt(10)
    p_c7.paragraph_format.space_after = Pt(12)
    r_c7 = p_c7.add_run("CHAPTER 7: REFERENCES")
    set_run_font(r_c7, name="Times New Roman", size=14, bold=True, color=RGBColor(15, 23, 42))

    p_ref_note = doc.add_paragraph()
    p_ref_note.paragraph_format.space_after = Pt(12)
    r_rn = p_ref_note.add_run("(Books, websites, research papers, or tutorials referred):")
    set_run_font(r_rn, name="Times New Roman", size=11.5, italic=True)

    references = [
        "1. Central Electricity Authority (CEA), Ministry of Power, Government of India, 'Report on Aggregate Technical and Commercial (AT&C) Losses in Power Distribution Utilities', New Delhi, 2023.",
        "2. P. S. Balamurugan and R. Dhanasekaran, 'Detection of Electricity Theft and Power Quality Monitoring in Smart Grid Using IoT and Machine Learning', IEEE Transactions on Smart Grid, vol. 12, no. 4, pp. 3210-3221, 2021.",
        "3. JetBrains, 'Ktor: Asynchronous Web Framework for Kotlin - Official Architecture & Server Guide', https://ktor.io/docs/server-overview.html, Accessed Oct. 2026.",
        "4. Kotlin Foundation, 'Kotlin Language Specification and Coroutines Guide (v2.2)', https://kotlinlang.org/docs/reference/, Accessed Oct. 2026.",
        "5. D. R. Hipp et al., 'SQLite Relational Database Engine Architecture & ACID Compliance Documentation', https://www.sqlite.org/docs.html, 2024.",
        "6. United Nations, 'Transforming Our World: The 2030 Agenda for Sustainable Development - Sustainable Development Goals (SDG 7, 9, 11, 12, 16)', Department of Economic and Social Affairs, https://sdgs.un.org/goals, 2015.",
        "7. M. H. Rashid, 'Power Electronics Handbook: Devices, Circuits, and Applications', 4th ed., Butterworth-Heinemann / Elsevier, Oxford, UK, 2018.",
        "8. World Bank Energy & Extractives Global Practice, 'Reducing Technical and Non-Technical Electricity Losses in Developing Countries', Energy Sector Management Assistance Program (ESMAP) Technical Report, Washington, D.C., 2022.",
        "9. Mozilla Developer Network (MDN), 'Web APIs, HTML5 File API & Responsive CSS Custom Properties Guide', https://developer.mozilla.org/en-US/docs/Web, 2026.",
        "10. Pratik Mali, 'PowerGuard: Electricity Theft Reporting & Vigilance Portal - Open Source Repository', GitHub: https://github.com/pratik0437/electricity-theft-reporting, 2026."
    ]

    for ref in references:
        p_r = doc.add_paragraph()
        p_r.paragraph_format.space_after = Pt(8)
        p_r.paragraph_format.line_spacing = 1.15
        r_ref = p_r.add_run(ref)
        set_run_font(r_ref, name="Times New Roman", size=11)

    output_path = "PowerGuard_Project_Report.docx"
    doc.save(output_path)
    print(f"Report document generated successfully: {output_path}")

if __name__ == "__main__":
    create_report()
