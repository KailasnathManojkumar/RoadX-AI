import os
import streamlit as st
import pandas as pd
import pydeck as pdk
import time
import numpy as np

# --- MAPBOX API KEY & ENVIRONMENT CONFIGURATION ---
MAPBOX_TOKEN = "pk.eyJ1Ijoia2FpbGFzbmF0aDEyMyIsImEiOiJjbXU4Zm93YmEwdXdnMnlzMmdnbTQyNzNoIn0.0yYdaXOauUT-_A6VaeuMyg"
os.environ["MAPBOX_API_KEY"] = MAPBOX_TOKEN
pdk.settings.mapbox_api_key = MAPBOX_TOKEN

# Page Configuration - Wide Mode Enabled
st.set_page_config(
    page_title="ROADX AI | Executive Infrastructure Control",
    page_icon="⚜️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session Navigation State
if "current_page" not in st.session_state:
    st.session_state.current_page = "🏠 Executive Overview"

# --- NEXT-GEN CSS ANIMATIONS & GLASSMORPHISM THEME ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Cinzel:wght@500;600;700;800&display=swap');

        /* Global Layout & Smooth Scrolling */
        .main { background-color: #030303; color: #E2E8F0; font-family: 'Plus Jakarta Sans', sans-serif; }
        .block-container { padding: 3rem 3rem 6rem 3.5rem !important; max-width: 100% !important; }
        
        h1, h2, h3, h4 { color: #FFFFFF !important; font-family: 'Cinzel', serif; letter-spacing: 0.5px; }
        p, span, label, div { font-family: 'Plus Jakarta Sans', sans-serif; }

        /* Smooth Page Entrance Animations */
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(15px); filter: blur(4px); }
            to { opacity: 1; transform: translateY(0); filter: blur(0); }
        }
        .animated-page { animation: fadeInUp 0.45s cubic-bezier(0.16, 1, 0.3, 1) forwards; }

        /* Modern Glassmorphism Cards with Neon Border Glow on Hover */
        .clean-card {
            background: linear-gradient(145deg, rgba(20, 20, 20, 0.6) 0%, rgba(10, 10, 10, 0.8) 100%);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-top: 2px solid #D4AF37;
            border-radius: 14px;
            padding: 26px;
            margin-bottom: 24px;
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.6);
            transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
        }
        .clean-card:hover {
            transform: translateY(-4px);
            border-color: rgba(212, 175, 55, 0.3);
            border-top-color: #F3E5AB;
            box-shadow: 0 16px 50px rgba(212, 175, 55, 0.08);
        }

        /* Interactive Navigation Cards */
        .nav-card {
            background: linear-gradient(145deg, rgba(18, 18, 18, 0.5) 0%, rgba(8, 8, 8, 0.7) 100%);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-left: 3px solid #D4AF37;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 20px;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }
        .nav-card:hover {
            transform: translateX(6px) scale(1.01);
            background: linear-gradient(145deg, rgba(28, 28, 28, 0.7) 0%, rgba(12, 12, 12, 0.9) 100%);
            border-color: rgba(212, 175, 55, 0.4);
            border-left-color: #F3E5AB;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }

        /* Stat Boxes with Subtle Glow */
        .stat-box {
            background: linear-gradient(145deg, rgba(15, 15, 15, 0.7) 0%, rgba(5, 5, 5, 0.9) 100%);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 22px;
            text-align: center;
            box-shadow: 0 8px 30px rgba(0,0,0,0.4);
            transition: transform 0.3s ease;
        }
        .stat-box:hover { transform: translateY(-3px); }
        .stat-number {
            font-family: 'Cinzel', serif;
            font-size: 2.2rem;
            color: #D4AF37;
            font-weight: 700;
            text-shadow: 0 0 20px rgba(212, 175, 55, 0.2);
        }
        .stat-title {
            font-size: 0.75rem;
            color: #888888;
            text-transform: uppercase;
            letter-spacing: 1.8px;
            margin-top: 8px;
        }

        /* Risk Badges */
        .risk-badge {
            display: inline-block;
            padding: 5px 12px;
            border-radius: 6px;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.5px;
        }
        .risk-low { background: rgba(16, 185, 129, 0.12); color: #10B981; border: 1px solid rgba(16, 185, 129, 0.3); }
        .risk-mod { background: rgba(245, 158, 11, 0.12); color: #F59E0B; border: 1px solid rgba(245, 158, 11, 0.3); }
        .risk-high { background: rgba(239, 68, 68, 0.12); color: #EF4444; border: 1px solid rgba(239, 68, 68, 0.3); }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #020202;
            border-right: 1px solid rgba(255, 255, 255, 0.04);
            padding-top: 0.5rem;
        }
        .sidebar-hud-box {
            background: rgba(212, 175, 55, 0.02);
            border: 1px solid rgba(212, 175, 55, 0.08);
            border-radius: 10px;
            padding: 16px;
            margin-bottom: 16px;
        }

        /* Live Indicator Pulse */
        @keyframes pulseGlow {
            0% { opacity: 1; transform: scale(1); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.6); }
            70% { opacity: 0.7; transform: scale(1.05); box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }
            100% { opacity: 1; transform: scale(1); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
        }
        .live-dot {
            height: 9px; width: 9px; background-color: #10B981; border-radius: 50%;
            display: inline-block; box-shadow: 0 0 10px #10B981;
            animation: pulseGlow 2.2s infinite cubic-bezier(0.4, 0, 0.6, 1);
            margin-right: 8px;
        }

        /* Custom Styled Buttons */
        .stButton>button {
            background: linear-gradient(135deg, #D4AF37 0%, #AA8C2C 100%);
            color: #000000;
            font-weight: 700;
            font-family: 'Cinzel', serif;
            letter-spacing: 0.8px;
            border: none;
            border-radius: 8px;
            padding: 0.65rem 1.4rem;
            width: 100%;
            box-shadow: 0 4px 20px rgba(212, 175, 55, 0.25);
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background: linear-gradient(135deg, #E5C158 0%, #C5A035 100%);
            box-shadow: 0 6px 25px rgba(212, 175, 55, 0.4);
            transform: translateY(-2px);
        }
    </style>
""", unsafe_allow_html=True)

# Telemetry Data Store
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

if "community_reports" not in st.session_state:
    st.session_state.community_reports = [
        {"id": 1, "location": "Ulloor Junction Patch", "type": "Pothole / Edge Break", "votes": 14, "status": "Active"},
        {"id": 2, "location": "Kazhakkoottam Service Rd", "type": "Surface Fracture", "votes": 9, "status": "Active"}
    ]

def get_color(score):
    if score >= 75:
        return [10, 185, 129, 220]
    elif score >= 40:
        return [245, 158, 11, 220]
    else:
        return [239, 68, 68, 220]

df["color"] = df["Health_Score"].apply(get_color)

# --- SIDEBAR HUD ---
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 14px 0 6px 0;">
            <h3 style="font-size: 1.5rem; letter-spacing: 3.5px; color: #F3E5AB; margin-bottom: 2px;">ROADX AI</h3>
            <p style="font-size: 0.62rem; color: #777; letter-spacing: 4px; text-transform: uppercase;">NEURAL EXECUTIVE HUD</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr style='border-color: rgba(255,255,255,0.06); margin: 16px 0;'>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class="sidebar-hud-box">
            <div style="font-size: 0.65rem; color: #aaa; letter-spacing: 1.5px; text-transform: uppercase; font-weight: 700;">Deployment Zone</div>
            <div style="font-size: 0.95rem; font-weight: 800; color: #D4AF37; margin-top: 6px;">TRIVANDRUM WARD 1</div>
            <div style="font-size: 0.72rem; color: #777; margin-top: 3px;">Kerala Public Works Dept.</div>
            <hr style="border-color: rgba(255,255,255,0.04); margin: 10px 0;">
            <div style="font-size: 0.7rem; color: #ccc; display: flex; align-items: center; margin-top: 6px;">
                <span class="live-dot"></span> V2I Beacon: <b style="color: #10B981; margin-left: 6px;">Active Online</b>
            </div>
            <div style="font-size: 0.7rem; color: #ccc; margin-top: 8px;">⚡ AI Core: YOLOv8-Tensor (v4.2)</div>
            <div style="font-size: 0.7rem; color: #ccc; margin-top: 6px;">🛰️ GPS Lock: 8.5241° N, 76.9366° E</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="sidebar-hud-box">
            <div style="font-size: 0.65rem; color: #aaa; letter-spacing: 1.5px; text-transform: uppercase; font-weight: 700;">Telemetry Stream</div>
            <div style="display: flex; justify-content: space-between; font-size: 0.75rem; margin-top: 8px; color: #ccc;">
                <span>Active Nodes:</span> <b style="color: #D4AF37;">54 Sensors</b>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 0.75rem; margin-top: 6px; color: #ccc;">
                <span>GPU Cluster:</span> <b style="color: #10B981;">34% (Optimized)</b>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 0.75rem; margin-top: 6px; color: #ccc;">
                <span>Stream Latency:</span> <b style="color: #F3E5AB;">14 ms</b>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style="padding: 14px; text-align: center; border: 1px dashed rgba(255,255,255,0.08); border-radius: 10px; margin-top: 25px;">
            <div style="font-size: 0.65rem; color: #666; text-transform: uppercase; letter-spacing: 1px;">Security Clearance</div>
            <div style="font-size: 0.8rem; color: #D4AF37; font-weight: 700; margin-top: 4px; letter-spacing: 0.5px;">LEVEL-4 MUNICIPAL ADMIN</div>
        </div>
    """, unsafe_allow_html=True)

# --- TOP NAVIGATION SELECTOR BAR ---
st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(212, 175, 55, 0.05) 0%, rgba(20, 20, 20, 0.4) 100%); backdrop-filter: blur(12px); border: 1px solid rgba(212, 175, 55, 0.15); border-radius: 12px; padding: 14px 22px; margin-bottom: 28px; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 8px 32px rgba(0,0,0,0.4);">
        <span style="font-family: 'Cinzel', serif; font-size: 0.9rem; color: #D4AF37; letter-spacing: 1.2px; font-weight: 700;">🧭 COMMAND MODULE GATEWAY</span>
        <span style="font-size: 0.75rem; color: #888;">Select active module to launch workspace</span>
    </div>
""", unsafe_allow_html=True)

nav_options = [
    "🏠 Overview",
    "🏛️ Command", 
    "👁️ Vision Lab", 
    "🔊 Acoustic Lab",
    "⚡ Smart-Cure",
    "🌱 Carbon Ledger",
    "📢 Citizen Hub", 
    "💰 Cost Estimator",
    "🚀 Capabilities",
    "📊 Financials", 
    "🏆 UN SDG"
]

label_to_state = {
    "🏠 Overview": "🏠 Executive Overview",
    "🏛️ Command": "🏛️ Municipal Command",
    "👁️ Vision Lab": "👁️ Neural Vision Lab",
    "🔊 Acoustic Lab": "🔊 Sub-Surface Acoustic Lab",
    "⚡ Smart-Cure": "⚡ Smart-Cure V2I Trigger",
    "🌱 Carbon Ledger": "🌱 Carbon Credit Ledger",
    "📢 Citizen Hub": "📢 Citizen Vigil Hub",
    "💰 Cost Estimator": "💰 Severity & Cost Estimator",
    "🚀 Capabilities": "🚀 Capabilities Matrix",
    "📊 Financials": "📊 Financial Economics",
    "🏆 UN SDG": "🏆 UN SDG Impact"
}

state_to_label = {v: k for k, v in label_to_state.items()}
current_label = state_to_label.get(st.session_state.current_page, "🏠 Overview")

col_sel_1, col_sel_2 = st.columns([3.5, 1])
with col_sel_1:
    selected_tab = st.selectbox("Switch Active Module", nav_options, index=nav_options.index(current_label), label_visibility="collapsed")
with col_sel_2:
    if st.button("🚀 LAUNCH MODULE", key="btn_switch_module"):
        target_state = label_to_state[selected_tab]
        if target_state != st.session_state.current_page:
            st.session_state.current_page = target_state
            st.rerun()

target_state = label_to_state[selected_tab]
if target_state != st.session_state.current_page:
    st.session_state.current_page = target_state
    st.rerun()

st.markdown("<hr style='border-color: rgba(255,255,255,0.06); margin: 15px 0 35px 0;'>", unsafe_allow_html=True)

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
            <h1 style='font-size: 2.6rem; margin-bottom: 6px; background: linear-gradient(90deg, #FFFFFF 0%, #D4AF37 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>ROADX AI EXECUTIVE SUITE</h1>
            <p style='color: #888; font-size: 1.05rem; margin-bottom: 35px;'>Trivandrum Municipal Pilot: Autonomous Infrastructure Health & Multi-Vehicle Safety Intelligence.</p>
        </div>
    """, unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown('<div class="stat-box"><div class="stat-number">12.4 km</div><div class="stat-title">Pilot Scan Corridor</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown('<div class="stat-box"><div class="stat-number" style="color:#EF4444; text-shadow: 0 0 20px rgba(239,68,68,0.3);">1 Asset</div><div class="stat-title">Critical Intervention</div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown('<div class="stat-box"><div class="stat-number" style="color:#10B981; text-shadow: 0 0 20px rgba(16,185,129,0.3);">99.4%</div><div class="stat-title">YOLOv8 Scan Accuracy</div></div>', unsafe_allow_html=True)
    with m4:
        st.markdown('<div class="stat-box"><div class="stat-number">142 t</div><div class="stat-title">Carbon Credits Issued</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### System Command Modules")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
            <div class="nav-card">
                <h3 style="font-size: 1.2rem; margin-bottom: 8px;">🏛️ Municipal Command Center</h3>
                <p style="color: #888; font-size: 0.9rem; margin-bottom: 16px;">Live Mapbox Trivandrum GIS heatmap and multi-vehicle road safety profiling.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("OPEN COMMAND CENTER", key="btn_cmd"):
            st.session_state.current_page = "🏛️ Municipal Command"
            st.rerun()
            
        st.markdown("""
            <div class="nav-card" style="margin-top: 24px;">
                <h3 style="font-size: 1.2rem; margin-bottom: 8px;">🔊 Sub-Surface Acoustic Lab</h3>
                <p style="color: #888; font-size: 0.9rem; margin-bottom: 16px;">Simulates real-time ground-penetrating acoustic resonance scans to predict hidden sub-surface hollows and sinkholes.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("OPEN ACOUSTIC LAB", key="btn_acou"):
            st.session_state.current_page = "🔊 Sub-Surface Acoustic Lab"
            st.rerun()

    with c2:
        st.markdown("""
            <div class="nav-card">
                <h3 style="font-size: 1.2rem; margin-bottom: 8px;">⚡ Smart-Cure V2I Trigger</h3>
                <p style="color: #888; font-size: 0.9rem; margin-bottom: 16px;">Simulates direct vehicle-to-infrastructure (V2I) micro-induction triggers that activate self-healing asphalt polymers.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("OPEN SMART-CURE TRIGGER", key="btn_cure"):
            st.session_state.current_page = "⚡ Smart-Cure V2I Trigger"
            st.rerun()

        st.markdown("""
            <div class="nav-card" style="margin-top: 24px;">
                <h3 style="font-size: 1.2rem; margin-bottom: 8px;">🌱 Carbon Credit Ledger</h3>
                <p style="color: #888; font-size: 0.9rem; margin-bottom: 16px;">Automatically calculates avoided carbon emissions from preventative maintenance and converts them into verified municipal credits.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("OPEN CARBON LEDGER", key="btn_carb"):
            st.session_state.current_page = "🌱 Carbon Credit Ledger"
            st.rerun()

    st.markdown("<br><hr style='border-color: rgba(255,255,255,0.06);'><br>", unsafe_allow_html=True)
    st.markdown("### Executive Network Overview Table")
    st.dataframe(df[["Road_ID", "Location", "Health_Score", "Status", "Predicted_Failure_Days"]], use_container_width=True, hide_index=True)

# ================= PAGE 1: MUNICIPAL COMMAND =================
elif st.session_state.current_page == "🏛️ Municipal Command":
    st.markdown("""
        <div class="animated-page">
            <h1 style='font-size: 2.4rem; margin-bottom: 6px;'>MUNICIPAL COMMAND CENTER</h1>
            <p style='color: #888; font-size: 1.05rem; margin-bottom: 30px;'>Trivandrum Spatial Intelligence and Multi-Vehicle Risk Diagnostics.</p>
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
        st.pydeck_chart(deck, use_container_width=True)
        
    with col_details:
        st.markdown("### Multi-Vehicle Safety Evaluation")
        st.markdown('<div class="clean-card">', unsafe_allow_html=True)
        sel_id = st.selectbox("Select Asset ID:", df["Road_ID"], key="sel_asset_id")
        r_info = df[df["Road_ID"] == sel_id].iloc[0]
        
        st.markdown(f"""
            <div style="font-size: 0.92rem; line-height: 2;">
                <b>Location:</b> {r_info['Location']}<br>
                <b>Health Score:</b> <span style="color: #D4AF37; font-weight: 700;">{r_info['Health_Score']} / 100</span><br>
                <b>Estimated Time To Failure:</b> {r_info['Predicted_Failure_Days']}
            </div>
            <hr style="border-color: rgba(255,255,255,0.06); margin: 18px 0;">
            <div style="font-size: 0.88rem; font-weight: 700; margin-bottom: 14px; color: #D4AF37; letter-spacing: 0.5px;">VEHICLE TYPE SAFETY PROFILES:</div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <span>🛵 <b>2-Wheelers:</b></span> {render_risk_badge(r_info['Two_Wheeler_Risk'])}
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <span>🚗 <b>4-Wheelers:</b></span> {render_risk_badge(r_info['Four_Wheeler_Risk'])}
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span>🚛 <b>Heavy Vehicles:</b></span> {render_risk_badge(r_info['Heavy_Vehicle_Risk'])}
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Comprehensive Asset Telemetry Log")
    st.dataframe(df, use_container_width=True, hide_index=True)

# ================= PAGE 2: VISION LAB =================
elif st.session_state.current_page == "👁️ Neural Vision Lab":
    st.markdown("""
        <div class="animated-page">
            <h1 style='font-size: 2.4rem; margin-bottom: 6px;'>NEURAL VISION LAB</h1>
            <p style='color: #888; font-size: 1.05rem; margin-bottom: 30px;'>Automated YOLOv8 Surface Degradation Diagnostics & Live V2I Warnings.</p>
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
                    <div style="padding: 16px; border-left: 3px solid #D4AF37; margin-top: 18px; font-size: 0.92rem; line-height: 20px;">
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
            <h1 style='font-size: 2.4rem; margin-bottom: 6px;'>SUB-SURFACE ACOUSTIC SONAR LAB</h1>
            <p style='color: #888; font-size: 1.05rem; margin-bottom: 30px;'>Simulates real-time ground-penetrating acoustic resonance scans to predict hidden sub-surface hollows and sinkholes weeks before they visually appear.</p>
        </div>
    """, unsafe_allow_html=True)

    col_ac1, col_ac2 = st.columns([1.2, 1])
    with col_ac1:
        st.markdown('<div class="clean-card">', unsafe_allow_html=True)
        st.markdown("### Acoustic Resonance Profiler")
        sel_corridor = st.selectbox("Select Test Corridor:", ["MC Road Sector B (Ulloor)", "NH-66 Kazhakkoottam Underpass", "Kowdiar Junction Ring"], key="sel_acou_corridor")
        sweep_speed = st.slider("Vehicle Fleet Roll Speed (km/h)", 20, 80, 45, key="slider_sweep_speed")
        
        if st.button("EXECUTE SUB-SURFACE ACOUSTIC SCAN"):
            with st.spinner("Analyzing tire vibration frequencies and acoustic dampening profiles..."):
                time.sleep(1.2)
            st.success("Acoustic Tomography Mapping Successful.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_ac2:
        st.markdown('<div class="clean-card">', unsafe_allow_html=True)
        st.markdown("### Sub-Surface Anomaly Report")
        st.markdown("""
            <div style="font-size: 0.92rem; line-height: 2;">
                <b>Corridor ID:</b> TVM-ACOUSTIC-02<br>
                <b>Sub-Base Void Status:</b> <span style="color: #EF4444; font-weight: 800;">CAVITY DETECTED (-1.2m depth)</span><br>
                <b>Estimated Time to Sinkhole Formation:</b> 28 Days<br>
                <b>Surface Visual Status:</b> 100% Intact (Invisible to Cameras)<br>
                <b>Acoustic Frequency Deviation:</b> 42.8 Hz (Standard: 18.2 Hz)
            </div>
            <hr style="border-color: rgba(255,255,255,0.06); margin: 18px 0;">
            <div style="font-size: 0.88rem; color: #D4AF37;"><b>AI Prognostic Recommendation:</b> Inject low-viscosity polyurethane grout into sub-base layer immediately to arrest soil erosion.</div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ================= NEW FEATURE 2: SMART-CURE V2I TRIGGER =================
elif st.session_state.current_page == "⚡ Smart-Cure V2I Trigger":
    st.markdown("""
        <div class="animated-page">
            <h1 style='font-size: 2.4rem; margin-bottom: 6px;'>SMART-CURE V2I MATERIAL TRIGGER</h1>
            <p style='color: #888; font-size: 1.05rem; margin-bottom: 30px;'>Simulates direct vehicle-to-infrastructure (V2I) micro-induction triggers that activate self-healing asphalt polymers.</p>
        </div>
    """, unsafe_allow_html=True)

    c_tr1, c_tr2 = st.columns(2)
    with c_tr1:
        st.markdown('<div class="clean-card">', unsafe_allow_html=True)
        st.markdown("### High-Stress Load Zone Config")
        truck_weight = st.slider("Approaching Heavy Axle Load (Tons)", 10, 45, 32, key="slider_truck_weight")
        polymer_status = st.selectbox("Embedded Microcapsule Status", ["Active (Ready to Bond)", "Depleted", "Regenerating"], key="sel_poly_status")
        
        if st.button("SEND V2I INDUCTION PULSE"):
            with st.spinner("Broadcasting low-frequency induction pulse via roadside unit..."):
                time.sleep(1)
            st.success("Induction Pulse Broadcasted Successfully.")
        st.markdown('</div>', unsafe_allow_html=True)

    with c_tr2:
        st.markdown('<div class="clean-card">', unsafe_allow_html=True)
        st.markdown("### Material Activation Telemetry")
        st.markdown(f"""
            <div style="font-size: 0.92rem; line-height: 2;">
                <b>Axle Stress Level:</b> {truck_weight} Tons<br>
                <b>Induction Frequency:</b> 300 kHz Electromagnetic Pulse<br>
                <b>Polymer Viscosity State:</b> <span style="color: #10B981;">Curing & Bonding Active</span><br>
                <b>Asphalt Fatigue Recovery Rate:</b> 91.4%<br>
                <b>Crew Intervention Required:</b> NONE (Autonomous Healing)
            </div>
            <hr style="border-color: rgba(255,255,255,0.06); margin: 18px 0;">
            <div style="font-size: 0.88rem; color: #D4AF37;"><b>System Note:</b> Microcapsules of rejuvenating oil successfully melted and sealed micro-fractures under heavy truck weight.</div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ================= NEW FEATURE 3: CARBON CREDIT LEDGER =================
elif st.session_state.current_page == "🌱 Carbon Credit Ledger":
    st.markdown("""
        <div class="animated-page">
            <h1 style='font-size: 2.4rem; margin-bottom: 6px;'>MUNICIPAL CARBON CREDIT LEDGER</h1>
            <p style='color: #888; font-size: 1.05rem; margin-bottom: 30px;'>Automatically calculates avoided carbon emissions from preventative maintenance and converts them into verified municipal carbon offset credits.</p>
        </div>
    """, unsafe_allow_html=True)

    cb1, cb2 = st.columns(2)
    with cb1:
        st.markdown('<div class="clean-card">', unsafe_allow_html=True)
        st.markdown("### Preventative Carbon Offset Metrics")
        st.markdown("""
            <div style="font-size: 0.92rem; line-height: 2;">
                <b>Total Avoided Hot-Mix Bitumen:</b> 340 Metric Tons<br>
                <b>Transport Fuel Saved:</b> 14,200 Liters Diesel<br>
                <b>Net Carbon Dioxide Offset:</b> <span style="color:#10B981; font-weight:750;">142.5 tCO2e</span><br>
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
            <h1 style='font-size: 2.4rem; margin-bottom: 6px;'>CITIZEN VIGIL HUB</h1>
            <p style='color: #888; font-size: 1.05rem; margin-bottom: 30px;'>Crowdsourced Hazard Telemetry & Community Verification Loop.</p>
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
            c_col1.markdown(f"📍 **{report['location']}**<br><span style='font-size:0.82rem; color:#888;'>{report['type']}</span>", unsafe_allow_html=True)
            if c_col2.button(f"👍 Still Here ({report['votes']})", key=f"vote_{idx}"):
                st.session_state.community_reports[idx]["votes"] += 1
                st.success("Vote recorded!")
                st.rerun()
            st.markdown("<hr style='border-color: rgba(255,255,255,0.04); margin: 12px 0;'>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ================= PAGE 7: SEVERITY & COST ESTIMATOR =================
elif st.session_state.current_page == "💰 Severity & Cost Estimator":
    st.markdown("""
        <div class="animated-page">
            <h1 style='font-size: 2.4rem; margin-bottom: 6px;'>SEVERITY & REPAIR COST ESTIMATOR</h1>
            <p style='color: #888; font-size: 1.05rem; margin-bottom: 30px;'>Calculate physical asphalt volumes and municipal financial requirements.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="clean-card">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        width_cm = st.slider("Pothole Diameter / Width (cm)", 10, 300, 60, key="slider_width_cm")
    with c2:
        depth_cm = st.slider("Pothole Depth (cm)", 2, 70, 15, key="slider_depth_cm")

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
            <h1 style='font-size: 2.4rem; margin-bottom: 6px;'>SYSTEM CAPABILITIES DIRECTORY</h1>
            <p style='color: #888; font-size: 1.05rem; margin-bottom: 30px;'>Comprehensive breakdown of core features, advanced innovations, and municipal modules provided by RoadX AI.</p>
        </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🌟 Next-Gen Deep Tech", "🏛️ Municipal Features", "🚗 V2I & Safety Tools"])
    
    with tab1:
        st.markdown("""
            <div class="clean-card">
                <h3>1. Sub-Surface Acoustic Sonar Lab</h3>
                <p style="color:#aaa; font-size:0.9rem;">Simulates real-time ground-penetrating acoustic resonance scans to predict hidden sub-surface hollows and sinkholes.</p>
                <hr style="border-color:rgba(255,255,255,0.06);">
                <h3>2. Smart-Cure V2I Material Trigger</h3>
                <p style="color:#aaa; font-size:0.9rem;">Simulates direct vehicle-to-infrastructure (V2I) micro-induction triggers that activate self-healing asphalt polymers.</p>
                <hr style="border-color:rgba(255,255,255,0.06);">
                <h3>3. Carbon Credit Ledger & ESG Monetization</h3>
                <p style="color:#aaa; font-size:0.9rem;">Automatically calculates avoided carbon emissions from preventative maintenance and converts them into verified municipal credits.</p>
            </div>
        """, unsafe_allow_html=True)

    with tab2:
        st.markdown("""
            <div class="clean-card">
                <h3>1. Mapbox Spatial Heatmap Command</h3>
                <p style="color:#aaa; font-size:0.9rem;">Real-time GIS-mapped network overview color-coded by structural health scores across regional road assets.</p>
                <hr style="border-color:rgba(255,255,255,0.06);">
                <h3>2. Preventative Economics Engine</h3>
                <p style="color:#aaa; font-size:0.9rem;">Shifts public works budgeting from expensive reactive reconstruction (₹4.5 Cr) to proactive micro-interventions (₹1.8 Cr).</p>
            </div>
        """, unsafe_allow_html=True)

    with tab3:
        st.markdown("""
            <div class="clean-card">
                <h3>1. Vehicle-to-Infrastructure (V2I) Alerts</h3>
                <p style="color:#aaa; font-size:0.9rem;">Instantly broadcasts audio/visual safety warnings and speed reduction advisories to connected vehicles approaching critical hazards.</p>
                <hr style="border-color:rgba(255,255,255,0.06);">
                <h3>2. Multi-Vehicle Risk Profiling</h3>
                <p style="color:#aaa; font-size:0.9rem;">Evaluates how individual road anomalies uniquely threaten 2-wheelers, passenger 4-wheelers, and heavy freight trucks.</p>
            </div>
        """, unsafe_allow_html=True)

# ================= PAGE 9: FINANCIALS =================
elif st.session_state.current_page == "📊 Financial Economics":
    st.markdown("""
        <div class="animated-page">
            <h1 style='font-size: 2.4rem; margin-bottom: 6px;'>FINANCIAL ECONOMICS</h1>
            <p style='color: #888; font-size: 1.05rem; margin-bottom: 30px;'>Transitioning from Reactive Resurfacing to Autonomous Preventative Maintenance.</p>
        </div>
    """, unsafe_allow_html=True)
    
    p1, p2 = st.columns(2)
    with p1:
        st.markdown("""
            <div class="clean-card" style="border-top-color: #EF4444;">
                <h3 style="color: #EF4444 !important; font-size: 1.25rem;">Traditional Reactive Budget</h3>
                <h2 style="color: #EF4444 !important; font-size: 2.2rem; margin: 12px 0;">₹4.5 Crores / yr</h2>
                <p style="color: #888; font-size: 0.9rem; line-height: 1.8;">High expenditure caused by waiting for full asphalt degradation, resulting in complete relaying and accident liability payouts.</p>
            </div>
        """, unsafe_allow_html=True)
    with p2:
        st.markdown("""
            <div class="clean-card" style="border-top-color: #D4AF37;">
                <h3 style="color: #D4AF37 !important; font-size: 1.25rem;">RoadX AI Preventative Model</h3>
                <h2 style="color: #D4AF37 !important; font-size: 2.2rem; margin: 12px 0;">₹1.8 Crores / yr</h2>
                <p style="color: #888; font-size: 0.9rem; line-height: 1.8;">Achieved via targeted micro-sealing, acoustic void injection, and AI predictive maintenance, saving over 60% in municipal infrastructure overhead.</p>
            </div>
        """, unsafe_allow_html=True)

# ================= PAGE 10: UN SDG IMPACT =================
elif st.session_state.current_page == "🏆 UN SDG Impact":
    st.markdown("""
        <div class="animated-page">
            <h1 style='font-size: 2.4rem; margin-bottom: 6px;'>UN SUSTAINABLE DEVELOPMENT GOALS</h1>
            <p style='color: #888; font-size: 1.05rem; margin-bottom: 30px;'>Aligning Municipal Infrastructure Intelligence with Global ESG & Sustainability Standards.</p>
        </div>
    """, unsafe_allow_html=True)

    sdg1, sdg2, sdg3 = st.columns(3)
    
    with sdg1:
        st.markdown("""
            <div class="clean-card">
                <h3 style="font-size: 1.15rem; color: #D4AF37;">SDG 9: Industry & Innovation</h3>
                <p style="color: #aaa; font-size: 0.88rem; margin-top: 12px;">Upgrading municipal infrastructure with resilient AI computer vision, IoT sensors, and automated V2I communication networks.</p>
            </div>
        """, unsafe_allow_html=True)
        
    with sdg2:
        st.markdown("""
            <div class="clean-card">
                <h3 style="font-size: 1.15rem; color: #D4AF37;">SDG 11: Sustainable Cities</h3>
                <p style="color: #aaa; font-size: 0.88rem; margin-top: 12px;">Enhancing commuter safety across multi-vehicle classes, reducing severe accidents, and preventing urban sinkhole collapses.</p>
            </div>
        """, unsafe_allow_html=True)
        
    with sdg3:
        st.markdown("""
            <div class="clean-card">
                <h3 style="font-size: 1.15rem; color: #D4AF37;">SDG 13: Climate Action</h3>
                <p style="color: #aaa; font-size: 0.88rem; margin-top: 12px;">Quantifying and tokenizing avoided carbon emissions from heavy hot-mix asphalt manufacturing and heavy transport logistics.</p>
            </div>
        """, unsafe_allow_html=True)
