import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def build_presentation():
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Theme Colors
    BG_DARK = RGBColor(11, 17, 32)        # #0B1120
    CARD_BG = RGBColor(21, 31, 50)        # #151F32
    CARD_BORDER = RGBColor(36, 53, 83)    # #243553
    TEXT_WHITE = RGBColor(248, 250, 252)  # #F8FAFC
    TEXT_MUTED = RGBColor(148, 163, 184)  # #94A3B8
    AMBER = RGBColor(245, 158, 11)        # #F59E0B
    SKY_BLUE = RGBColor(56, 189, 248)     # #38BDF8
    EMERALD = RGBColor(16, 185, 129)      # #10B981
    PURPLE = RGBColor(168, 85, 247)       # #A855F7

    blank_layout = prs.slide_layouts[6]

    def set_slide_background(slide):
        bg_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg_box.fill.solid()
        bg_box.fill.fore_color.rgb = BG_DARK
        bg_box.line.color.rgb = BG_DARK

    def add_header(slide, title_text, category_text="POWERGUARD VIGILANCE PLATFORM"):
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(1.1))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p0 = tf.paragraphs[0]
        p0.text = category_text.upper()
        p0.font.size = Pt(10)
        p0.font.bold = True
        p0.font.color.rgb = AMBER

        p1 = tf.add_paragraph()
        p1.text = title_text
        p1.font.size = Pt(24)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_WHITE
        p1.space_before = Pt(3)

    def add_card(slide, left, top, width, height, title="", title_color=AMBER, bg_color=CARD_BG, border_color=CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)

        if title:
            tb = slide.shapes.add_textbox(left + Inches(0.25), top + Inches(0.2), width - Inches(0.5), Inches(0.45))
            tf = tb.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
            p = tf.paragraphs[0]
            p.text = title
            p.font.size = Pt(15)
            p.font.bold = True
            p.font.color.rgb = title_color

        return card

    # =========================================================================
    # SLIDE 1: Title Slide
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    # Main Center Card
    add_card(s1, Inches(1.2), Inches(1.0), Inches(10.933), Inches(5.5), bg_color=CARD_BG, border_color=CARD_BORDER)

    # Badge Pill
    pill = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.6), Inches(1.4), Inches(4.2), Inches(0.4))
    pill.fill.solid()
    pill.fill.fore_color.rgb = RGBColor(30, 41, 59)
    pill.line.color.rgb = AMBER
    pill.line.width = Pt(1)
    ptf = pill.text_frame
    ptf.vertical_anchor = MSO_ANCHOR.MIDDLE
    pp = ptf.paragraphs[0]
    pp.alignment = PP_ALIGN.CENTER
    pp.text = "⚡ KOTLIN & KTOR POWER VIGILANCE SYSTEM"
    pp.font.size = Pt(11)
    pp.font.bold = True
    pp.font.color.rgb = AMBER

    # Title & Subtitle text box
    tb = s1.shapes.add_textbox(Inches(1.6), Inches(2.0), Inches(10.0), Inches(2.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = "PowerGuard: Electricity Theft Reporting & Vigilance Portal"
    p1.font.size = Pt(30)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_WHITE

    p2 = tf.add_paragraph()
    p2.text = "A Role-Based Full-Stack Web Platform for Power Distribution Vigilance, Evidence Auditing & Field Investigation Oversight"
    p2.font.size = Pt(14)
    p2.font.color.rgb = TEXT_MUTED
    p2.space_before = Pt(10)

    # 3 Highlights Cards inside Slide 1
    features = [
        ("👤 Citizen Whistleblowing", "Named reporting with mobile verification, GPS location & photo evidence", SKY_BLUE),
        ("🛡️ Central Admin Control", "Real-time KPI dashboard, case triage & officer dispatch allocation", AMBER),
        ("👮 Vigilance Officer Desk", "Site inspection, load verification & digital audit resolution log", EMERALD)
    ]
    for i, (f_title, f_desc, color) in enumerate(features):
        c_left = Inches(1.6 + i * 3.4)
        c_top = Inches(4.5)
        add_card(s1, c_left, c_top, Inches(3.2), Inches(1.6), title=f_title, title_color=color, bg_color=RGBColor(15, 23, 42))
        t_box = s1.shapes.add_textbox(c_left + Inches(0.2), c_top + Inches(0.65), Inches(2.8), Inches(0.8))
        tf_c = t_box.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = tf_c.margin_top = tf_c.margin_right = tf_c.margin_bottom = 0
        p = tf_c.paragraphs[0]
        p.text = f_desc
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 2: Problem Statement & Motivation
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "Problem Statement & Industry Motivation", "Challenges in Power Distribution")

    # Column 1: The Critical Problem (Card Left)
    add_card(s2, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.2), title="⚠️ The Challenges of Electricity Theft", title_color=RGBColor(239, 68, 68))
    tb_left = s2.shapes.add_textbox(Inches(1.1), Inches(2.4), Inches(5.0), Inches(4.3))
    tf_l = tb_left.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = tf_l.margin_top = tf_l.margin_right = tf_l.margin_bottom = 0

    points_l = [
        ("Massive Financial Losses: ", "Commercial and residential electricity theft causes over 20-30% Aggregate Technical & Commercial (AT&C) losses for DISCOM utilities."),
        ("Hazardous Public Safety Risks: ", "Unregulated direct line hooking (kundi) and bypassed service cables lead to transformer overloads, short-circuits, and electrocution hazards."),
        ("Slow & Opaque Manual Reporting: ", "Citizens lack an accessible, real-time reporting channel; paper-based complaints are frequently delayed or lost in bureaucracy."),
        ("Absence of Chain-of-Custody: ", "Vigilance officers lack tamper-proof digital evidence logs, premises landmarks, and chronological audit histories to take legal enforcement.")
    ]
    for i, (bold_txt, regular_txt) in enumerate(points_l):
        p = tf_l.add_paragraph() if i > 0 else tf_l.paragraphs[0]
        p.space_before = Pt(10)
        r1 = p.add_run()
        r1.text = "• " + bold_txt
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = TEXT_WHITE
        r2 = p.add_run()
        r2.text = regular_txt
        r2.font.size = Pt(11.5)
        r2.font.color.rgb = TEXT_MUTED

    # Column 2: The PowerGuard Solution (Card Right)
    add_card(s2, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.2), title="💡 The PowerGuard Automated Solution", title_color=EMERALD)
    tb_right = s2.shapes.add_textbox(Inches(7.1), Inches(2.4), Inches(5.1), Inches(4.3))
    tf_r = tb_right.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = tf_r.margin_top = tf_r.margin_right = tf_r.margin_bottom = 0

    points_r = [
        ("Citizen Direct Reporting: ", "Easy web portal enabling named citizens to submit complaints with exact pole landmarks and photographic evidence."),
        ("Centralized Administrative Triage: ", "Automated case ticketing generating unique Reference IDs (e.g. PG-2026-1084) for triage and priority dispatch."),
        ("Designated Field Officer Allocation: ", "Administrators assign complaints directly to specialized Vigilance Officers with clear inspection instructions."),
        ("Digital Evidence & Audit Stepper: ", "Real-time transparent progress tracking from Submission → Under Investigation → Dispatched → Resolved/Confirmed.")
    ]
    for i, (bold_txt, regular_txt) in enumerate(points_r):
        p = tf_r.add_paragraph() if i > 0 else tf_r.paragraphs[0]
        p.space_before = Pt(10)
        r1 = p.add_run()
        r1.text = "✔ " + bold_txt
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = TEXT_WHITE
        r2 = p.add_run()
        r2.text = regular_txt
        r2.font.size = Pt(11.5)
        r2.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 3: 3-Role Architecture & Workflow
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "3-Role Vigilance Architecture & Operations", "Role-Based Access Control (RBAC)")

    role_cards = [
        ("👤 1. Citizen Portal", "View & Make Reports", SKY_BLUE, [
            ("Named Identity: ", "Submits reports with full name, contact mobile, and optional email."),
            ("Incident Detailing: ", "Categorizes theft (Direct Hooking, Meter Bypass, Sub-metering, etc.)."),
            ("Photographic Evidence: ", "Attaches site photos and electric pole identification numbers."),
            ("My Submitted Reports: ", "Monitors assignment status and official inspection updates live.")
        ]),
        ("🛡️ 2. Central Admin Desk", "Case Review & Allocation", AMBER, [
            ("Oversight Dashboard: ", "Analyzes live KPIs (total reports, active investigations, resolved cases)."),
            ("Case Triage: ", "Evaluates hazard severity levels (Critical, High, Medium, Low)."),
            ("Officer Assignment: ", "Assigns complaints to field vigilance officers with custom instructions."),
            ("Data Export: ", "Exports complete audit reports to CSV for senior management oversight.")
        ]),
        ("👮 3. Vigilance Officer Desk", "Field Inspection & Action", EMERALD, [
            ("Assigned Cases Desk: ", "Accesses complaints specifically allocated by the Administrator."),
            ("Site Inspection: ", "Examines uploaded photo evidence, premises GPS, and suspect consumer IDs."),
            ("Status Transitions: ", "Updates case state: Under Investigation → Team Dispatched → Resolved."),
            ("Official Findings Log: ", "Records legal seizure notes, penalty assessments, and resolution logs.")
        ])
    ]

    for idx, (r_title, r_sub, r_col, r_items) in enumerate(role_cards):
        c_x = Inches(0.8 + idx * 3.95)
        add_card(s3, c_x, Inches(1.7), Inches(3.75), Inches(5.2), title=r_title, title_color=r_col)

        sub_tb = s3.shapes.add_textbox(c_x + Inches(0.25), Inches(2.25), Inches(3.25), Inches(0.35))
        tf_s = sub_tb.text_frame
        p_sub = tf_s.paragraphs[0]
        p_sub.text = r_sub.upper()
        p_sub.font.size = Pt(9.5)
        p_sub.font.bold = True
        p_sub.font.color.rgb = TEXT_MUTED

        items_tb = s3.shapes.add_textbox(c_x + Inches(0.25), Inches(2.65), Inches(3.25), Inches(4.0))
        tf_i = items_tb.text_frame
        tf_i.word_wrap = True
        tf_i.margin_left = tf_i.margin_top = tf_i.margin_right = tf_i.margin_bottom = 0

        for j, (bold_txt, regular_txt) in enumerate(r_items):
            p = tf_i.add_paragraph() if j > 0 else tf_i.paragraphs[0]
            p.space_before = Pt(8)
            r1 = p.add_run()
            r1.text = "• " + bold_txt
            r1.font.bold = True
            r1.font.size = Pt(11)
            r1.font.color.rgb = TEXT_WHITE
            r2 = p.add_run()
            r2.text = regular_txt
            r2.font.size = Pt(10.5)
            r2.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 4: Technical Architecture & System Design
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "System Architecture & Technology Stack", "Full-Stack Implementation")

    tech_cards = [
        ("⚙️ Backend Core: Kotlin & Ktor", SKY_BLUE, Inches(0.8), Inches(1.7), Inches(5.6), Inches(2.5), [
            ("Language: ", "Kotlin 2.2.20 (Modern, type-safe, expressive, asynchronous)."),
            ("Web Framework: ", "Ktor Server running on Netty asynchronous high-throughput engine."),
            ("Serialization: ", "kotlinx.serialization for lightning-fast JSON encoding & decoding."),
            ("REST API Design: ", "Clean REST endpoints for Auth, Reports, Officer Assignment & Stats.")
        ]),
        ("💾 Database & Data Integrity", EMERALD, Inches(6.8), Inches(1.7), Inches(5.7), Inches(2.5), [
            ("SQLite Storage: ", "Local relational database (data/powerguard.db) with thread-safe access."),
            ("Automatic Mirroring: ", "Synchronized JSON export (reports_mirror.json) for instant inspection."),
            ("Evidence Management: ", "Decodes & stores evidence photos in data/evidence_images/ folder."),
            ("Audit Trail: ", "Stores chronological status history entries with author identity & timestamps.")
        ]),
        ("🎨 Frontend UI & Interaction", AMBER, Inches(0.8), Inches(4.4), Inches(5.6), Inches(2.5), [
            ("Responsive Single Page: ", "Vanilla HTML5, modern CSS3 variables, and reactive JavaScript."),
            ("Photo Thumbnails in Tables: ", "Visual evidence thumbnails displayed right beside each complaint."),
            ("Dual Modals: ", "Interactive inspection lightbox & officer assignment configuration popup."),
            ("No External Bloat: ", "Zero heavy frameworks; lightweight, rapid loading, presentation-ready.")
        ]),
        ("🛡️ Security & Access Control", PURPLE, Inches(6.8), Inches(4.4), Inches(5.7), Inches(2.5), [
            ("Role-Based Access: ", "Strict separation of CITIZEN, OFFICER, and ADMIN viewports."),
            ("Protected State Machines: ", "Only Admins can assign officers; only Officers can update status."),
            ("Contact Validation: ", "Mandatory citizen full name and contact mobile number verification."),
            ("Visual Inspector: ", "Standalone HTML database browser for auditing DB contents and images.")
        ])
    ]

    for title, col, x, y, w, h, items in tech_cards:
        add_card(s4, x, y, w, h, title=title, title_color=col)
        c_tb = s4.shapes.add_textbox(x + Inches(0.25), y + Inches(0.65), w - Inches(0.5), h - Inches(0.75))
        tf_c = c_tb.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = tf_c.margin_top = tf_c.margin_right = tf_c.margin_bottom = 0

        for j, (bold_txt, regular_txt) in enumerate(items):
            p = tf_c.add_paragraph() if j > 0 else tf_c.paragraphs[0]
            p.space_before = Pt(4)
            r1 = p.add_run()
            r1.text = "• " + bold_txt
            r1.font.bold = True
            r1.font.size = Pt(11)
            r1.font.color.rgb = TEXT_WHITE
            r2 = p.add_run()
            r2.text = regular_txt
            r2.font.size = Pt(10.5)
            r2.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 5: Key Features & Demonstration Highlights
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Key Features & Platform Capabilities", "Interactive Platform Demonstration")

    demo_features = [
        ("1. Identified Citizen Reporting", "Mandatory citizen contact info (Name, Phone, Email) auto-populated from profile; eliminates anonymous false alarms while preserving clean report records.", SKY_BLUE),
        ("2. Visual Evidence Alongside Complaints", "Uploaded evidence photos are rendered as interactive thumbnails directly beside each complaint across Admin, Officer, and Citizen dashboards.", AMBER),
        ("3. End-to-End Progress Stepper", "Citizens and officers track complaints in real time via 4-stage visual stepper: Submitted → Assigned → Field Inspection → Action Completed.", EMERALD),
        ("4. Comprehensive Theft Taxonomy", "Standardized categorization covering Direct Hooking, Shunt Bypass, Commercial Sub-Metering, Transformer Taps, and Underground Splicing.", PURPLE),
        ("5. Live Analytics & KPI Telemetry", "Real-time summary metrics on pending assignments, active investigations, resolved cases, and dynamic theft category horizontal breakdown bars.", SKY_BLUE),
        ("6. Standalone Database Visual Inspector", "Integrated HTML table viewer allowing direct visual browsing of powerguard.db rows and photos inside VS Code or any standard browser.", AMBER)
    ]

    for idx, (f_title, f_desc, col) in enumerate(demo_features):
        row = idx // 2
        col_idx = idx % 2
        card_x = Inches(0.8 + col_idx * 5.95)
        card_y = Inches(1.7 + row * 1.7)
        card_w = Inches(5.75)
        card_h = Inches(1.5)

        add_card(s5, card_x, card_y, card_w, card_h, title=f_title, title_color=col)
        t_box = s5.shapes.add_textbox(card_x + Inches(0.25), card_y + Inches(0.6), card_w - Inches(0.5), Inches(0.8))
        tf_f = t_box.text_frame
        tf_f.word_wrap = True
        tf_f.margin_left = tf_f.margin_top = tf_f.margin_right = tf_f.margin_bottom = 0
        p = tf_f.paragraphs[0]
        p.text = f_desc
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 6: Conclusion, Impact & Future Scope
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Project Impact & Future Enhancements", "Summary & Roadmap")

    # Left Card: Project Impact
    add_card(s6, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.2), title="🏆 Key Achievements & Impact", title_color=EMERALD)
    tb_imp = s6.shapes.add_textbox(Inches(1.1), Inches(2.4), Inches(5.0), Inches(4.3))
    tf_imp = tb_imp.text_frame
    tf_imp.word_wrap = True
    tf_imp.margin_left = tf_imp.margin_top = tf_imp.margin_right = tf_imp.margin_bottom = 0

    impact_points = [
        ("Loss Reduction: ", "Enables electricity distribution companies to swiftly detect, inspect, and curb revenue loss from non-technical commercial theft."),
        ("Accountability & Transparency: ", "Eliminates lost paperwork with immutable digital audit trails showing exact officer assignments, inspection dates, and remarks."),
        ("Citizen Empowerment: ", "Provides public consumers with an easy, responsive platform to protect grid infrastructure and report fire hazards."),
        ("Production Readiness: ", "Clean architecture with Kotlin & Ktor, verified build, fully functional local SQLite database, and complete GitHub repository.")
    ]
    for i, (bold_txt, regular_txt) in enumerate(impact_points):
        p = tf_imp.add_paragraph() if i > 0 else tf_imp.paragraphs[0]
        p.space_before = Pt(10)
        r1 = p.add_run()
        r1.text = "✔ " + bold_txt
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = TEXT_WHITE
        r2 = p.add_run()
        r2.text = regular_txt
        r2.font.size = Pt(11.5)
        r2.font.color.rgb = TEXT_MUTED

    # Right Card: Future Scope
    add_card(s6, Inches(6.8), Inches(1.7), Inches(5.7), Inches(3.6), title="🚀 Future Scope & Enhancements", title_color=SKY_BLUE)
    tb_fut = s6.shapes.add_textbox(Inches(7.1), Inches(2.4), Inches(5.1), Inches(2.7))
    tf_fut = tb_fut.text_frame
    tf_fut.word_wrap = True
    tf_fut.margin_left = tf_fut.margin_top = tf_fut.margin_right = tf_fut.margin_bottom = 0

    future_points = [
        ("AI Computer Vision: ", "Automated visual analysis on evidence images to detect hookings, bypassed meter seals, and shunt wires."),
        ("Smart Meter Telemetry (AMI): ", "Integration with smart grid sensors for automatic theft alarms when meter consumption drops anomalously."),
        ("Mobile Field App: ", "Native Android/iOS application with offline inspection caching and GPS geotag verification.")
    ]
    for i, (bold_txt, regular_txt) in enumerate(future_points):
        p = tf_fut.add_paragraph() if i > 0 else tf_fut.paragraphs[0]
        p.space_before = Pt(8)
        r1 = p.add_run()
        r1.text = "→ " + bold_txt
        r1.font.bold = True
        r1.font.size = Pt(11.5)
        r1.font.color.rgb = TEXT_WHITE
        r2 = p.add_run()
        r2.text = regular_txt
        r2.font.size = Pt(11)
        r2.font.color.rgb = TEXT_MUTED

    # Bottom Right Thank You Box
    add_card(s6, Inches(6.8), Inches(5.5), Inches(5.7), Inches(1.4), bg_color=RGBColor(15, 23, 42), border_color=AMBER)
    tb_ty = s6.shapes.add_textbox(Inches(7.1), Inches(5.65), Inches(5.1), Inches(1.1))
    tf_ty = tb_ty.text_frame
    tf_ty.word_wrap = True
    tf_ty.margin_left = tf_ty.margin_top = tf_ty.margin_right = tf_ty.margin_bottom = 0

    p_ty = tf_ty.paragraphs[0]
    p_ty.text = "Thank You! Questions & Discussion"
    p_ty.font.size = Pt(16)
    p_ty.font.bold = True
    p_ty.font.color.rgb = AMBER

    p_repo = tf_ty.add_paragraph()
    p_repo.text = "GitHub Repository: https://github.com/pratik0437/electricity-theft-reporting"
    p_repo.font.size = Pt(10.5)
    p_repo.font.color.rgb = TEXT_WHITE
    p_repo.space_before = Pt(4)

    output_path = "PowerGuard_Project_Presentation.pptx"
    prs.save(output_path)
    print(f"Presentation saved successfully to: {output_path}")

if __name__ == "__main__":
    build_presentation()
