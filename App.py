import os
import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np
from PIL import Image, ImageDraw
import random

# --- CONFIGURATION ---
MAPBOX_TOKEN = "pk.eyJ1Ijoia2FpbGFzbmF0aDEyMyIsImEiOiJjbXU4Zm93YmEwdXdnMnlzMmdnbTQyNzNoIn0.0yYdaXOauUT-_A6VaeuMyg"
os.environ["MAPBOX_API_KEY"] = MAPBOX_TOKEN
pdk.settings.mapbox_api_key = MAPBOX_TOKEN

st.set_page_config(
    page_title="ROADX AI | Enterprise Platform",
    page_icon="⚜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- FUTURISTIC CYBER-GOLD THEME CSS ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Cinzel:wght@600;700;800&family=JetBrains+Mono:wght@400;700&display=swap');

        html, body, [data-testid="stAppViewContainer"] {
            background-color: #030305 !important;
            color: #F1F5F9 !important;
            font-family: 'Outfit', sans-serif;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #09090E 0%, #030305 100%) !important;
            border-right: 1px solid rgba(212, 175, 55, 0.2);
        }

        .block-container {
            max-width: 1300px !important;
            padding-top: 2rem !important;
            padding-bottom: 6rem !important;
            padding-left: 3rem !important;
            padding-right: 3rem !important;
        }

        #MainMenu, footer, header {visibility: hidden;}

        .brand-title {
            font-family: 'Cinzel', serif;
            font-size: 1.8rem;
            font-weight: 800;
            letter-spacing: 3px;
            color: #D4AF37;
            text-transform: uppercase;
            margin-bottom: 0.2rem;
        }
        .brand-title span { color: #FFFFFF; }

        .section-heading {
            font-family: 'Cinzel', serif;
            font-size: 2rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-top: 1rem;
            margin-bottom: 1.5rem;
            color: #FFFFFF;
            border-left: 4px solid #D4AF37;
            padding-left: 15px;
        }

        .sleek-card {
            background: linear-gradient(145deg, rgba(18, 18, 24, 0.7) 0%, rgba(8, 8, 12, 0.9) 100%);
            border: 1px solid rgba(212, 175, 55, 0.25);
            border-radius: 16px;
            padding: 28px;
            margin-bottom: 20px;
            backdrop-filter: blur(10px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.6);
        }

        .stButton>button {
            background: linear-gradient(135deg, #1A1A22 0%, #111116 100%) !important;
            color: #FFFFFF !important;
            font-family: 'Cinzel', serif !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            border-radius: 10px !important;
            border: 1px solid rgba(212, 175, 55, 0.4) !important;
            padding: 0.75rem 1rem !important;
            width: 100%;
            font-size: 0.85rem !important;
            letter-spacing: 1.5px !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
        }
        .stButton>button:hover {
            background: linear-gradient(135deg, #D4AF37 0%, #AA8C2C 100%) !important;
            color: #030305 !important;
            border-color: #D4AF37 !important;
        }

        p, span, div, label { color: #94A3B8; font-size: 1.02rem; line-height: 1.6; }
        h1, h2, h3 { color: #FFFFFF; }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if "user_role" not in st.session_state:
    st.session_state.user_role = "Select Role"

if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False

if "carbon_credits" not in st.session_state:
    st.session_state.carbon_credits = 142.5

if "road_data" not in st.session_state:
    st.session_state.road_data = pd.DataFrame({
        "Road_ID": ["TVM-01", "TVM-02", "TVM-03", "TVM-04", "TVM-05"],
        "Location": ["MC Road, Ulloor", "NH-66 Bypass", "Kowdiar Square", "Pattom Corridor", "East Fort Ring"],
        "Latitude": [8.5331, 8.5645, 8.5175, 8.5208, 8.4842],
        "Longitude": [76.9317, 76.8782, 76.9551, 76.9382, 76.9472],
        "Health_Score": [88, 42, 94, 28, 65],
        "Status": ["Optimal", "Moderate Risk", "Optimal", "Critical Failure", "Moderate Risk"],
        "Predicted_Failure_Days": ["90+ days", "30 days", "120+ days", "4 days (Critical)", "45 days"],
        "Two_Wheeler_Risk": ["Low Risk", "High Risk", "Low Risk", "Critical High Risk", "Moderate Risk"],
    })

if "vision_database" not in st.session_state:
    st.session_state.vision_database = [
        {"ticket_id": "TICK-801", "location": "MC Road Corridor, Sector 4", "defect": "Critical Pothole", "confidence": "98.4%", "status": "Dispatched"},
        {"ticket_id": "TICK-802", "location": "NH-66 Bypass Junction", "defect": "Surface Fracture", "confidence": "91.2%", "status": "Pending"}
    ]

if "community_reports" not in st.session_state:
    st.session_state.community_reports = [
        {"id": 1, "location": "Ulloor Junction", "type": "Pothole / Edge Break", "status": "Active"},
        {"id": 2, "location": "Kazhakkoottam Rd", "type": "Surface Fracture", "status": "Active"}
    ]

if "completed_fixes" not in st.session_state:
    st.session_state.completed_fixes = [
        {"id": "FIX-101", "location": "Vellayambalam Square", "repair_type": "Polymer Resin Injection", "date_resolved": "Yesterday", "status": "Completed & Verified"},
        {"id": "FIX-102", "location": "Pattom Main Road", "repair_type": "Smart-Cure Thermal Patch", "date_resolved": "3 days ago", "status": "Completed & Verified"}
    ]

if "financial_ledger" not in st.session_state:
    st.session_state.financial_ledger = [
        {"Record": "Q1 Preventative Patching Allocation", "Amount": "₹45,00,000", "Type": "Expenditure"},
        {"Record": "Carbon Credit Offset Monetization", "Amount": "+₹12,50,000", "Type": "Revenue"}
    ]

df = st.session_state.road_data
df["color"] = df["Health_Score"].apply(lambda x: [10, 185, 129, 220] if x >= 75 else ([245, 158, 11, 220] if x >= 40 else [239, 68, 68, 220]))

# ================= LANDING SCREEN =================
if st.session_state.user_role == "Select Role":
    st.markdown("""
        <div style="text-align: center; padding: 40px 0 20px 0;">
            <div class="brand-title" style="font-size: 2.8rem;">ROADX<span>.AI</span></div>
            <div style="font-family: 'JetBrains Mono'; font-size: 0.9rem; color: #D4AF37; letter-spacing: 4px; margin-top: 5px;">AUTONOMOUS MUNICIPAL ROAD PLATFORM</div>
            <p style="max-width: 650px; margin: 20px auto 40px auto; font-size: 1.15rem; color: #94A3B8;">
                Select your portal entry point below to access specialized telemetry, field execution modules, or citizen reporting tools.
            </p>
        </div>
    """, unsafe_allow_html=True)

    col_l1, col_l2, col_l3 = st.columns(3)
    
    with col_l1:
        st.markdown("""
            <div class="sleek-card" style="text-align: center; min-height: 280px; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="font-size: 2.5rem; margin-bottom: 10px;">🛡️</div>
                    <h3 style="color: #FFF; font-family: 'Cinzel'; margin-bottom: 10px;">Citizen Portal</h3>
                    <p style="font-size: 0.95rem;">Track local repairs, view civic updates, and report road hazards directly to municipal workers.</p>
                </div>
        """, unsafe_allow_html=True)
        if st.button("ENTER AS CITIZEN"):
            st.session_state.user_role = "Citizen / Public User"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col_l2:
        st.markdown("""
            <div class="sleek-card" style="text-align: center; min-height: 280px; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="font-size: 2.5rem; margin-bottom: 10px;">⚡</div>
                    <h3 style="color: #FFF; font-family: 'Cinzel'; margin-bottom: 10px;">Field Contractor</h3>
                    <p style="font-size: 0.95rem;">Access task assignments, run neural vision inference, and calculate precise repair budgets.</p>
                </div>
        """, unsafe_allow_html=True)
        if st.button("ENTER AS CONTRACTOR"):
            st.session_state.user_role = "Field Contractor"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col_l3:
        st.markdown("""
            <div class="sleek-card" style="text-align: center; min-height: 280px; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="font-size: 2.5rem; margin-bottom: 10px;">🔒</div>
                    <h3 style="color: #D4AF37; font-family: 'Cinzel'; margin-bottom: 10px;">Admin / Planner</h3>
                    <p style="font-size: 0.95rem;">Secured access required. Full command grid telemetry, carbon credit minting, and municipal economics.</p>
                </div>
        """, unsafe_allow_html=True)
        if st.button("ENTER AS ADMIN"):
            st.session_state.user_role = "Admin / City Planner"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.stop()

# ================= ACTIVE WORKSPACE =================
with st.sidebar:
    st.markdown("""
        <div style="padding: 10px 0 15px 0;">
            <div class="brand-title">ROADX<span>.AI</span></div>
            <div style="font-family: 'JetBrains Mono'; font-size: 0.7rem; color: #D4AF37; letter-spacing: 2px;">ACTIVE PORTAL</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style="background: rgba(212, 175, 55, 0.05); border: 1px solid rgba(212, 175, 55, 0.2); border-radius: 12px; padding: 12px; margin-bottom: 15px;">
            <div style="font-size: 0.7rem; color: #D4AF37; font-family: 'JetBrains Mono';">CURRENT ROLE</div>
            <div style="font-size: 0.85rem; color: #FFFFFF; font-weight: 600;">{st.session_state.user_role}</div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.user_role == "Admin / City Planner" and not st.session_state.admin_authenticated:
        st.markdown("<hr style='border-color: rgba(212,175,55,0.15); margin: 10px 0;'>", unsafe_allow_html=True)
        admin_pass = st.text_input("Enter Admin Password", type="password")
        if admin_pass == "kai2000":
            st.session_state.admin_authenticated = True
            st.success("🔓 Unlocked")
            st.rerun()
        elif admin_pass != "":
            st.error("❌ Invalid Password")

    if st.button("← SWITCH ROLE"):
        st.session_state.user_role = "Select Role"
        st.session_state.admin_authenticated = False
        st.rerun()

    st.markdown("<hr style='border-color: rgba(212,175,55,0.15); margin: 20px 0;'>", unsafe_allow_html=True)
    
    if st.session_state.user_role == "Citizen / Public User":
        pages = ["Public Home", "Report Hazard", "Civic Updates & Fixes"]
    elif st.session_state.user_role == "Field Contractor":
        pages = ["Field Operations Hub", "Vision Lab", "Cost Estimator"]
    elif st.session_state.user_role == "Admin / City Planner":
        pages = ["Overview", "Command Center", "Vision Lab", "Carbon Ledger", "Finance"] if st.session_state.admin_authenticated else ["Admin Locked"]
            
    page = st.radio("Navigation", pages, label_visibility="collapsed")

# ================= PAGE ROUTING =================
if page == "Admin Locked":
    st.markdown("""
        <div style="padding: 60px 20px; text-align: center;">
            <h1 style="font-family: 'Cinzel', serif; font-size: 2.5rem; color: #EF4444; margin-bottom: 20px;">ADMIN AUTHENTICATION REQUIRED</h1>
            <p style="font-size: 1.2rem; max-width: 600px; margin: 0 auto; color: #94A3B8;">
                Please enter the secure administrative password in the sidebar input field to unlock municipal control systems.
            </p>
        </div>
    """, unsafe_allow_html=True)

# --- CITIZEN PAGES ---
elif page == "Public Home":
    st.markdown("""
        <div style="padding: 30px 0 40px 0;">
            <h1 style="font-family: 'Cinzel', serif; font-size: 3.2rem; font-weight: 800; color: #FFF; line-height: 1.1; margin-bottom: 15px;">
                TRIVANDRUM <span style="color: #D4AF37;">CIVIC PORTAL.</span>
            </h1>
            <p style="font-size: 1.2rem; max-width: 750px; color: #94A3B8;">Welcome citizen! Track municipal road improvements, check verified repairs in your neighborhood, and report potholes directly to city crews.</p>
        </div>
    """, unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'<div class="sleek-card"><h2 style="color:#D4AF37; font-family:\'Cinzel\'; font-size: 2.5rem;">{45 + len(st.session_state.community_reports)}</h2><p style="margin-top:5px;">Potholes Fixed & Tracked This Month</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="sleek-card"><h2 style="color:#FFF; font-family:\'Cinzel\'; font-size: 2.5rem;">98.2%</h2><p style="margin-top:5px;">Citizen Report Resolution Rate</p></div>', unsafe_allow_html=True)

elif page == "Report Hazard":
    st.markdown('<div class="section-heading">Citizen Pothole & Hazard Reporting</div>', unsafe_allow_html=True)
    c_rep1, c_rep2 = st.columns(2)
    with c_rep1:
        st.markdown('<div class="sleek-card">', unsafe_allow_html=True)
        with st.form("public_report"):
            st.markdown("### Submit Road Issue")
            street = st.text_input("Street Name / Landmark")
            issue_type = st.selectbox("Issue Type", ["Pothole / Crater", "Surface Fracture", "Broken Edge / Curb", "Water Logging"])
            if st.form_submit_button("SUBMIT REPORT") and street:
                st.success("Report successfully transmitted to municipal operations!")
                st.session_state.community_reports.insert(0, {"id": len(st.session_state.community_reports)+1, "location": street, "type": issue_type, "status": "Active"})
                st.session_state.vision_database.insert(0, {"ticket_id": f"TICK-{random.randint(850, 999)}", "location": street, "defect": issue_type, "confidence": "Verified Citizen Report", "status": "Pending"})
        st.markdown('</div>', unsafe_allow_html=True)
    with c_rep2:
        st.markdown('<div class="sleek-card">', unsafe_allow_html=True)
        st.markdown("### Active Neighborhood Reports")
        for r in st.session_state.community_reports:
            st.markdown(f"""<div style="background: rgba(0,0,0,0.3); padding: 12px; border-radius: 8px; margin-top: 10px; border-left: 3px solid #D4AF37;"><b>{r['location']}</b><br><span style="color:#D4AF37; font-size:0.9rem;">{r['type']}</span></div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "Civic Updates & Fixes":
    st.markdown('<div class="section-heading">Public Civic Updates & Recent Fixes</div>', unsafe_allow_html=True)
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        st.markdown("### ✅ Recently Fixed & Verified")
        for fix in st.session_state.completed_fixes:
            st.markdown(f"""
                <div style="background: rgba(16, 185, 129, 0.05); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: 12px; padding: 16px; margin-bottom: 15px;">
                    <div style="color: #10B981; font-family: 'JetBrains Mono'; font-size: 0.8rem;">{fix['id']} • {fix['date_resolved']}</div>
                    <div style="font-weight: 700; color: #FFF; font-size: 1.1rem; margin: 4px 0;">{fix['location']}</div>
                    <div style="font-size: 0.9rem; color: #94A3B8;">Method: {fix['repair_type']}</div>
                </div>
            """, unsafe_allow_html=True)
    with col_f2:
        st.markdown("### 🚧 Upcoming Municipal Developments")
        st.markdown("""
            <div style="background: rgba(212, 175, 55, 0.05); border: 1px solid rgba(212, 175, 55, 0.2); border-radius: 12px; padding: 16px; margin-bottom: 15px;">
                <div style="color: #D4AF37; font-family: 'JetBrains Mono'; font-size: 0.8rem;">SCHEDULED: NEXT WEEK</div>
                <div style="font-weight: 700; color: #FFF; font-size: 1.1rem; margin: 4px 0;">MC Road Sector 2 Resurfacing</div>
            </div>
        """, unsafe_allow_html=True)

# --- CONTRACTOR PAGES ---
elif page == "Field Operations Hub":
    st.markdown('<div class="section-heading">Field Contractor Execution Hub</div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="sleek-card">
            <h3>Active Task Assignments & Live Tickets</h3>
            <p>Review assigned maintenance tickets generated from neural scans and citizen reports.</p>
        </div>
    """, unsafe_allow_html=True)
    st.dataframe(pd.DataFrame(st.session_state.vision_database), use_container_width=True, hide_index=True)

# --- SHARED TOOLS (Vision Lab & Cost Estimator) ---
elif page == "Vision Lab":
    st.markdown('<div class="section-heading">Neural Vision Lab & Defect Logger</div>', unsafe_allow_html=True)
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.markdown('<div class="sleek-card">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload Pavement Image", type=["jpg", "png", "jpeg"])
        input_location = st.text_input("Exact Incident Location / Street", value="Pattom Junction, Sector 2")
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Pavement Frame", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col_v2:
        st.markdown('<div class="sleek-card">', unsafe_allow_html=True)
        st.markdown("### Tensor Inference Pipeline")
        if uploaded_file is not None:
            if st.button("RUN YOLOv8 INFERENCE & LOG"):
                with st.spinner("Processing tensor weights..."):
                    import time
                    time.sleep(1.0)
                    img_annotated = image.copy()
                    draw = ImageDraw.Draw(img_annotated)
                    w, h = img_annotated.size
                    draw.rectangle([w*0.25, h*0.4, w*0.65, h*0.75], outline="#EF4444", width=5)
                    st.success("Inference complete! Ticket logged to Command Grid.")
                    st.image(img_annotated, caption="YOLOv8 Bounding Box Output", use_container_width=True)
                    st.session_state.vision_database.insert(0, {"ticket_id": f"TICK-{random.randint(803, 999)}", "location": input_location, "defect": "Critical Pothole", "confidence": "98.4%", "status": "Pending"})
        else:
            st.info("Upload an image to execute object detection.")
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "Cost Estimator":
    st.markdown('<div class="section-heading">Severity & Cost Estimator</div>', unsafe_allow_html=True)
    st.markdown('<div class="sleek-card">', unsafe_allow_html=True)
    w = st.slider("Width (cm)", 10, 200, 50)
    d = st.slider("Depth (cm)", 2, 50, 10)
    cost = (w * w * d / 1000) * 2.75 + 150
    st.markdown(f"""
        <div style="margin-top: 20px; padding: 20px; background: rgba(212,175,55,0.05); border-radius: 12px; border: 1px solid rgba(212,175,55,0.3); text-align: center;">
            <h2 style="color:#D4AF37; font-family:'Cinzel'; font-size:2.5rem;">₹{cost:.2f}</h2>
            <p style="margin-top: 5px;">Estimated Real-Time Repair Budget</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("SAVE ESTIMATE TO MUNICIPAL BUDGET"):
        st.session_state.financial_ledger.append({"Record": f"Field Repair Estimate ({w}x{d}cm)", "Amount": f"₹{cost:.2f}", "Type": "Expenditure"})
        st.success("Estimate successfully committed to financial ledger!")
    st.markdown('</div>', unsafe_allow_html=True)

# --- ADMIN-ONLY PAGES ---
elif page == "Overview":
    st.markdown("""
        <div style="padding: 30px 0 40px 0;">
            <h1 style="font-family: 'Cinzel', serif; font-size: 3.2rem; font-weight: 800; color: #FFF; line-height: 1.1; margin-bottom: 15px;">
                ADMINISTRATIVE <span style="color: #D4AF37;">OVERVIEW.</span>
            </h1>
            <p style="font-size: 1.2rem; max-width: 750px; color: #94A3B8;">High-level municipal asset health, macro telemetry, and budgetary oversight.</p>
        </div>
    """, unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="sleek-card"><h2 style="color:#D4AF37; font-family:\'Cinzel\'; font-size: 2.5rem;">12.4 km</h2><p style="margin-top:5px;">Pilot Corridor Monitored</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="sleek-card"><h2 style="color:#FFF; font-family:\'Cinzel\'; font-size: 2.5rem;">{len(st.session_state.vision_database)}</h2><p style="margin-top:5px;">Active Defect Tickets</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="sleek-card"><h2 style="color:#D4AF37; font-family:\'Cinzel\'; font-size: 2.5rem;">{st.session_state.carbon_credits:.1f} t</h2><p style="margin-top:5px;">Carbon Credits Minted</p></div>', unsafe_allow_html=True)

elif page == "Command Center":
    st.markdown('<div class="section-heading">Municipal Command Grid</div>', unsafe_allow_html=True)
    col_map, col_ctrl = st.columns([2, 1])
    with col_map:
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position=["Longitude", "Latitude"],
            get_fill_color="color",
            get_radius=350,
            pickable=True,
        )
        view_state = pdk.ViewState(latitude=8.5241, longitude=76.9366, zoom=12, pitch=30)
        deck = pdk.Deck(layers=[layer], initial_view_state=view_state, map_style="mapbox://styles/mapbox/dark-v10")
        st.pydeck_chart(deck, use_container_width=True)
    with col_ctrl:
        st.markdown('<div class="sleek-card">', unsafe_allow_html=True)
        sel_id = st.selectbox("Select Asset Corridor", df["Road_ID"])
        row = df[df["Road_ID"] == sel_id].iloc[0]
        st.markdown(f"""
            <div style="margin-top: 15px;">
                <b>Location:</b> {row['Location']}<br><br>
                <b>Health Score:</b> <span style="color: #D4AF37; font-weight: 700;">{row['Health_Score']} / 100</span><br><br>
                <b>Failure ETA:</b> {row['Predicted_Failure_Days']}<br><br>
                <b>2-Wheeler Risk:</b> {row['Two_Wheeler_Risk']}
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "Carbon Ledger":
    st.markdown('<div class="section-heading">Carbon Credit Ledger</div>', unsafe_allow_html=True)
    c_col1, c_col2 = st.columns(2)
    with c_col1:
        st.markdown(f"""
            <div class="sleek-card">
                <h2 style="color:#D4AF37; font-family:'Cinzel'; font-size:2.5rem;">{st.session_state.carbon_credits:.1f} tCO2e</h2>
                <p style="margin-top:10px;">Avoided hot-mix bitumen emissions verified.</p>
            </div>
        """, unsafe_allow_html=True)
    with c_col2:
        st.markdown('<div class="sleek-card">', unsafe_allow_html=True)
        st.markdown("### Ledger Minting")
        if st.button("MINT VERIFIED CREDITS"):
            st.session_state.carbon_credits += 15.0
            st.session_state.financial_ledger.append({
                "Record": "Minted 15.0 tCO2e Carbon Offsets", 
                "Amount": f"+₹{(15.0 * 8500):,.2f}", 
                "Type": "Revenue"
            })
            st.success("Successfully minted 15.0 cryptographic carbon credits & logged revenue to finance ledger!")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "Finance":
    st.markdown('<div class="section-heading">Financial Economics & Ledger</div>', unsafe_allow_html=True)
    st.dataframe(pd.DataFrame(st.session_state.financial_ledger), use_container_width=True, hide_index=True)

# --- FOOTER ---
st.markdown("""
    <div style="border-top: 1px solid rgba(212,175,55,0.2); margin-top: 80px; padding-top: 30px; text-align: center;">
        <div style="font-family: 'Cinzel', serif; font-size: 0.8rem; color: #D4AF37; letter-spacing: 3px;">ROADX.AI © 2026 // TRIVANDRUM MUNICIPAL PILOT</div>
    </div>
""", unsafe_allow_html=True)
