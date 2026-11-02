import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

def build_24page_report():
    doc = Document()

    # Configure 1-inch margins
    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)

        # Running Footer on every page
        footer = s.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("Department of Computer Science & Engineering-(AI&ML) | APSIT")
        frun.font.name = "Times New Roman"
        frun.font.size = Pt(9.5)
        frun.font.bold = True
        frun.font.color.rgb = RGBColor(100, 116, 139)

    def set_font(run, name="Times New Roman", size=12, bold=False, italic=False, color=None):
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
        p.paragraph_format.space_after = Pt(14)
        r = p.add_run("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING\n(ARTIFICIAL INTELLIGENCE AND MACHINE LEARNING)")
        set_font(r, size=11, bold=True, color=RGBColor(30, 41, 59))

    # =========================================================================
    # PAGE 1: COVER PAGE
    # =========================================================================
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(10)
    p_inst.paragraph_format.space_after = Pt(2)
    r_tr = p_inst.add_run("Parshvanath Charitable Trust's\n")
    set_font(r_tr, size=11, italic=True)
    r_col = p_inst.add_run("A. P. SHAH INSTITUTE OF TECHNOLOGY\n")
    set_font(r_col, size=16, bold=True, color=RGBColor(15, 23, 42))
    r_ap = p_inst.add_run("(Approved by AICTE New Delhi & Govt. of Maharashtra, Affiliated to University of Mumbai)\n(Religious Jain Minority)")
    set_font(r_ap, size=9.5, italic=True, color=RGBColor(71, 85, 105))

    p_d = doc.add_paragraph()
    p_d.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_d.paragraph_format.space_before = Pt(18)
    p_d.paragraph_format.space_after = Pt(28)
    r_d = p_d.add_run("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING\n(ARTIFICIAL INTELLIGENCE AND MACHINE LEARNING)")
    set_font(r_d, size=12, bold=True, color=RGBColor(30, 41, 59))

    p_t = doc.add_paragraph()
    p_t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t.paragraph_format.space_before = Pt(20)
    p_t.paragraph_format.space_after = Pt(36)
    r_t = p_t.add_run("POWERGUARD – ELECTRICITY THEFT REPORTING &\nVIGILANCE PORTAL")
    set_font(r_t, size=17, bold=True, color=RGBColor(15, 23, 42))

    p_rep = doc.add_paragraph()
    p_rep.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_rep.paragraph_format.space_before = Pt(20)
    p_rep.paragraph_format.space_after = Pt(8)
    r_rep = p_rep.add_run("REPORT")
    set_font(r_rep, size=14, bold=True, color=RGBColor(15, 23, 42))

    p_ay = doc.add_paragraph()
    p_ay.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ay.paragraph_format.space_before = Pt(4)
    p_ay.paragraph_format.space_after = Pt(28)
    r_ay = p_ay.add_run("Academic Year: 2026-27")
    set_font(r_ay, size=12, bold=True)

    p_top = doc.add_paragraph()
    p_top.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_top.paragraph_format.space_before = Pt(14)
    p_top.paragraph_format.space_after = Pt(4)
    r_top = p_top.add_run("Topic:\n")
    set_font(r_top, size=13, bold=True)
    r_name = p_top.add_run("Pratik Mali - 22104037")
    set_font(r_name, size=12)

    p_g = doc.add_paragraph()
    p_g.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_g.paragraph_format.space_before = Pt(40)
    p_g.paragraph_format.space_after = Pt(10)
    r_gu = p_g.add_run("Under the guidance of\n")
    set_font(r_gu, size=11, bold=True)
    r_gname = p_g.add_run("Prof. Vijesh Mundokalam")
    set_font(r_gname, size=13, bold=True, color=RGBColor(15, 23, 42))

    doc.add_page_break()

    # =========================================================================
    # PAGE 2: TABLE OF CONTENTS
    # =========================================================================
    add_page_header(doc)

    p_tc = doc.add_paragraph()
    p_tc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tc.paragraph_format.space_before = Pt(10)
    p_tc.paragraph_format.space_after = Pt(20)
    r_tc = p_tc.add_run("TABLE OF CONTENTS")
    set_font(r_tc, size=14, bold=True, color=RGBColor(15, 23, 42))

    p_c_lbl = doc.add_paragraph()
    p_c_lbl.paragraph_format.space_after = Pt(8)
    r_clbl = p_c_lbl.add_run("Contents")
    set_font(r_clbl, size=13, bold=True)

    toc_lines = [
        ("REPORT", "1", False, 0),
        ("TABLE OF CONTENTS", "2", False, 0),
        ("CHAPTER 1: INTRODUCTION", "3", False, 0),
        ("CHAPTER 2: PROBLEM STATEMENT", "4", False, 0),
        ("CHAPTER 3: TECHNOLOGY & TOOLS", "6", False, 0),
        ("3.1 Tools and Technologies Used", "6", False, 1),
        ("3.2 Methodology", "8", False, 1),
        ("3.3 Development Architecture", "9", False, 1),
        ("CHAPTER 4: IMPLEMENTATION", "10", False, 0),
        ("4.1 Implementation and Source Code", "10", False, 1),
        ("4.2 Application Workflow", "14", False, 1),
        ("4.3 Screenshots of Implementation", "15", False, 1),
        ("4.4 Important Implementation Details", "19", False, 1),
        ("CHAPTER 5: CONCLUSION & FUTURE SCOPE", "20", False, 0),
        ("5.1 Learnings from Web & Mobile Application Development Project", "20", False, 1),
        ("5.2 Future Scope", "20", False, 1),
        ("CHAPTER 6: SUSTAINABLE DEVELOPMENT GOALS (SDG) MAPPING", "22", False, 0),
        ("6.1 SDG Goals and Their Description", "22", False, 1),
        ("CHAPTER 7: REFERENCES", "24", False, 0),
        ("7.1 References", "24", False, 1)
    ]

    for title, pg, is_bold, indent_level in toc_lines:
        p_line = doc.add_paragraph()
        p_line.paragraph_format.space_after = Pt(4)
        p_line.paragraph_format.line_spacing = 1.15
        
        indent = "    " * indent_level
        left_text = f"{indent}{title} "
        target_len = 100
        dots = "." * max(4, target_len - len(left_text) - len(pg))
        
        r1 = p_line.add_run(left_text)
        set_font(r1, size=10.5, bold=(indent_level == 0))
        r2 = p_line.add_run(dots)
        set_font(r2, size=10.5, color=RGBColor(148, 163, 184))
        r3 = p_line.add_run(f" {pg}")
        set_font(r3, size=10.5, bold=(indent_level == 0))

    doc.add_page_break()

    # =========================================================================
    # PAGE 3: CHAPTER 1: INTRODUCTION
    # =========================================================================
    add_page_header(doc)

    p_ch1 = doc.add_paragraph()
    p_ch1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ch1.paragraph_format.space_before = Pt(10)
    p_ch1.paragraph_format.space_after = Pt(20)
    r_ch1 = p_ch1.add_run("CHAPTER 1: INTRODUCTION")
    set_font(r_ch1, size=14, bold=True, color=RGBColor(15, 23, 42))

    p_in_lbl = doc.add_paragraph()
    p_in_lbl.paragraph_format.space_after = Pt(10)
    r_in = p_in_lbl.add_run("⮚ Introduction:")
    set_font(r_in, size=12, bold=True)

    paras_c1 = [
        "In today's digital world, web and mobile platforms have become an important part of public utility vigilance and infrastructure management. They allow citizens and administrators to coordinate essential civic activities conveniently through responsive web interfaces without relying on slow manual paperwork. Utility grievance and vigilance applications provide critical features such as reporting violations, uploading evidence, verifying landmarks, and tracking investigation status.",
        "POWERGUARD is an electricity theft reporting and vigilance management web application developed using Kotlin and Ktor as part of the Web and Mobile Application Development (WMD) subject. The main objective of this project is to develop a user-friendly and interactive vigilance application that demonstrates the essential functionalities of a modern digital utility surveillance and enforcement system.",
        "The application provides user registration and role-based login facilities, allowing users to access dedicated portals based on their designated responsibilities (Normal Citizen, Vigilance Officer, and Central Administrator). After logging in, citizens can submit theft complaints with title, theft category, severity level, premises address, nearest electric pole ID, and photographic evidence. Administrators review incoming reports, assess hazard priorities, and assign cases to field vigilance officers. In turn, officers inspect field sites, review evidence, and record official inspection findings.",
        "The application uses modern HTML5, CSS3 custom properties, and responsive layout styling to create an attractive and responsive user interface. SQLite local persistence paired with automated JSON mirroring is used for local data storage, allowing complaint records, user accounts, and investigation history to remain permanently available even after restarting the application server.",
        "POWERGUARD demonstrates how modern web application development technologies can be used to create an interactive utility management application with multiple features, secure role-based access, and persistent local data storage."
    ]

    for para in paras_c1:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(10)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(para)
        set_font(r, size=11.5)

    doc.add_page_break()

    # =========================================================================
    # PAGE 4: CHAPTER 2: PROBLEM STATEMENT (Part 1)
    # =========================================================================
    add_page_header(doc)

    p_ch2 = doc.add_paragraph()
    p_ch2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ch2.paragraph_format.space_before = Pt(10)
    p_ch2.paragraph_format.space_after = Pt(20)
    r_ch2 = p_ch2.add_run("CHAPTER 2: PROBLEM STATEMENT")
    set_font(r_ch2, size=14, bold=True, color=RGBColor(15, 23, 42))

    p_ps_lbl = doc.add_paragraph()
    p_ps_lbl.paragraph_format.space_after = Pt(10)
    r_ps = p_ps_lbl.add_run("⮚ Problem Statement:")
    set_font(r_ps, size=12, bold=True)

    ps_intro = [
        "Traditional electricity theft reporting activities often require consumers to visit physical utility offices or use generic call-center helplines that lack photo verification. This consumes time, delays enforcement, and makes basic utility grievance management ineffective and opaque.",
        "The main problem addressed by this project is the need for a simple and user-friendly web application that brings citizen reporting, administrative case triage, and field vigilance investigation together in one platform.",
        "The objective of the POWERGUARD application is to develop a role-based vigilance management prototype that allows citizens, administrators, and field officers to manage electricity theft cases through an intuitive web interface.",
        "The application aims to solve this problem by providing the following functionalities:"
    ]

    for text in ps_intro:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(text)
        set_font(r, size=11.5)

    fn_p4 = [
        ("1. User Registration and Role Authentication: ", "Allows new citizens to create an account and existing citizens, officers, and administrators to log in securely using their credentials."),
        ("2. Citizen Reporting Desk: ", "Enables named citizens to submit theft reports with incident summary, theft category, premises address, and nearest pole number."),
        ("3. Photographic Evidence Upload: ", "Allows users to upload site evidence photos (such as direct hooking wires or bypassed meter seals) that are stored and displayed directly beside complaints."),
        ("4. Administrator Oversight Dashboard: ", "Displays real-time KPIs (total registered reports, unassigned cases, active investigations, resolved cases) and category breakdowns."),
        ("5. Officer Case Assignment: ", "Enables the Central Administrator to review citizen reports and assign each case to a designated Field Vigilance Officer with specific inspection instructions."),
        ("6. Vigilance Officer Investigation Desk: ", "Provides a dedicated desk for assigned officers to inspect evidence photos, record site findings, and transition complaint status.")
    ]

    for bold_prefix, desc in fn_p4:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15
        r_b = p.add_run(bold_prefix)
        set_font(r_b, size=11, bold=True)
        r_d = p.add_run(desc)
        set_font(r_d, size=11)

    doc.add_page_break()

    # =========================================================================
    # PAGE 5: CHAPTER 2: PROBLEM STATEMENT (Part 2)
    # =========================================================================
    add_page_header(doc)

    fn_p5 = [
        ("7. Multi-Stage Progress Stepper: ", "Maintains an end-to-end chronological timeline tracking status progression from Citizen Reported → Assigned to Officer → Field Inspection → Action Completed."),
        ("8. Standardized Theft Taxonomy: ", "Categorizes power theft into Direct Line Hooking (Kundi), Meter Tampering / Shunt Bypass, Commercial Sub-Metering, Transformer Taps, and Splicing."),
        ("9. Dual-Persistence & Standalone Database Visual Inspector: ", "Stores data in SQLite (powerguard.db), mirrors records in JSON (reports_mirror.json), and provides an interactive standalone visual inspector with photo lightbox."),
        ("10. Public Tracking & Auditability: ", "Allows citizens to track their submitted reports using a unique Reference ID (e.g. PG-2026-1084) and view official inspection findings.")
    ]

    for bold_prefix, desc in fn_p5:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(12)
        p.paragraph_format.line_spacing = 1.15
        r_b = p.add_run(bold_prefix)
        set_font(r_b, size=11.5, bold=True)
        r_d = p.add_run(desc)
        set_font(r_d, size=11.5)

    p_sum = doc.add_paragraph()
    p_sum.paragraph_format.space_before = Pt(20)
    p_sum.paragraph_format.space_after = Pt(10)
    p_sum.paragraph_format.line_spacing = 1.15
    r_sum = p_sum.add_run(
        "By integrating these ten core functionalities into a unified, secure platform, POWERGUARD transforms traditional, fragmented power distribution vigilance into a streamlined, accountable, and transparent digital process."
    )
    set_font(r_sum, size=11.5, italic=True)

    doc.add_page_break()

    # =========================================================================
    # PAGE 6: CHAPTER 3: TECHNOLOGY & TOOLS (Part 1)
    # =========================================================================
    add_page_header(doc)

    p_ch3 = doc.add_paragraph()
    p_ch3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ch3.paragraph_format.space_before = Pt(10)
    p_ch3.paragraph_format.space_after = Pt(20)
    r_ch3 = p_ch3.add_run("CHAPTER 3: TECHNOLOGY & TOOLS")
    set_font(r_ch3, size=14, bold=True, color=RGBColor(15, 23, 42))

    p_t_lbl = doc.add_paragraph()
    p_t_lbl.paragraph_format.space_after = Pt(10)
    r_tlbl = p_t_lbl.add_run("⮚ Tools & Methodologies:\n3.1 Tools and Technologies Used")
    set_font(r_tlbl, size=12, bold=True)

    p_t_intro = doc.add_paragraph()
    p_t_intro.paragraph_format.space_after = Pt(10)
    p_t_intro.paragraph_format.line_spacing = 1.15
    r_tintro = p_t_intro.add_run(
        "The POWERGUARD electricity theft reporting and vigilance application is developed using Kotlin and Ktor Server. Various tools, frameworks, and libraries are used to create the user interface, manage application functionality, and store persistent vigilance data."
    )
    set_font(r_tintro, size=11.5)

    tools_p6 = [
        ("1. Kotlin Programming Language (v2.2.20)",
         "Kotlin is a modern, statically typed programming language developed by JetBrains. It is known for its concise syntax, null safety, and full interoperability with Java.\nIn this project, Kotlin is used to develop the complete backend server logic, including data models, repository operations, asynchronous coroutine management, authentication verification, and RESTful routing handlers."),
        
        ("2. Ktor Server Framework (Netty Engine)",
         "Ktor is an asynchronous web framework built from the ground up by JetBrains using Kotlin and coroutines. It runs on the high-throughput Netty asynchronous server engine.\nIn POWERGUARD, Ktor provides non-blocking HTTP request processing, static content serving, ContentNegotiation routing, CORS configuration, and RESTful API endpoints with minimal memory overhead."),
        
        ("3. Visual Studio Code & IntelliJ IDEA",
         "Visual Studio Code and IntelliJ IDEA were used as the code editors for developing, editing, and managing the project source code. Extensions for Kotlin, Gradle, SQLite, and HTML/CSS/JS provided seamless syntax highlighting, debugging, and terminal execution.")
    ]

    for title, desc in tools_p6:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.line_spacing = 1.15
        r_t = p.add_run(title + "\n")
        set_font(r_t, size=11.5, bold=True)
        r_d = p.add_run(desc)
        set_font(r_d, size=11)

    doc.add_page_break()

    # =========================================================================
    # PAGE 7: CHAPTER 3: TECHNOLOGY & TOOLS (Part 2)
    # =========================================================================
    add_page_header(doc)

    tools_p7 = [
        ("4. SQLite Relational Database Engine",
         "SQLite is a self-contained, serverless, zero-configuration relational database engine embedded directly into the application.\nIn this project, SQLite (data/powerguard.db) is used to store:\n"
         "• Registered citizen, officer, and administrator user credentials and contact details.\n"
         "• Theft reports with Reference IDs, categories, addresses, landmarks, and evidence photos.\n"
         "• Officer assignments and administrative inspection directives.\n"
         "• Chronological status history logs with timestamps and inspection notes."),
        
        ("5. kotlinx.serialization & REST API Architecture",
         "The kotlinx.serialization library is used for serializing and deserializing data between Kotlin objects and JSON strings. It enables lightning-fast JSON encoding and decoding across all REST endpoints."),
        
        ("6. Responsive HTML5, Modern CSS3, & Vanilla JavaScript",
         "The frontend interface is engineered using semantic HTML5, CSS3 custom properties (dark-mode theme palette), and reactive vanilla JavaScript. It features an interactive single-page layout with modal dialogs and evidence photo preview."),
        
        ("7. Gradle Build Automation (Gradle 9.1 Wrapper)",
         "Gradle Wrapper is used for automated compilation, dependency resolution, and execution of the Ktor application.")
    ]

    for title, desc in tools_p7:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(10)
        p.paragraph_format.line_spacing = 1.15
        r_t = p.add_run(title + "\n")
        set_font(r_t, size=11.5, bold=True)
        r_d = p.add_run(desc)
        set_font(r_d, size=11)

    doc.add_page_break()

    # =========================================================================
    # PAGE 8: CHAPTER 3: TECHNOLOGY & TOOLS (Part 3)
    # =========================================================================
    add_page_header(doc)

    p_lib_lbl = doc.add_paragraph()
    p_lib_lbl.paragraph_format.space_after = Pt(6)
    r_lib = p_lib_lbl.add_run("Built-in Standard Libraries Used:\n")
    set_font(r_lib, size=11.5, bold=True)

    libs = [
        ("• java.sql & JDBC SQLite: ", "Used for establishing database connections, executing prepared statements, and handling ACID transactions."),
        ("• java.time.LocalDateTime: ", "Used for generating standardized chronological timestamps (yyyy-MM-dd HH:mm) for audit trails."),
        ("• java.util.Base64: ", "Used for decoding evidence image strings and extracting physical image files into the filesystem.")
    ]
    for b_txt, r_txt in libs:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        r1 = p.add_run(b_txt)
        set_font(r1, size=11, bold=True)
        r2 = p.add_run(r_txt)
        set_font(r2, size=11)

    p_m_lbl = doc.add_paragraph()
    p_m_lbl.paragraph_format.space_before = Pt(10)
    p_m_lbl.paragraph_format.space_after = Pt(6)
    r_mlbl = p_m_lbl.add_run("3.2 Methodology")
    set_font(r_mlbl, size=12, bold=True)

    p_m_intro = doc.add_paragraph()
    p_m_intro.paragraph_format.space_after = Pt(6)
    p_m_intro.paragraph_format.line_spacing = 1.15
    r_mintro = p_m_intro.add_run(
        "The application follows a modular and component-based development approach. The development process consists of the following stages:"
    )
    set_font(r_mintro, size=11.5)

    stages = [
        "1. Requirement Analysis: Identifying essential functionalities required in a power theft vigilance portal (reporting, triage, assignment, investigation).",
        "2. UI Design: Creating responsive single-page interfaces for citizen complaint filing, admin case assignment, officer investigation, and public tracking.",
        "3. Application Development: Implementing backend routing, authentication, and report management using Kotlin and Ktor.",
        "4. Role-Based Access Control: Restricting portal viewports so Citizens only report, Admins assign, and Officers investigate.",
        "5. Data Storage: Implementing SQLite relational persistence and automated JSON/image filesystem mirroring.",
        "6. Integration: Connecting frontend forms with Ktor asynchronous REST APIs using fetch and JSON serialization.",
        "7. Testing: Checking system operations such as citizen registration, report submission, image decoding, admin assignment, and officer status updates."
    ]

    for st in stages:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(st)
        set_font(r, size=10.5)

    doc.add_page_break()

    # =========================================================================
    # PAGE 9: CHAPTER 3: TECHNOLOGY & TOOLS (Part 4)
    # =========================================================================
    add_page_header(doc)

    p_arch_lbl = doc.add_paragraph()
    p_arch_lbl.paragraph_format.space_before = Pt(10)
    p_arch_lbl.paragraph_format.space_after = Pt(12)
    r_albl = p_arch_lbl.add_run("3.3 Development Architecture")
    set_font(r_albl, size=12, bold=True)

    arch_paras = [
        "The application follows a three-tier layered architecture with a central state management model. The architecture cleanly separates user presentation, business logic processing, and persistent data storage.",
        "The Presentation Layer consists of a responsive single-page web client engineered using HTML5, modern CSS3 custom properties, and reactive JavaScript. It provides role-specific views for Citizens, Central Administrators, and Field Vigilance Officers, dynamically updating viewports based on session role authentication.",
        "The Application & Service Layer is powered by Kotlin and Ktor running on the asynchronous Netty engine. Ktor route handlers process incoming HTTP requests, enforce Role-Based Access Control, validate input parameters, and invoke repository methods. Coroutines ensure non-blocking concurrent request handling.",
        "The Persistence & Storage Layer implements a dual-persistence strategy. An ACID-compliant SQLite relational database (data/powerguard.db) provides reliable transactional storage. Concurrently, an automated JSON mirror (data/reports_mirror.json) and an evidence image extractor (data/evidence_images/) maintain human-verifiable data transparency and local file inspection.",
        "This architectural approach makes the application highly reliable, easy to organize, maintain, audit, and extend with future microservices."
    ]

    for ap in arch_paras:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(12)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(ap)
        set_font(r, size=11.5)

    doc.add_page_break()

    # =========================================================================
    # PAGE 10: CHAPTER 4: IMPLEMENTATION (Part 1)
    # =========================================================================
    add_page_header(doc)

    p_ch4 = doc.add_paragraph()
    p_ch4.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ch4.paragraph_format.space_before = Pt(10)
    p_ch4.paragraph_format.space_after = Pt(20)
    r_ch4 = p_ch4.add_run("CHAPTER 4: IMPLEMENTATION")
    set_font(r_ch4, size=14, bold=True, color=RGBColor(15, 23, 42))

    p_sc_lbl = doc.add_paragraph()
    p_sc_lbl.paragraph_format.space_after = Pt(10)
    r_sclbl = p_sc_lbl.add_run("⮚ Implementation and source code\n4.1 Implementation and Source Code")
    set_font(r_sclbl, size=12, bold=True)

    p_sc_intro = doc.add_paragraph()
    p_sc_intro.paragraph_format.space_after = Pt(10)
    p_sc_intro.paragraph_format.line_spacing = 1.15
    r_scintro = p_sc_intro.add_run(
        "The POWERGUARD electricity theft reporting and vigilance application is implemented using Kotlin and Ktor. The application is divided into distinct modular components, where each module performs a specific operational task.\n"
        "The main application manages authentication, report ingestion, officer assignments, status transitions, image decoding, and data persistence."
    )
    set_font(r_scintro, size=11.5)

    modules_p10 = [
        ("4.1.1 Application Initialization",
         "The application starts by initializing the Ktor embedded Netty server in Application.kt. It installs ContentNegotiation for JSON serialization, configures CORS policies, registers API routes (/api/auth, /api/reports, /api/officers, /api/stats), and serves static web assets (index.html, app.js, styles.css).\n"
         "The main() function starts the server on port 8080 and initializes the ReportRepository instance."),
        
        ("4.1.2 User Registration and Login Module",
         "This module allows users to register citizen accounts by entering their full name, mobile number, email, and password. Existing users (Citizens, Officers, Admins) log in by selecting their role tab.\n"
         "The backend verifies credentials against the SQLite users table, checks role permissions, and issues an authenticated session token. Input validation ensures that mandatory contact numbers and credentials are provided.")
    ]

    for title, desc in modules_p10:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(10)
        p.paragraph_format.line_spacing = 1.15
        r_t = p.add_run(title + "\n")
        set_font(r_t, size=11.5, bold=True)
        r_d = p.add_run(desc)
        set_font(r_d, size=11)

    doc.add_page_break()

    # =========================================================================
    # PAGE 11: CHAPTER 4: IMPLEMENTATION (Part 2)
    # =========================================================================
    add_page_header(doc)

    p_post_auth = doc.add_paragraph()
    p_post_auth.paragraph_format.space_after = Pt(8)
    p_post_auth.paragraph_format.line_spacing = 1.15
    r_pa = p_post_auth.add_run(
        "After successful authentication, the user is redirected to their designated portal view (Citizen Reporting, Officer Desk, or Admin Oversight).\n\n"
        "Features of Authentication:\n"
        "• Role selection tabs (Citizen, Vigilance Officer, Administrator).\n"
        "• Citizen registration with full name, contact mobile, and optional email.\n"
        "• Automatic population of reporter details from citizen profile into complaint forms.\n"
        "• Role-Based Access Control preventing unauthorized role viewports.\n"
        "• Error messages for invalid credentials and session sign-out functionality."
    )
    set_font(r_pa, size=11)

    modules_p11 = [
        ("4.1.3 Citizen Complaint Submission Module",
         "This module allows logged-in citizens to submit electricity theft complaints. The form captures incident headline, theft category, hazard severity, premises street address, nearest electric pole ID / landmark, suspect consumer number, and description.\n"
         "The client-side FileReader encodes uploaded evidence photos into Base64 format and submits the payload via POST /api/reports. Form reset automatically re-populates the citizen's verified contact credentials."),
        
        ("4.1.4 Unique Reference ID Generation",
         "When a report is received, the backend automatically generates a unique tracking Reference ID with the prefix 'PG-2026-' followed by four randomly generated digits (e.g. PG-2026-1084).\n"
         "The generator checks against existing database records to prevent collisions, ensuring every complaint has a distinct, permanent tracking code.")
    ]

    for title, desc in modules_p11:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(10)
        p.paragraph_format.line_spacing = 1.15
        r_t = p.add_run(title + "\n")
        set_font(r_t, size=11.5, bold=True)
        r_d = p.add_run(desc)
        set_font(r_d, size=11)

    doc.add_page_break()

    # =========================================================================
    # PAGE 12: CHAPTER 4: IMPLEMENTATION (Part 3)
    # =========================================================================
    add_page_header(doc)

    modules_p12 = [
        ("4.1.5 Central Administrator Assignment Module",
         "This module enables the Administrator to manage the lifecycle of incoming reports. The Admin Review Table displays all registered complaints with severity badges, category labels, evidence thumbnails, and current statuses.\n"
         "The administrator selects an unassigned complaint, opens the assignment modal, and selects a designated Field Vigilance Officer from the active officer roster (e.g. Er. Vikramaditya Deshmukh). The administrator enters specific inspection instructions and submits the assignment via PATCH /api/reports/{refId}/assign.\n"
         "The report status transitions to 'UNDER_INVESTIGATION' and an initial assignment record is appended to the audit history."),
        
        ("4.1.6 Field Vigilance Officer Investigation Module",
         "The officer investigation module provides a specialized desk for vigilance officers to manage cases assigned to them.\n"
         "Officers view premises address, landmark, nearest electric pole ID, and inspect full-resolution evidence photos. The officer updates the investigation status using the transition selector:\n"
         "• UNDER_INVESTIGATION: Initial case verification and site visit planning.\n"
         "• TEAM_DISPATCHED: Field inspection squad dispatched to premises.\n"
         "• RESOLVED_CONFIRMED: Theft confirmed on site, illegal tapping seized, penalty served.\n"
         "• DISMISSED: Site inspected; no unauthorized tapping or meter bypass detected.\n"
         "Submitting findings via PATCH /api/reports/{refId}/investigate updates the database and logs official remarks.")
    ]

    for title, desc in modules_p12:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(12)
        p.paragraph_format.line_spacing = 1.15
        r_t = p.add_run(title + "\n")
        set_font(r_t, size=11.5, bold=True)
        r_d = p.add_run(desc)
        set_font(r_d, size=11)

    doc.add_page_break()

    # =========================================================================
    # PAGE 13: CHAPTER 4: IMPLEMENTATION (Part 4)
    # =========================================================================
    add_page_header(doc)

    modules_p13 = [
        ("4.1.7 Evidence Photo Processing & Extraction Module",
         "To ensure seamless auditing inside code editors and external viewers, the repository implements an automatic image extraction pipeline in saveEvidenceImageFile().\n"
         "Whenever a report with Base64 image data is created or updated, the backend decodes the Base64 byte array and saves a clean image file directly into the data/evidence_images/ folder with the format [RefID]_[Filename].png/jpg.\n"
         "This allows developers and auditors in VS Code to click on evidence images directly in the file explorer and preview photos instantly with full zoom."),
        
        ("4.1.8 Audit History Timeline Module",
         "The audit history module maintains an immutable chronological record of every status change and inspection finding.\n"
         "Each history entry (StatusHistoryEntry) contains:\n"
         "• Timestamp: Exact date and time (yyyy-MM-dd HH:mm).\n"
         "• Status: Transitioned report state.\n"
         "• Updated By: Full name and role of the acting citizen, admin, or officer.\n"
         "• Remarks: Official field notes, dispatch instructions, or penalty remarks.\n"
         "The history array is serialized into JSON and stored in the SQLite history_json column, ensuring a complete legal chain of custody.")
    ]

    for title, desc in modules_p13:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(12)
        p.paragraph_format.line_spacing = 1.15
        r_t = p.add_run(title + "\n")
        set_font(r_t, size=11.5, bold=True)
        r_d = p.add_run(desc)
        set_font(r_d, size=11)

    doc.add_page_break()

    # =========================================================================
    # PAGE 14: CHAPTER 4: IMPLEMENTATION (Part 5)
    # =========================================================================
    add_page_header(doc)

    modules_p14 = [
        ("4.1.9 Multi-Stage Status Stepper Module",
         "The application provides a 4-stage visual milestone stepper in the tracking view (GET /api/reports/track/{refId}):\n"
         "1. Citizen Reported (Step 1) → 2. Assigned to Officer (Step 2) → 3. Field Inspection (Step 3) → 4. Action Completed / Dismissed (Step 4).\n"
         "Completed steps are highlighted with green checkmarks, active steps with glowing amber borders, and pending steps in muted slate, giving citizens intuitive visual clarity."),
        
        ("4.1.10 SQLite Dual-Persistence & Visual Inspector",
         "The repository synchronizes SQLite transactions with an automated JSON mirror (reports_mirror.json) and maintains a standalone visual inspector (data/view_database.html).\n"
         "This allows inspecting database rows and photos directly in any browser without needing command-line SQL tools.")
    ]

    for title, desc in modules_p14:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.line_spacing = 1.15
        r_t = p.add_run(title + "\n")
        set_font(r_t, size=11.5, bold=True)
        r_d = p.add_run(desc)
        set_font(r_d, size=11)

    p_wf_lbl = doc.add_paragraph()
    p_wf_lbl.paragraph_format.space_before = Pt(8)
    p_wf_lbl.paragraph_format.space_after = Pt(6)
    r_wflbl = p_wf_lbl.add_run("4.2 Application Workflow\nThe overall workflow of the POWERGUARD application is as follows:")
    set_font(r_wflbl, size=11.5, bold=True)

    wf_steps_p14 = [
        "1. The user launches the application at http://localhost:8080.",
        "2. The server initializes SQLite tables and loads active vigilance officer rosters.",
        "3. The citizen registers or logs in, filling in verified contact credentials."
    ]
    for s in wf_steps_p14:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(s)
        set_font(r, size=11)

    doc.add_page_break()

    # =========================================================================
    # PAGE 15: CHAPTER 4: IMPLEMENTATION (Part 6) & Figure 4.1
    # =========================================================================
    add_page_header(doc)

    wf_steps_p15 = [
        "4. The citizen submits a theft complaint with category, address, pole ID, and photo evidence.",
        "5. The server creates a unique Reference ID (e.g. PG-2026-1084) and stores records in SQLite.",
        "6. The Central Administrator reviews incoming complaints and assigns each case to a Vigilance Officer.",
        "7. The designated Vigilance Officer accesses their desk, reviews photo evidence, and inspects the site.",
        "8. The officer updates the investigation status (Confirmed/Dismissed) and logs legal seizure notes.",
        "9. The citizen tracks live milestone progress and views official inspection remarks."
    ]
    for s in wf_steps_p15:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(s)
        set_font(r, size=10.5)

    p_scr_lbl = doc.add_paragraph()
    p_scr_lbl.paragraph_format.space_before = Pt(10)
    p_scr_lbl.paragraph_format.space_after = Pt(8)
    r_scrlbl = p_scr_lbl.add_run("4.3 Screenshots of Implementation\nFigure 4.1: Portal Login & Role Selection Screen")
    set_font(r_scrlbl, size=11.5, bold=True)

    # Insert Figure 4.1 Screenshot
    fig1_path = "data/report_screenshots/fig1_login.png"
    if os.path.exists(fig1_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_after = Pt(10)
        doc.add_picture(fig1_path, width=Inches(5.6))

    doc.add_page_break()

    # =========================================================================
    # PAGE 16: Figure 4.2 & Figure 4.3
    # =========================================================================
    add_page_header(doc)

    p_f2 = doc.add_paragraph()
    p_f2.paragraph_format.space_before = Pt(6)
    p_f2.paragraph_format.space_after = Pt(6)
    r_f2 = p_f2.add_run("Figure 4.2: Citizen Registration Screen")
    set_font(r_f2, size=11.5, bold=True)

    fig2_path = "data/report_screenshots/fig2_register.png"
    if os.path.exists(fig2_path):
        doc.add_picture(fig2_path, width=Inches(5.4))

    p_f3 = doc.add_paragraph()
    p_f3.paragraph_format.space_before = Pt(10)
    p_f3.paragraph_format.space_after = Pt(6)
    r_f3 = p_f3.add_run("Figure 4.3: Citizen Theft Reporting Dashboard")
    set_font(r_f3, size=11.5, bold=True)

    fig3_path = "data/report_screenshots/fig3_citizen.png"
    if os.path.exists(fig3_path):
        doc.add_picture(fig3_path, width=Inches(5.4))

    doc.add_page_break()

    # =========================================================================
    # PAGE 17: Figure 4.4
    # =========================================================================
    add_page_header(doc)

    p_f4 = doc.add_paragraph()
    p_f4.paragraph_format.space_before = Pt(10)
    p_f4.paragraph_format.space_after = Pt(10)
    r_f4 = p_f4.add_run("Figure 4.4: Central Administrator Case Oversight & KPI Desk")
    set_font(r_f4, size=12, bold=True)

    fig4_path = "data/report_screenshots/fig4_admin.png"
    if os.path.exists(fig4_path):
        doc.add_picture(fig4_path, width=Inches(6.0))

    doc.add_page_break()

    # =========================================================================
    # PAGE 18: Figure 4.5 & Figure 4.6
    # =========================================================================
    add_page_header(doc)

    p_f5 = doc.add_paragraph()
    p_f5.paragraph_format.space_before = Pt(6)
    p_f5.paragraph_format.space_after = Pt(6)
    r_f5 = p_f5.add_run("Figure 4.5: Vigilance Officer Assignment & Inspection Modal")
    set_font(r_f5, size=11.5, bold=True)

    fig5_path = "data/report_screenshots/fig5_officer.png"
    if os.path.exists(fig5_path):
        doc.add_picture(fig5_path, width=Inches(5.4))

    p_f6 = doc.add_paragraph()
    p_f6.paragraph_format.space_before = Pt(10)
    p_f6.paragraph_format.space_after = Pt(6)
    r_f6 = p_f6.add_run("Figure 4.6: Standalone SQLite Database Visual Inspector")
    set_font(r_f6, size=11.5, bold=True)

    fig6_path = "data/report_screenshots/fig6_db_inspector.png"
    if os.path.exists(fig6_path):
        doc.add_picture(fig6_path, width=Inches(5.4))

    doc.add_page_break()

    # =========================================================================
    # PAGE 19: 4.4 Important Implementation Details
    # =========================================================================
    add_page_header(doc)

    p_iid_lbl = doc.add_paragraph()
    p_iid_lbl.paragraph_format.space_before = Pt(10)
    p_iid_lbl.paragraph_format.space_after = Pt(12)
    r_iid = p_iid_lbl.add_run("4.4 Important Implementation Details")
    set_font(r_iid, size=12, bold=True)

    iid_paras = [
        "The application uses asynchronous non-blocking request handlers and reactive DOM updates to refresh the interface whenever complaint records, officer assignments, or investigation statuses change.",
        "Modular callback functions and RESTful fetch calls connect the frontend single-page interface with the Ktor backend endpoints. This maintains a structured, decoupled approach to application engineering.",
        "The application implements Role-Based Access Control (RBAC) across three distinct roles (Citizen, Vigilance Officer, Administrator). Protected route logic ensures that only Administrators can assign cases, and only assigned Officers can submit field findings.",
        "Local data persistence is powered by SQLite relational tables paired with automated JSON mirroring and evidence image file extraction. This eliminates dependency on external cloud databases during demonstrations and ensures complete local data portability and auditability.",
        "Client-side FileReader API encodes photographic evidence into Base64 format for reliable JSON transmission, while the backend extracts physical image files for direct inspection.",
        "Form validation prevents submission of empty or malformed reports. Mandatory citizen identification ensures accountability while eliminating anonymous false alarms."
    ]

    for para in iid_paras:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(10)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(para)
        set_font(r, size=11)

    doc.add_page_break()

    # =========================================================================
    # PAGE 20: CHAPTER 5: CONCLUSION & FUTURE SCOPE (Part 1)
    # =========================================================================
    add_page_header(doc)

    p_ch5 = doc.add_paragraph()
    p_ch5.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ch5.paragraph_format.space_before = Pt(10)
    p_ch5.paragraph_format.space_after = Pt(20)
    r_ch5 = p_ch5.add_run("CHAPTER 5: CONCLUSION & FUTURE SCOPE")
    set_font(r_ch5, size=14, bold=True, color=RGBColor(15, 23, 42))

    p_c5_lbl = doc.add_paragraph()
    p_c5_lbl.paragraph_format.space_after = Pt(10)
    r_c5lbl = p_c5_lbl.add_run("⮚ Learnings from Web & Mobile Application Development Project:\n5.1 Learnings from Web & Mobile Application Development Project")
    set_font(r_c5lbl, size=12, bold=True)

    learnings = [
        "The development of the POWERGUARD electricity theft reporting and vigilance application provided comprehensive practical knowledge of Kotlin, Ktor Server, and modern web application development. Through this project, we learned how to build an asynchronous backend server using Kotlin coroutines, modular Ktor plugins, and kotlinx.serialization. We gained hands-on experience in creating responsive user interfaces, implementing role-based authentication, handling user input, and validating complex forms with photographic evidence uploads. The project also helped us understand the importance of state management and reactive DOM updates for dynamic dashboard data rendering.",
        "We also gained practical knowledge of relational database persistence using SQLite and JDBC. We learned how to store and retrieve user accounts, complaint details, officer assignments, and chronological audit histories. Implementing features such as unique Reference ID generation, photo Base64 decoding, multi-stage milestone tracking, and theme customization helped us understand how different full-stack modules interact seamlessly. Overall, this project improved our software architecture, problem-solving, debugging, and web application development skills."
    ]

    for l_text in learnings:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(10)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(l_text)
        set_font(r, size=11.5)

    p_fs_lbl = doc.add_paragraph()
    p_fs_lbl.paragraph_format.space_before = Pt(8)
    p_fs_lbl.paragraph_format.space_after = Pt(6)
    r_fslbl = p_fs_lbl.add_run("5.2 Future Scope")
    set_font(r_fslbl, size=12, bold=True)

    p_fs1 = doc.add_paragraph()
    p_fs1.paragraph_format.space_after = Pt(10)
    p_fs1.paragraph_format.line_spacing = 1.15
    r_fs1 = p_fs1.add_run(
        "In the future, the POWERGUARD application can be enhanced by integrating automated AI and Computer Vision models to analyze uploaded evidence photos, automatically classifying illegal hooking wires, shunt bypasses, and broken seals with confidence scores before officer dispatch. Cloud database integration (such as PostgreSQL or AWS RDS) can be introduced to support state-wide multi-utility deployments."
    )
    set_font(r_fs1, size=11.5)

    doc.add_page_break()

    # =========================================================================
    # PAGE 21: CHAPTER 5: CONCLUSION & FUTURE SCOPE (Part 2)
    # =========================================================================
    add_page_header(doc)

    p_fs2 = doc.add_paragraph()
    p_fs2.paragraph_format.space_before = Pt(10)
    p_fs2.paragraph_format.space_after = Pt(12)
    p_fs2.paragraph_format.line_spacing = 1.15
    r_fs2 = p_fs2.add_run(
        "Additionally, Smart Meter (Advanced Metering Infrastructure - AMI) telemetry hooks can be integrated via MQTT or Kafka message brokers to automatically cross-reference citizen complaints with localized transformer load drops and consumption anomalies in real time.\n\n"
        "A dedicated cross-platform mobile application (Android/iOS) can be developed to provide field vigilance officers with GPS-guided navigation, offline site inspection caching, and digital signature capture for on-site penalty assessment receipts. Push notifications can be sent to citizens when their complaints transition through investigation milestones.\n\n"
        "Advanced security mechanisms, role-based biometric authentication, encrypted communication, and role-based audit export can further improve the application's enterprise reliability. These enhancements will transform this educational prototype into a comprehensive, production-grade utility vigilance and smart grid protection system."
    )
    set_font(r_fs2, size=11.5)

    doc.add_page_break()

    # =========================================================================
    # PAGE 22: CHAPTER 6: SUSTAINABLE DEVELOPMENT GOALS (SDG) MAPPING (Part 1)
    # =========================================================================
    add_page_header(doc)

    p_ch6 = doc.add_paragraph()
    p_ch6.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ch6.paragraph_format.space_before = Pt(10)
    p_ch6.paragraph_format.space_after = Pt(20)
    r_ch6 = p_ch6.add_run("CHAPTER 6: SUSTAINABLE DEVELOPMENT GOALS (SDG)\nMAPPING")
    set_font(r_ch6, size=14, bold=True, color=RGBColor(15, 23, 42))

    p_sdg_lbl = doc.add_paragraph()
    p_sdg_lbl.paragraph_format.space_after = Pt(8)
    r_sdglbl = p_sdg_lbl.add_run("⮚ SDG Goals No. along with description:\n6.1 SDG Goals and Their Description")
    set_font(r_sdglbl, size=12, bold=True)

    p_sdg_intro = doc.add_paragraph()
    p_sdg_intro.paragraph_format.space_after = Pt(10)
    p_sdg_intro.paragraph_format.line_spacing = 1.15
    r_sintro = p_sdg_intro.add_run(
        "The POWERGUARD electricity theft reporting and vigilance application aligns with several United Nations Sustainable Development Goals (SDGs), particularly those associated with clean energy reliability, sustainable infrastructure, community safety, and transparent institutional governance."
    )
    set_font(r_sintro, size=11.5)

    sdg_p22 = [
        ("SDG 7: Affordable and Clean Energy",
         "Goal: Ensure access to affordable, reliable, sustainable and modern energy for all.",
         "Relation to the Project:\nElectricity theft causes immense unmetered energy waste and destabilizes electrical distribution networks, forcing utilities to burn more fossil fuels to compensate for distribution deficits. By curbing non-technical distribution losses, POWERGUARD stabilizes power distribution, protects transformers from overloads, and ensures more affordable, reliable electricity for legitimate consumers."),
        
        ("SDG 9: Industry, Innovation and Infrastructure",
         "Goal: Build resilient infrastructure, promote inclusive and sustainable industrialization and foster innovation.",
         "Relation to the Project:\nThe project demonstrates the use of modern asynchronous web technologies (Kotlin and Ktor) to build a resilient utility vigilance platform. It digitizes paper-based complaint registers, introducing automated case triage and digital evidence verification to modernize electrical distribution monitoring.")
    ]

    for title, goal, rel in sdg_p22:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.line_spacing = 1.15
        r_t = p.add_run(title + "\n")
        set_font(r_t, size=11.5, bold=True)
        r_g = p.add_run(goal + "\n")
        set_font(r_g, size=11, italic=True)
        r_r = p.add_run(rel)
        set_font(r_r, size=11)

    doc.add_page_break()

    # =========================================================================
    # PAGE 23: CHAPTER 6: SUSTAINABLE DEVELOPMENT GOALS (SDG) MAPPING (Part 2)
    # =========================================================================
    add_page_header(doc)

    sdg_p23 = [
        ("SDG 11: Sustainable Cities and Communities",
         "Goal: Make cities and human settlements inclusive, safe, resilient and sustainable.",
         "Relation to the Project:\nUnregulated wire hooking (kundi) into overhead distribution cables poses critical fire hazards and life-threatening electrocution risks in dense urban settlements. POWERGUARD provides rapid complaint filing and officer dispatch, protecting urban neighborhoods from electrical fires and grid failures."),
        
        ("SDG 16: Peace, Justice and Strong Institutions",
         "Goal: Promote peaceful and inclusive societies for sustainable development, provide access to justice for all and build effective, accountable and inclusive institutions at all levels.",
         "Relation to the Project:\nBy maintaining an immutable digital audit history with chronological timestamps, assigned officer IDs, and public milestone tracking, POWERGUARD eliminates bureaucratic opacity, prevents bribery, and combats administrative corruption in public utilities.")
    ]

    for title, goal, rel in sdg_p23:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.line_spacing = 1.15
        r_t = p.add_run(title + "\n")
        set_font(r_t, size=11.5, bold=True)
        r_g = p.add_run(goal + "\n")
        set_font(r_g, size=11, italic=True)
        r_r = p.add_run(rel)
        set_font(r_r, size=11)

    p_sdg_conc = doc.add_paragraph()
    p_sdg_conc.paragraph_format.space_before = Pt(10)
    p_sdg_conc.paragraph_format.space_after = Pt(8)
    r_sconclbl = p_sdg_conc.add_run("Conclusion of SDG Mapping\n")
    set_font(r_sconclbl, size=11.5, bold=True)
    r_sconctxt = p_sdg_conc.add_run(
        "The POWERGUARD application primarily supports the objectives of SDG 7 and SDG 9 by enhancing electrical grid reliability and modernizing vigilance infrastructure. It also strongly contributes to SDG 11 and SDG 16 through community electrical safety and transparent public governance. Although developed as an educational prototype, it demonstrates how digital technology can protect essential public utilities and promote sustainable energy distribution."
    )
    set_font(r_sconctxt, size=11)

    doc.add_page_break()

    # =========================================================================
    # PAGE 24: CHAPTER 7: REFERENCES
    # =========================================================================
    add_page_header(doc)

    p_ch7 = doc.add_paragraph()
    p_ch7.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ch7.paragraph_format.space_before = Pt(10)
    p_ch7.paragraph_format.space_after = Pt(16)
    r_ch7 = p_ch7.add_run("CHAPTER 7: REFERENCES")
    set_font(r_ch7, size=14, bold=True, color=RGBColor(15, 23, 42))

    p_r_lbl = doc.add_paragraph()
    p_r_lbl.paragraph_format.space_after = Pt(8)
    r_rlbl = p_r_lbl.add_run("7.1 References\nThe following resources are relevant to the technologies and concepts used in the development of the POWERGUARD electricity theft reporting and vigilance application:")
    set_font(r_rlbl, size=11.5)

    ref_items = [
        ("1. Kotlin Documentation – Official documentation for Kotlin programming language, syntax, coroutines and data classes.",
         "https://kotlinlang.org/docs/home.html"),
        ("2. Ktor Framework Documentation – Official documentation for Ktor asynchronous server, routing, plugins, and Netty engine.",
         "https://ktor.io/docs/server-overview.html"),
        ("3. SQLite Database Documentation – Documentation for SQLite embedded relational engine, SQL syntax, and ACID compliance.",
         "https://www.sqlite.org/docs.html"),
        ("4. kotlinx.serialization Guide – Documentation for JSON encoding, decoding, and data serialization in Kotlin.",
         "https://github.com/Kotlin/kotlinx.serialization"),
        ("5. Central Electricity Authority (CEA) – Reports on Aggregate Technical & Commercial (AT&C) losses in power distribution utilities.",
         "https://cea.nic.in/"),
        ("6. Mozilla Developer Network (MDN) – Documentation for HTML5 File API, FileReader, and CSS3 Custom Properties.",
         "https://developer.mozilla.org/en-US/docs/Web"),
        ("7. Visual Studio Code – Documentation for code editor, Kotlin extensions, and development environment.",
         "https://code.visualstudio.com/docs"),
        ("8. United Nations Sustainable Development Goals – Official documentation for SDG 7, SDG 9, SDG 11, and SDG 16.",
         "https://sdgs.un.org/goals")
    ]

    for title, link in ref_items:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15
        r_t = p.add_run(title + "\n")
        set_font(r_t, size=10.5)
        r_l = p.add_run(link)
        set_font(r_l, size=10, italic=True, color=RGBColor(2, 132, 199))

    out_file = "PowerGuard_Academic_Report_24Pages.docx"
    doc.save(out_file)
    print(f"24-Page Project Report successfully created: {out_file}")

    try:
        doc.save("PowerGuard_Project_Report.docx")
        print("Also updated PowerGuard_Project_Report.docx")
    except Exception as e:
        print(f"Notice: PowerGuard_Project_Report.docx was locked by Word: {e}")

if __name__ == "__main__":
    build_24page_report()
