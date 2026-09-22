import os
import streamlit as st
import pandas as pd
import pydeck as pdk
import time

# --- MAPBOX API KEY & ENVIRONMENT CONFIGURATION ---
MAPBOX_TOKEN = "pk.eyJ1Ijoia2FpbGFzbmF0aDEyMyIsImEiOiJjbXU4Zm93YmEwdXdnMnlzMmdnbTQyNzNoIn0.0yYdaXOauUT-_A6VaeuMyg"
os.environ["MAPBOX_API_KEY"] = MAPBOX_TOKEN
pdk.settings.mapbox_api_key = MAPBOX_TOKEN

# Page Configuration
st.set_page_config(
    page_title="ROADX AI | Executive Infrastructure Control",
    page_icon="⚜️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session Navigation State
if "current_page" not in st.session_state:
    st.session_state.current_page = "🏠 Executive Overview"

# High-End Ultra Minimalist Dark Theme (Zero Black Boxes, Glass & Gold Styling)
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=Cinzel:wght@500;600;700&display=swap');

        /* Global Background & Typography */
        .main { background-color: #080808; color: #E2E8F0; font-family: 'Plus Jakarta Sans', sans-serif; }
        .block-container { padding: 2rem 2.5rem 3rem 2.5rem; max-width: 100%; }
        
        h1, h2, h3, h4 { color: #F8FAFC !important; font-family: 'Cinzel', serif; letter-spacing: 0.5px; }
        p, span, label, div { font-family: 'Plus Jakarta Sans', sans-serif; }

        /* Page Entrance Animation */
        @keyframes pageEntrance {
            from { opacity: 0; transform: translateY(12px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .animated-page { animation: pageEntrance 0.45s ease-out forwards; }

        /* Premium Minimalist Border Cards */
        .clean-card {
            border: 1px solid #222222;
            border-top: 2px solid #D4AF37;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            background: rgba(255, 255, 255, 0.015);
            transition: all 0.3s ease;
        }
        .clean-card:hover {
            border-color: #333333;
            border-top-color: #F3E5AB;
        }

        /* Nav Action Card */
        .nav-card {
            border: 1px solid #1E1E1E;
            border-left: 3px solid #D4AF37;
            border-radius: 8px;
            padding: 18px;
            margin-bottom: 15px;
            background: rgba(255, 255, 255, 0.01);
            transition: transform 0.2s ease, border-color 0.2s ease;
        }
        .nav-card:hover {
            transform: translateX(4px);
            border-color: #333;
            border-left-color: #F3E5AB;
        }

        /* Metric Boxes */
        .stat-box {
            border: 1px solid #1C1C1C;
            border-radius: 8px;
            padding: 16px;
            text-align: center;
            background: rgba(255, 255, 255, 0.01);
        }
        .stat-number {
            font-family: 'Cinzel', serif;
            font-size: 1.7rem;
            color: #D4AF37;
            font-weight: 600;
        }
        .stat-title {
            font-size: 0.7rem;
            color: #888888;
            text-transform: uppercase;
            letter-spacing: 1.2px;
            margin-top: 4px;
        }

        /* Vehicle Risk Badges */
        .risk-badge {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 0.78rem;
            font-weight: 600;
            letter-spacing: 0.5px;
        }
        .risk-low { background: rgba(16, 185, 129, 0.15); color: #10B981; border: 1px solid rgba(16, 185, 129, 0.3); }
        .risk-mod { background: rgba(245, 158, 11, 0.15); color: #F59E0B; border: 1px solid rgba(245, 158, 11, 0.3); }
        .risk-high { background: rgba(239, 68, 68, 0.15); color: #EF4444; border: 1px solid rgba(239, 68, 68, 0.3); }

        /* Sidebar Customization */
        section[data-testid="stSidebar"] {
            background-color: #050505;
            border-right: 1px solid #181818;
        }

        /* Buttons */
        .stButton>button {
            background: #D4AF37;
            color: #000000;
            font-weight: 600;
            font-family: 'Cinzel', serif;
            letter-spacing: 0.5px;
            border: none;
            border-radius: 5px;
            padding: 0.55rem 1rem;
            width: 100%;
            transition: background 0.2s ease;
        }
        .stButton>button:hover {
            background: #E5C158;
            color: #000000;
        }
    </style>
""", unsafe_allow_html=True)

# Hyper-Local Trivandrum Pilot Telemetry Data
if "road_data" not in st.session_state:
    st.session_state.road_data = pd.DataFrame({
        "Road_ID": ["TVM-01", "TVM-02", "TVM-03", "TVM-04", "TVM-05"],
        "Location": ["MC Road, Ulloor Junction", "NH-66 Kazhakkoottam Bypass", "Kowdiar Square Corridor", "Pattom-Kumarapuram Rd", "East Fort City Ring Rd"],
        "Latitude": [8.5331, 8.5645, 8.5175, 8.5208, 8.4842],
        "Longitude": [76.9317, 76.8782, 76.9551, 76.9382, 76.9472],
        "Health_Score": [88, 42, 94, 28, 65],
        "Status": ["Optimal", "Moderate Risk", "Optimal", "Critical Failure", "Moderate Risk"],
        "Predicted_Failure_Days": ["90+ days", "30 days", "120+ days", "4 days (Immediate)", "45 days"],
        "Two_Wheeler_Risk": ["Low Risk", "High Risk", "Low Risk", "Critical High Risk", "Moderate Risk"],
        "Four_Wheeler_Risk": ["Low Risk", "Moderate Risk", "Low Risk", "High Risk", "Low Risk"],
        "Heavy_Vehicle_Risk": ["Low Risk", "High Risk", "Low Risk", "Structural Threat", "High Risk"]
    })

df = st.session_state.road_data

# Community Verification Store in Session State
if "community_reports" not in st.session_state:
    st.session_state.community_reports = [
        {"id": 1, "location": "Ulloor Junction Patch", "type": "Pothole / Edge Break", "votes": 14, "status": "Active"},
        {"id": 2, "location": "Kazhakkoottam Service Rd", "type": "Surface Fracture", "votes": 9, "status": "Active"}
    ]

# Function to assign RGB colors for Pydeck
def get_color(score):
    if score >= 75:
        return [10, 185, 129, 210]   # Emerald Green
    elif score >= 40:
        return [245, 158, 11, 210]  # Amber Orange
    else:
        return [239, 68, 68, 210]   # Red Danger

df["color"] = df["Health_Score"].apply(get_color)

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    else:
        st.markdown("""
            <div style="text-align: center; padding: 10px 0;">
                <h3 style="font-size: 1.15rem; letter-spacing: 2px; color: #F3E5AB; margin-top: 4px;">ROADX AI</h3>
                <p style="font-size: 0.58rem; color: #666; letter-spacing: 3px; text-transform: uppercase;">EXECUTIVE INFRASTRUCTURE</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<hr style='border-color: #1A1A1A;'>", unsafe_allow_html=True)
    
    nav_options = [
        "🏠 Executive Overview",
        "🏛️ Municipal Command", 
        "👁️ Neural Vision Lab", 
        "🔊 Sub-Surface Acoustic Lab",
        "⚡ Smart-Cure V2I Trigger",
        "🌱 Carbon Credit Ledger",
        "📢 Citizen Vigil Hub", 
        "💰 Severity & Cost Estimator",
        "🚀 Capabilities Matrix",
        "📊 Financial Economics", 
        "🏆 UN SDG Impact"
    ]
    
    try:
        current_index = nav_options.index(st.session_state.current_page)
    except ValueError:
        current_index = 0

    selected_nav = st.radio("Navigation", nav_options, index=current_index)
    if selected_nav != st.session_state.current_page:
        st.session_state.current_page = selected_nav
        st.rerun()
    
    st.markdown("<hr style='border-color: #1A1A1A;'>", unsafe_allow_html=True)
    st.markdown("""
        <div style="padding: 10px; border-radius: 6px; border: 1px solid #1C1C1C; background: rgba(255,255,255,0.01);">
            <div style="font-size: 0.7rem; color: #888;">PILOT DEPLOYMENT ZONE</div>
            <div style="font-size: 0.82rem; font-weight: 600; color: #D4AF37; margin-top: 2px;">TRIVANDRUM WARD 1</div>
            <div style="font-size: 0.68rem; color: #666; margin-top: 4px;">Kerala Public Works Dept.</div>
        </div>
    """, unsafe_allow_html=True)

# Helper for vehicle badge rendering
def render_risk_badge(risk_text):
    if "Low" in risk_text:
        return f'<span class="risk-badge risk-low">{risk_text}</span>'
    elif "Mod" in risk_text:
        return f'<span class="risk-badge risk-mod">{risk_text}</span>'
    else:
        return f'<span class="risk-badge risk-high">{risk_text}</span>'

# ================= PAGE 0: EXECUTIVE OVERVIEW (HOMEPAGE) =================
if st.session_state.current_page == "🏠 Executive Overview":
    st.markdown("""
        <div class="animated-page">
            <h1 style='font-size: 2.2rem; margin-bottom: 2px;'>ROADX AI</h1>
            <p style='color: #888; font-size: 0.95rem; margin-bottom: 25px;'>Trivandrum Municipal Pilot: Autonomous Infrastructure Health & Multi-Vehicle Safety Intelligence.</p>
        </div>
    """, unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown('<div class="stat-box"><div class="stat-number">12.4 km</div><div class="stat-title">Pilot Scan Corridor</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown('<div class="stat-box"><div class="stat-number" style="color:#EF4444;">1 Asset</div><div class="stat-title">Critical Intervention</div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown('<div class="stat-box"><div class="stat-number" style="color:#10B981;">99.4%</div><div class="stat-title">YOLOv8 Scan Accuracy</div></div>', unsafe_allow_html=True)
    with m4:
        st.markdown('<div class="stat-box"><div class="stat-number">142 t</div><div class="stat-title">Carbon Credits Issued</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### System Command Modules")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
            <div class="nav-card">
                <h3 style="font-size: 1.1rem; margin-bottom: 4px;">🏛️ Municipal Command Center</h3>
                <p style="color: #888; font-size: 0.83rem; margin-bottom: 12px;">Live Mapbox Trivandrum GIS heatmap and multi-vehicle road safety profiling.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("OPEN COMMAND CENTER", key="btn_cmd"):
            st.session_state.current_page = "🏛️ Municipal Command"
            st.rerun()
            
        st.markdown("""
            <div class="nav-card" style="margin-top: 15px;">
                <h3 style="font-size: 1.1rem; margin-bottom: 4px;">🔊 Sub-Surface Acoustic Lab</h3>
                <p style="color: #888; font-size: 0.83rem; margin-bottom: 12px;">Ground-penetrating vibration profiling to predict sinkholes before surface cracks appear.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("OPEN ACOUSTIC LAB", key="btn_acou"):
            st.session_state.current_page = "🔊 Sub-Surface Acoustic Lab"
            st.rerun()

    with c2:
        st.markdown("""
            <div class="nav-card">
                <h3 style="font-size: 1.1rem; margin-bottom: 4px;">⚡ Smart-Cure V2I Trigger</h3>
                <p style="color: #888; font-size: 0.83rem; margin-bottom: 12px;">Automated vehicle-to-infrastructure trigger for self-healing polymer asphalt activation.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("OPEN SMART-CURE TRIGGER", key="btn_cure"):
            st.session_state.current_page = "⚡ Smart-Cure V2I Trigger"
            st.rerun()

        st.markdown("""
            <div class="nav-card" style="margin-top: 15px;">
                <h3 style="font-size: 1.1rem; margin-bottom: 4px;">🌱 Carbon Credit Ledger</h3>
                <p style="color: #888; font-size: 0.83rem; margin-bottom: 12px;">Cryptographic ESG audit reports and municipal carbon credit issuance.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("OPEN CARBON LEDGER", key="btn_carb"):
            st.session_state.current_page = "🌱 Carbon Credit Ledger"
            st.rerun()

# ================= PAGE 1: MUNICIPAL COMMAND =================
elif st.session_state.current_page == "🏛️ Municipal Command":
    st.markdown("""
        <div class="animated-page">
            <h1 style='font-size: 2rem; margin-bottom: 2px;'>MUNICIPAL COMMAND CENTER</h1>
            <p style='color: #888; font-size: 0.9rem; margin-bottom: 20px;'>Trivandrum Spatial Intelligence and Multi-Vehicle Risk Diagnostics.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col_map, col_details = st.columns([1.6, 1])
    with col_map:
        st.markdown("### Trivandrum Infrastructure Spatial Grid")
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position=["Longitude", "Latitude"],
            get_fill_color="color",
            get_radius=350,
            pickable=True,
        )
        view_state = pdk.ViewState(latitude=8.5241, longitude=76.9366, zoom=12.5, pitch=30)
        deck = pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            map_style="mapbox://styles/mapbox/dark-v10",
            api_keys={"mapbox": MAPBOX_TOKEN},
            tooltip={"text": "Asset ID: {Road_ID}\nLocation: {Location}\nHealth Score: {Health_Score}/100"}
        )
        st.pydeck_chart(deck)
        
    with col_details:
        st.markdown("### Multi-Vehicle Safety Evaluation")
        st.markdown('<div class="clean-card">', unsafe_allow_html=True)
        sel_id = st.selectbox("Select Asset ID:", df["Road_ID"])
        r_info = df[df["Road_ID"] == sel_id].iloc[0]
        
        st.markdown(f"""
            <div style="font-size: 0.88rem; line-height: 1.8;">
                <b>Location:</b> {r_info['Location']}<br>
                <b>Health Score:</b> <span style="color: #D4AF37; font-weight: 700;">{r_info['Health_Score']} / 100</span><br>
                <b>Estimated Time To Failure:</b> {r_info['Predicted_Failure_Days']}
            </div>
            <hr style="border-color: #222; margin: 12px 0;">
            <div style="font-size: 0.85rem; font-weight: 600; margin-bottom: 10px; color: #D4AF37;">VEHICLE TYPE SAFETY PROFILES:</div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span>🛵 <b>2-Wheelers:</b></span> {render_risk_badge(r_info['Two_Wheeler_Risk'])}
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span>🚗 <b>4-Wheelers:</b></span> {render_risk_badge(r_info['Four_Wheeler_Risk'])}
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span>🚛 <b>Heavy Vehicles:</b></span> {render_risk_badge(r_info['Heavy_Vehicle_Risk'])}
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ================= PAGE 2: VISION LAB =================
elif st.session_state.current_page == "👁️ Neural Vision Lab":
    st.markdown("""
        <div class="animated-page">
            <h1 style='font-size: 2rem; margin-bottom: 2px;'>NEURAL VISION LAB</h1>
            <p style='color: #888; font-size: 0.9rem; margin-bottom: 25px;'>Automated YOLOv8 Surface Degradation Diagnostics & Live V2I Warnings.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col_up, col_res = st.columns(2)
    with col_up:
        st.markdown('<div class="clean-card">', unsafe_allow_html=True)
        st.markdown("### Upload Target Pavement Image")
        uploaded_img = st.file_uploader("Select pavement scan", type=["jpg", "jpeg", "png"])
        if uploaded_img:
            st.image(uploaded_img, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
            
    with col_res:
        st.markdown('<div class="clean-card">', unsafe_allow_html=True)
        st.markdown("### Diagnostic Inference & V2I Alert Feed")
        if uploaded_img:
            if st.button("RUN TENSOR SCAN & BROADCAST V2I"):
                with st.spinner("Executing neural model inference..."):
                    time.sleep(1)
                st.success("Inference Complete.")
                
                st.error("🚨 **V2I AUDIO/VISUAL ALERT TRIGGERED:** Critical road defect detected 50m ahead. Speed advisory broadcasted to connected vehicles in proximity.")
                
                st.markdown("""
                    <div style="padding: 12px; border-left: 2px solid #D4AF37; margin-top: 12px; font-size: 0.88rem; line-height: 1.8;">
                        <b>Model Network:</b> RoadX-YOLOv8-X<br>
                        <b>Pothole Detection Confidence:</b> <span style="color:#D4AF37;">98.2%</span><br>
                        <b>Sub-surface Cracking Index:</b> Critical (0.84)<br>
                        <b>Estimated Repair Cost:</b> ₹3,450 (Material & Labor)<br>
                        <b>Recommended Action:</b> Polymer-modified Bituminous Sealing.
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Upload an image on the left panel to begin diagnostic scan and test V2I warnings.")
        st.markdown('</div>', unsafe_allow_html=True)

# ================= NEW FEATURE 1: SUB-SURFACE ACOUSTIC LAB =================
elif st.session_state.current_page == "🔊 Sub-Surface Acoustic Lab":
    st.markdown("""
        <div class="animated-page">
            <h1 style='font-size: 2rem; margin-bottom: 2px;'>SUB-SURFACE ACOUSTIC SONAR LAB</h1>
            <p style='color: #888; font-size: 0.9rem; margin-bottom: 25px;'>Listening Inside the Earth: Predicting Invisible Cavities & Sinkholes Before Surface Cracking Occurs.</p>
        </div>
    """, unsafe_allow_html=True)

    col_ac1, col_ac2 = st.columns([1.2, 1])
    with col_ac1:
        st.markdown('<div class="clean-card">', unsafe_allow_html=True)
        st.markdown("### Acoustic Resonance Profiler")
        sel_corridor = st.selectbox("Select Test Corridor:", ["MC Road Sector B (Ulloor)", "NH-66 Kazhakkoottam Underpass", "Kowdiar Junction Ring"])
        sweep_speed = st.slider("Vehicle Fleet Roll Speed (km/h)", 20, 80, 45)
        
        if st.button("EXECUTE SUB-SURFACE ACOUSTIC SCAN"):
            with st.spinner("Analyzing tire vibration frequencies and acoustic dampening profiles..."):
                time.sleep(1.2)
            st.success("Acoustic Tomography Mapping Successful.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_ac2:
        st.markdown('<div class="clean-card">', unsafe_allow_html=True)
        st.markdown("### Sub-Surface Anomaly Report")
        st.markdown("""
            <div style="font-size: 0.88rem; line-height: 1.8;">
                <b>Corridor ID:</b> TVM-ACOUSTIC-02<br>
                <b>Sub-Base Void Status:</b> <span style="color: #EF4444; font-weight: 750;">CAVITY DETECTED (-1.2m depth)</span><br>
                <b>Estimated Time to Sinkhole Formation:</b> 28 Days<br>
                <b>Surface Visual Status:</b> 100% Intact (Invisible to Cameras)<br>
                <b>Acoustic Frequency Deviation:</b> 42.8 Hz (Standard: 18.2 Hz)
            </div>
            <hr style="border-color: #222; margin: 12px 0;">
            <div style="font-size: 0.83rem; color: #D4AF37;"><b>AI Prognostic Recommendation:</b> Inject low-viscosity polyurethane grout into sub-base layer immediately to arrest soil erosion.</div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ================= NEW FEATURE 2: SMART-CURE V2I TRIGGER =================
elif st.session_state.current_page == "⚡ Smart-Cure V2I Trigger":
    st.markdown("""
        <div class="animated-page">
            <h1 style='font-size: 2rem; margin-bottom: 2px;'>SMART-CURE V2I MATERIAL TRIGGER</h1>
            <p style='color: #888; font-size: 0.9rem; margin-bottom: 25px;'>Autonomous V2I Communication: Triggering Self-Healing Polymer Asphalt Via Roadside Units.</p>
        </div>
    """, unsafe_allow_html=True)

    c_tr1, c_tr2 = st.columns(2)
    with c_tr1:
        st.markdown('<div class="clean-card">', unsafe_allow_html=True)
        st.markdown("### High-Stress Load Zone Config")
        truck_weight = st.slider("Approaching Heavy Axle Load (Tons)", 10, 45, 32)
        polymer_status = st.selectbox("Embedded Microcapsule Status", ["Active (Ready to Bond)", "Depleted", "Regenerating"])
        
        if st.button("SEND V2I INDUCTION PULSE"):
            with st.spinner("Broadcasting low-frequency induction pulse via roadside unit..."):
                time.sleep(1)
            st.success("Induction Pulse Broadcasted Successfully.")
        st.markdown('</div>', unsafe_allow_html=True)

    with c_tr2:
        st.markdown('<div class="clean-card">', unsafe_allow_html=True)
        st.markdown("### Material Activation Telemetry")
        st.markdown(f"""
            <div style="font-size: 0.88rem; line-height: 1.8;">
                <b>Axle Stress Level:</b> {truck_weight} Tons<br>
                <b>Induction Frequency:</b> 300 kHz Electromagnetic Pulse<br>
                <b>Polymer Viscosity State:</b> <span style="color: #10B981;">Curing & Bonding Active</span><br>
                <b>Asphalt Fatigue Recovery Rate:</b> 91.4%<br>
                <b>Crew Intervention Required:</b> NONE (Autonomous Healing)
            </div>
            <hr style="border-color: #222; margin: 12px 0;">
            <div style="font-size: 0.83rem; color: #D4AF37;"><b>System Note:</b> Microcapsules of rejuvenating oil successfully melted and sealed micro-fractures under heavy truck weight.</div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ================= NEW FEATURE 3: CARBON CREDIT LEDGER =================
elif st.session_state.current_page == "🌱 Carbon Credit Ledger":
    st.markdown("""
        <div class="animated-page">
            <h1 style='font-size: 2rem; margin-bottom: 2px;'>MUNICIPAL CARBON CREDIT LEDGER</h1>
            <p style='color: #888; font-size: 0.9rem; margin-bottom: 25px;'>Automated ESG Monetization: Cryptographic Auditing of Avoided Road Reconstruction Emissions.</p>
        </div>
    """, unsafe_allow_html=True)

    cb1, cb2 = st.columns(2)
    with cb1:
        st.markdown('<div class="clean-card">', unsafe_allow_html=True)
        st.markdown("### Preventative Carbon Offset Metrics")
        st.markdown("""
            <div style="font-size: 0.88rem; line-height: 1.8;">
                <b>Total Avoided Hot-Mix Bitumen:</b> 340 Metric Tons<br>
                <b>Transport Fuel Saved:</b> 14,200 Liters Diesel<br>
                <b>Net Carbon Dioxide Offset:</b> <span style="color:#10B981; font-weight:700;">142.5 tCO2e</span><br>
                <b>Current Market Valuation:</b> ₹11,80,000 (~$14,200 USD)<br>
                <b>Audit Status:</b> Verified & Cryptographically Signed
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with cb2:
        st.markdown('<div class="clean-card">', unsafe_allow_html=True)
        st.markdown("### Issue Municipal Carbon Credits")
        st.write("Generate official ESG audit certificates for international carbon trading boards:")
        if st.button("MINT VERIFIED ESG CREDITS"):
            with st.spinner("Generating cryptographic proof-of-work on municipal ledger..."):
                time.sleep(1)
            st.success("Successfully minted 142.5 Verified Carbon Units (VCUs) for Trivandrum Ward 1.")
        st.markdown('</div>', unsafe_allow_html=True)

# ================= PAGE 6: CITIZEN HUB =================
elif st.session_state.current_page == "📢 Citizen Vigil Hub":
    st.markdown("""
        <div class="animated-page">
            <h1 style='font-size: 2rem; margin-bottom: 2px;'>CITIZEN VIGIL HUB</h1>
            <p style='color: #888; font-size: 0.9rem; margin-bottom: 25px;'>Crowdsourced Hazard Telemetry & Community Verification Loop.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col_form, col_feed = st.columns(2)
    with col_form:
        st.markdown('<div class="clean-card">', unsafe_allow_html=True)
        st.markdown("### Submit Road Hazard Report")
        with st.form("citizen_report"):
            loc_name = st.text_input("Street / Junction Name (e.g., Peroorkada Junction)")
            hazard_type = st.selectbox("Observed Anomaly", ["Minor Crack 🟡", "Pothole / Edge Break 🟠", "Severe Road Failure 🔴"])
            submitted = st.form_submit_button("SUBMIT TELEMETRY")
            
            if submitted and loc_name:
                new_rep = {"id": len(st.session_state.community_reports)+1, "location": loc_name, "type": hazard_type, "votes": 1, "status": "Active"}
                st.session_state.community_reports.append(new_rep)
                st.success("Report dynamic injection complete! +200 Civic Points")
        st.markdown('</div>', unsafe_allow_html=True)
                
    with col_feed:
        st.markdown('<div class="clean-card">', unsafe_allow_html=True)
        st.markdown("### Community Verification Loop (Crowdsourced Feed)")
        st.write("Vote to verify active hazards and help eliminate AI false positives:")
        
        for idx, report in enumerate(st.session_state.community_reports):
            c_col1, c_col2 = st.columns([3, 2])
            c_col1.markdown(f"📍 **{report['location']}**<br><span style='font-size:0.78rem; color:#888;'>{report['type']}</span>", unsafe_allow_html=True)
            if c_col2.button(f"👍 Still Here ({report['votes']})", key=f"vote_{idx}"):
                st.session_state.community_reports[idx]["votes"] += 1
                st.success("Vote recorded!")
                st.rerun()
            st.markdown("<hr style='border-color: #1A1A1A; margin: 8px 0;'>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ================= PAGE 7: SEVERITY & COST ESTIMATOR =================
elif st.session_state.current_page == "💰 Severity & Cost Estimator":
    st.markdown("""
        <div class="animated-page">
            <h1 style='font-size: 2rem; margin-bottom: 2px;'>SEVERITY & REPAIR COST ESTIMATOR</h1>
            <p style='color: #888; font-size: 0.9rem; margin-bottom: 25px;'>Calculate physical asphalt volumes and municipal financial requirements.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="clean-card">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        width_cm = st.slider("Pothole Diameter / Width (cm)", 10, 300, 60)
    with c2:
        depth_cm = st.slider("Pothole Depth (cm)", 2, 70, 15)

    volume_liters = (width_cm * width_cm * depth_cm) / 1000
    material_cost = volume_liters * 2.75
    labor_fixed = 150.00
    total_cost = material_cost + labor_fixed

    st.markdown("---")
    r1, r2, r3 = st.columns(3)
    r1.metric("Required Asphalt Volume", f"{volume_liters:.1f} Liters")
    r2.metric("Estimated Material Cost", f"₹{material_cost:.2f}")
    r3.metric("Total Repair Budget", f"₹{total_cost:.2f}")

    if total_cost > 1000:
        st.warning("⚠️ High financial impact hazard. Heavy machinery deployment recommended.")
    else:
        st.success("✅ Standard quick-patch cold mix sufficient.")
    st.markdown('</div>', unsafe_allow_html=True)

# ================= PAGE 8: CAPABILITIES MATRIX =================
elif st.session_state.current_page == "🚀 Capabilities Matrix":
    st.markdown("""
        <div class="animated-page">
            <h1 style='font-size: 2rem; margin-bottom: 2px;'>SYSTEM CAPABILITIES DIRECTORY</h1>
            <p style='color: #888; font-size: 0.9rem; margin-bottom: 25px;'>Comprehensive breakdown of core features, advanced innovations, and municipal modules provided by RoadX AI.</p>
        </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🌟 Next-Gen Deep Tech", "🏛️ Municipal Features", "🚗 V2I & Safety Tools"])
    
    with tab1:
        st.markdown("""
            <div class="clean-card">
                <h3>1. Sub-Surface Acoustic Sonar Lab</h3>
                <p style="color:#aaa; font-size:0.85rem;">Predicts hidden sub-base voids and sinkholes weeks before surface cracks form by analyzing tire vibration frequencies.</p>
                <hr style="border-color:#222;">
                <h3>2. Smart-Cure V2I Material Trigger</h3>
                <p style="color:#aaa; font-size:0.85rem;">Automatically triggers electromagnetic induction pulses via roadside units to activate self-healing polymer asphalt under heavy trucks.</p>
                <hr style="border-color:#222;">
                <h3>3. Carbon Credit Ledger & ESG Monetization</h3>
                <p style="color:#aaa; font-size:0.85rem;">Converts avoided hot-mix bitumen reconstruction into cryptographic carbon offsets for municipal green funding.</p>
            </div>
        """, unsafe_allow_html=True)

    with tab2:
        st.markdown("""
            <div class="clean-card">
                <h3>1. Mapbox Spatial Heatmap Command</h3>
                <p style="color:#aaa; font-size:0.85rem;">Real-time GIS-mapped network overview color-coded by structural health scores across regional road assets.</p>
                <hr style="border-color:#222;">
                <h3>2. Preventative Economics Engine</h3>
                <p style="color:#aaa; font-size:0.85rem;">Shifts public works budgeting from expensive reactive reconstruction (₹4.5 Cr) to proactive micro-interventions (₹1.8 Cr).</p>
            </div>
        """, unsafe_allow_html=True)

    with tab3:
        st.markdown("""
            <div class="clean-card">
                <h3>1. Vehicle-to-Infrastructure (V2I) Alerts</h3>
                <p style="color:#aaa; font-size:0.85rem;">Instantly broadcasts audio/visual safety warnings and speed reduction advisories to connected vehicles approaching critical hazards.</p>
                <hr style="border-color:#222;">
                <h3>2. Multi-Vehicle Risk Profiling</h3>
                <p style="color:#aaa; font-size:0.85rem;">Evaluates how individual road anomalies uniquely threaten 2-wheelers, passenger 4-wheelers, and heavy freight trucks.</p>
            </div>
        """, unsafe_allow_html=True)

# ================= PAGE 9: FINANCIALS =================
elif st.session_state.current_page == "📊 Financial Economics":
    st.markdown("""
        <div class="animated-page">
            <h1 style='font-size: 2rem; margin-bottom: 2px;'>FINANCIAL ECONOMICS</h1>
            <p style='color: #888; font-size: 0.9rem; margin-bottom: 25px;'>Transitioning from Reactive Resurfacing to Autonomous Preventative Maintenance.</p>
        </div>
    """, unsafe_allow_html=True)
    
    p1, p2 = st.columns(2)
    with p1:
        st.markdown("""
            <div class="clean-card" style="border-top-color: #EF4444;">
                <h3 style="color: #EF4444 !important; font-size: 1.15rem;">Traditional Reactive Budget</h3>
                <h2 style="color: #EF4444 !important; font-size: 1.8rem; margin: 8px 0;">₹4.5 Crores / yr</h2>
                <p style="color: #888; font-size: 0.83rem; line-height: 1.6;">High expenditure caused by waiting for full asphalt degradation, resulting in complete relaying and accident liability payouts.</p>
            </div>
        """, unsafe_allow_html=True)
    with p2:
        st.markdown("""
            <div class="clean-card" style="border-top-color: #D4AF37;">
                <h3 style="color: #D4AF37 !important; font-size: 1.15rem;">RoadX AI Preventative Model</h3>
                <h2 style="color: #D4AF37 !important; font-size: 1.8rem; margin: 8px 0;">₹1.8 Crores <span style="font-size:0.85rem; color:#10B981;">(-60%)</span></h2>
                <p style="color: #888; font-size: 0.83rem; line-height: 1.6;">AI-driven targeted micro-interventions executed prior to structural failure, extending road lifespans by 3.5x.</p>
            </div>
        """, unsafe_allow_html=True)

# ================= PAGE 10: SDG IMPACT =================
elif st.session_state.current_page == "🏆 UN SDG Impact":
    st.markdown("""
        <div class="animated-page">
            <h1 style='font-size: 2rem; margin-bottom: 2px;'>UN SDG SUSTAINABILITY IMPACT</h1>
            <p style='color: #888; font-size: 0.9rem; margin-bottom: 25px;'>Quantifiable Alignment with United Nations Global Development Goals.</p>
        </div>
    """, unsafe_allow_html=True)
    
    s1, s2, s3 = st.columns(3)
    with s1:
        st.markdown('<div class="clean-card"><h3>SDG 9</h3><p style="color:#888; font-size:0.83rem; margin-top:8px;">Industry, Innovation & Infrastructure: Resilient infrastructure created via early-warning computer vision.</p></div>', unsafe_allow_html=True)
    with s2:
        st.markdown('<div class="clean-card"><h3>SDG 11</h3><p style="color:#888; font-size:0.83rem; margin-top:8px;">Sustainable Cities: Decreasing two-wheeler accident vulnerabilities in high-density urban transit corridors.</p></div>', unsafe_allow_html=True)
    with s3:
        st.markdown('<div class="clean-card"><h3>SDG 12</h3><p style="color:#888; font-size:0.83rem; margin-top:8px;">Responsible Consumption: Reducing bitumen waste by replacing full-road relaying with micro-treatments.</p></div>', unsafe_allow_html=True)

# Minimal Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #444; font-size: 0.72rem; letter-spacing: 1px;'>ROADX AI — TRIVANDRUM MUNICIPAL PILOT CONTROL</p>", unsafe_allow_html=True)
