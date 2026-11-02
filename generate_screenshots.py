import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs("data/report_screenshots", exist_ok=True)

# Helper to draw a modern card
def create_ui_image(title, subtitle, elements, output_path, bg_color=(11, 17, 32), card_color=(21, 31, 50)):
    w, h = 960, 540
    img = Image.new("RGB", (w, h), bg_color)
    draw = ImageDraw.Draw(img)

    # Top browser bar
    draw.rectangle([0, 0, w, 36], fill=(15, 23, 42))
    # Window circles
    draw.ellipse([14, 12, 26, 24], fill=(239, 68, 68))
    draw.ellipse([34, 12, 46, 24], fill=(245, 158, 11))
    draw.ellipse([54, 12, 66, 24], fill=(16, 185, 129))
    # URL bar
    draw.rectangle([90, 8, w - 90, 28], fill=(30, 41, 59), outline=(51, 65, 85))
    draw.text((105, 11), "http://localhost:8080/powerguard", fill=(148, 163, 184))

    # App Header
    draw.rectangle([0, 36, w, 85], fill=(15, 23, 42), outline=(36, 53, 83))
    draw.text((30, 48), "⚡ PowerGuard Vigilance Portal", fill=(245, 158, 11))
    draw.text((30, 68), "Electricity Theft Reporting & Investigation Management", fill=(148, 163, 184))

    # Page Title Box
    draw.text((30, 100), title, fill=(248, 250, 252))
    draw.text((30, 124), subtitle, fill=(56, 189, 248))

    # Render elements
    for el in elements:
        t = el.get("type")
        if t == "card":
            box = el["box"]
            draw.rectangle(box, fill=el.get("bg", card_color), outline=el.get("border", (36, 53, 83)), width=el.get("width", 1))
            if "title" in el:
                draw.text((box[0] + 15, box[1] + 12), el["title"], fill=el.get("t_color", (248, 250, 252)))
            if "desc" in el:
                draw.text((box[0] + 15, box[1] + 36), el["desc"], fill=el.get("d_color", (148, 163, 184)))
        elif t == "text":
            draw.text(el["pos"], el["text"], fill=el.get("color", (248, 250, 252)))
        elif t == "input":
            box = el["box"]
            draw.rectangle(box, fill=(15, 23, 42), outline=(51, 65, 85))
            draw.text((box[0] + 10, box[1] + 8), el.get("placeholder", ""), fill=(148, 163, 184))
        elif t == "button":
            box = el["box"]
            draw.rectangle(box, fill=el.get("bg", (245, 158, 11)), outline=el.get("border", (217, 119, 6)))
            draw.text((box[0] + 15, box[1] + 8), el.get("text", "Button"), fill=el.get("t_color", (255, 255, 255)))

    img.save(output_path, "PNG")
    print(f"Created: {output_path}")

# 1. Login Screen
create_ui_image(
    "Portal Sign In & Role Authentication",
    "Select your portal role (Citizen, Officer, Admin) and enter credentials",
    [
        {"type": "card", "box": [280, 150, 680, 480], "bg": (17, 26, 46), "border": (245, 158, 11), "width": 2},
        {"type": "text", "pos": [310, 175], "text": "🔐 Sign In to PowerGuard Portal", "color": (248, 250, 252)},
        {"type": "button", "box": [310, 215, 420, 245], "bg": (245, 158, 11), "text": "👤 Citizen"},
        {"type": "button", "box": [430, 215, 540, 245], "bg": (30, 41, 59), "text": "👮 Officer"},
        {"type": "button", "box": [550, 215, 650, 245], "bg": (30, 41, 59), "text": "🛡️ Admin"},
        {"type": "text", "pos": [310, 265], "text": "Username / Moodle ID *", "color": (148, 163, 184)},
        {"type": "input", "box": [310, 290, 650, 325], "placeholder": "Enter username or citizen ID"},
        {"type": "text", "pos": [310, 345], "text": "Password *", "color": (148, 163, 184)},
        {"type": "input", "box": [310, 370, 650, 405], "placeholder": "••••••••••••"},
        {"type": "button", "box": [310, 425, 650, 460], "bg": (245, 158, 11), "text": "🔒 Secure Sign In to Portal"},
    ],
    "data/report_screenshots/fig1_login.png"
)

# 2. Registration Screen
create_ui_image(
    "New Citizen Account Registration",
    "Create a verified citizen account for complaint submission & tracking",
    [
        {"type": "card", "box": [280, 150, 680, 490], "bg": (17, 26, 46), "border": (56, 189, 248), "width": 2},
        {"type": "text", "pos": [310, 175], "text": "📝 Citizen Account Registration", "color": (248, 250, 252)},
        {"type": "text", "pos": [310, 215], "text": "Full Name *", "color": (148, 163, 184)},
        {"type": "input", "box": [310, 235, 650, 268], "placeholder": "Pratik Mali"},
        {"type": "text", "pos": [310, 280], "text": "Mobile Phone Number *", "color": (148, 163, 184)},
        {"type": "input", "box": [310, 300, 650, 333], "placeholder": "+91 98201 23456"},
        {"type": "text", "pos": [310, 345], "text": "Email Address (Optional)", "color": (148, 163, 184)},
        {"type": "input", "box": [310, 365, 650, 398], "placeholder": "pratik.mali@apsit.edu.in"},
        {"type": "button", "box": [310, 425, 650, 460], "bg": (16, 185, 129), "text": "✅ Create Account & Proceed"}
    ],
    "data/report_screenshots/fig2_register.png"
)

# 3. Citizen Report Dashboard
create_ui_image(
    "Citizen Electricity Theft Reporting Dashboard",
    "Submit incident details, nearest electric pole, and photo evidence",
    [
        {"type": "card", "box": [30, 150, 580, 500], "title": "⚡ File an Electricity Theft Complaint", "desc": "Provide verified premises landmark and attach evidence photos"},
        {"type": "text", "pos": [50, 215], "text": "Theft Category: Direct Line Hooking (Kundi)", "color": (245, 158, 11)},
        {"type": "input", "box": [50, 240, 560, 275], "placeholder": "Direct wire tapped from distribution box"},
        {"type": "text", "pos": [50, 290], "text": "Premises Address & Nearest Pole Number", "color": (148, 163, 184)},
        {"type": "input", "box": [50, 310, 560, 345], "placeholder": "Plot 42, Sector 7, Near Pole #LT-442"},
        {"type": "card", "box": [50, 360, 560, 440], "bg": (15, 23, 42), "border": (245, 158, 11), "title": "📷 Evidence Photo Attached: exp8.png", "desc": "Base64 encoded & verified for vigilance inspection"},
        {"type": "button", "box": [50, 455, 250, 490], "bg": (245, 158, 11), "text": "🚨 Submit Theft Report"},
        {"type": "card", "box": [610, 150, 930, 500], "title": "📋 My Submitted Reports", "desc": "Live tracking by Reference ID"},
        {"type": "card", "box": [630, 215, 910, 295], "bg": (15, 23, 42), "border": (56, 189, 248), "title": "PG-2026-1084 | Direct Hooking", "desc": "Status: SUBMITTED (Pending Assignment)"},
        {"type": "card", "box": [630, 315, 910, 395], "bg": (15, 23, 42), "border": (16, 185, 129), "title": "PG-2026-6021 | Wire Tapping", "desc": "Status: RESOLVED_CONFIRMED (Action Done)"}
    ],
    "data/report_screenshots/fig3_citizen.png"
)

# 4. Admin Oversight Dashboard
create_ui_image(
    "Central Administrator Case Oversight & KPI Desk",
    "Monitor real-time system KPIs and review incoming theft complaints",
    [
        {"type": "card", "box": [30, 150, 240, 225], "title": "4 Total Reports", "desc": "All registered cases", "title_color": (248, 250, 252)},
        {"type": "card", "box": [260, 150, 470, 225], "title": "2 Pending Allocation", "desc": "Awaiting officer", "title_color": (56, 189, 248)},
        {"type": "card", "box": [490, 150, 700, 225], "title": "1 Active Investigation", "desc": "Field team inspecting", "title_color": (245, 158, 11)},
        {"type": "card", "box": [720, 150, 930, 225], "title": "1 Case Confirmed", "desc": "Seizure penalty served", "title_color": (16, 185, 129)},
        {"type": "card", "box": [30, 245, 930, 500], "title": "🛡️ Incoming Citizen Complaints Review Table", "desc": "Displaying Reference IDs, Evidence Photos, and Officer Assignment Actions"},
        {"type": "text", "pos": [50, 305], "text": "Ref ID: PG-2026-1084 | Photo: [Thumb] | Title: Direct Hooking | Pole #LT-442 | Action: [Assign Officer]", "color": (248, 250, 252)},
        {"type": "text", "pos": [50, 355], "text": "Ref ID: PG-2026-6021 | Photo: [Thumb] | Title: Distribution Box Tap | Pole #LT-442 | Officer: Er. Deshmukh", "color": (56, 189, 248)},
        {"type": "text", "pos": [50, 405], "text": "Ref ID: PG-2026-5995 | Photo: [Thumb] | Title: Meter Shunt Bypass | Pole #HT-102 | Action: [Assign Officer]", "color": (248, 250, 252)},
        {"type": "text", "pos": [50, 455], "text": "Ref ID: PG-2026-5332 | Photo: [None]  | Title: Commercial Sub-meter | Pole #LT-890 | Officer: Er. Priya Nair", "color": (16, 185, 129)}
    ],
    "data/report_screenshots/fig4_admin.png"
)

# 5. Officer Assignment & Inspection
create_ui_image(
    "Vigilance Officer Field Investigation Desk",
    "Inspect site photo evidence, update case status, and submit findings",
    [
        {"type": "card", "box": [30, 150, 930, 500], "title": "👮 Investigation Desk — Er. Vikramaditya Deshmukh", "desc": "Assigned electricity theft reports for vigilance verification"},
        {"type": "card", "box": [60, 215, 480, 475], "bg": (15, 23, 42), "border": (245, 158, 11), "title": "📷 Photographic Evidence Verification", "desc": "Click to enlarge full-resolution photo of illegal tapping"},
        {"type": "card", "box": [510, 215, 900, 475], "bg": (17, 26, 46), "border": (56, 189, 248), "title": "📝 Official Inspection Log Submission"},
        {"type": "text", "pos": [530, 260], "text": "Complaint Ref: PG-2026-1084", "color": (56, 189, 248)},
        {"type": "text", "pos": [530, 290], "text": "Current Status: RESOLVED_CONFIRMED", "color": (16, 185, 129)},
        {"type": "text", "pos": [530, 325], "text": "Inspection Notes & Legal Findings:", "color": (148, 163, 184)},
        {"type": "input", "box": [530, 350, 880, 405], "placeholder": "Hooking wire disconnected and seized. Penalty notice served."},
        {"type": "button", "box": [530, 420, 750, 455], "bg": (16, 185, 129), "text": "💾 Submit Official Inspection Findings"}
    ],
    "data/report_screenshots/fig5_officer.png"
)

# 6. Database Visual Inspector
create_ui_image(
    "Standalone SQLite Database Visual Inspector",
    "Direct visual inspection of powerguard.db rows with photos rendered in table",
    [
        {"type": "card", "box": [30, 150, 930, 500], "title": "⚡ SQLite Database Inspector (data/powerguard.db)", "desc": "Visual table of complaints with photo thumbnails shown directly beside records"},
        {"type": "text", "pos": [50, 215], "text": "Source File: data/powerguard.db & reports_mirror.json | Total Rows: 4 (2 with photo evidence)", "color": (245, 158, 11)},
        {"type": "card", "box": [50, 250, 900, 470], "bg": (15, 23, 42), "border": (36, 53, 83)},
        {"type": "text", "pos": [70, 275], "text": "Ref ID       Evidence Photo       Category            Citizen Reporter     Assigned Officer", "color": (148, 163, 184)},
        {"type": "text", "pos": [70, 310], "text": "PG-2026-1084 [📷 exp8.png]       Direct Hooking      Pratik Mali          Pending Assignment", "color": (248, 250, 252)},
        {"type": "text", "pos": [70, 350], "text": "PG-2026-6021 [No Photo]          Direct Hooking      Rohan Deshmukh       Er. V. Deshmukh", "color": (56, 189, 248)},
        {"type": "text", "pos": [70, 390], "text": "PG-2026-5995 [📷 WhatsApp.jpg]   Meter Bypass        Citizen Informer     Pending Assignment", "color": (248, 250, 252)},
        {"type": "text", "pos": [70, 430], "text": "PG-2026-5332 [No Photo]          Sub-Metering        Citizen Informer     Er. Priya Nair", "color": (16, 185, 129)}
    ],
    "data/report_screenshots/fig6_db_inspector.png"
)
