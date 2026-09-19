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
    page_title="ROADGUARD AI 2.0 | Executive Infrastructure Control",
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

        /* Premium Minimalist Border Cards (No Solid Black Block Backgrounds) */
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

        /* Nav Action Card (Home Page Navigation) */
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

# Researched Infrastructure Telemetry Data
if "road_data" not in st.session_state:
    st.session_state.road_data = pd.DataFrame({
        "Road_ID": ["RG-101", "RG-102", "RG-103", "RG-104", "RG-105", "RG-106"],
        "Location": ["MG Road, Kochi", "NH-66 Edappally Bypass", "MC Road, Trivandrum", "Seaport-Airport Rd", "Vyttila Mobility Hub Rd", "Marine Drive Promenade"],
        "Latitude": [9.9816, 10.0261, 8.5241, 10.0159, 9.9667, 9.9784],
        "Longitude": [76.2999, 76.3125, 76.9366, 76.3419, 76.3188, 76.2758],
        "Health_Score": [92, 65, 41, 18, 54, 88],
        "Status": ["Optimal", "Moderate", "High Risk", "Critical Failure", "Moderate Risk", "Optimal"],
        "Predicted_Failure_Days": ["120+ days", "45 days", "14 days", "3 days (Immediate)", "30 days", "90+ days"],
        "Two_Wheeler_Risk": ["Low Risk", "Moderate Risk", "High Risk", "Critical High Risk", "Moderate Risk", "Low Risk"],
        "Four_Wheeler_Risk": ["Low Risk", "Low Risk", "Moderate Risk", "High Risk", "Low Risk", "Low Risk"],
        "Heavy_Vehicle_Risk": ["Low Risk", "High Risk", "Critical High Risk", "Structural Threat", "High Risk", "Low Risk"]
    })

df = st.session_state.road_data

# Function to assign RGB colors for Pydeck
def get_color(score):
    if score >= 75:
        return [16, 185, 129, 210]   # Emerald Green
    elif score >= 40:
        return [245, 158, 11, 210]  # Amber Orange
    else:
        return [239, 68, 68, 210]    # Red Danger

df["color"] = df["Health_Score"].apply(get_color)

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 10px 0;">
            <div style="font-size: 2rem; color: #D4AF37;">⚜️</div>
            <h3 style="font-size: 1.05rem; letter-spacing: 2px; color: #F3E5AB; margin-top: 4px;">ROADGUARD</h3>
            <p style="font-size: 0.58rem; color: #666; letter-spacing: 3px; text-transform: uppercase;">AI 2.0 EXECUTIVE</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr style='border-color: #1A1A1A;'>", unsafe_allow_html=True)
    
    nav_options = [
        "🏠 Executive Overview",
        "🏛️ Municipal Command", 
        "👁️ Neural Vision Lab", 
        "📢 Citizen Vigil Hub", 
        "📊 Financial Economics", 
        "🏆 UN SDG Impact"
    ]
    
    # Sync radio select with session state
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
            <div style="font-size: 0.7rem; color: #888;">AI MONITOR GRID</div>
            <div style="font-size: 0.82rem; font-weight: 600; color: #D4AF37; margin-top: 2px;">SECURE TELEMETRY</div>
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
            <h1 style='font-size: 2.2rem; margin-bottom: 2px;'>ROADGUARD AI 2.0</h1>
            <p style='color: #888; font-size: 0.95rem; margin-bottom: 25px;'>Autonomous Infrastructure Health & Multi-Vehicle Safety Intelligence Platform.</p>
        </div>
    """, unsafe_allow_html=True)

    # Top Telemetry Summary Metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown('<div class="stat-box"><div class="stat-number">1,420 km</div><div class="stat-title">Network Scan Area</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown('<div class="stat-box"><div class="stat-number" style="color:#EF4444;">1 Asset</div><div class="stat-title">Critical Intervention</div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown('<div class="stat-box"><div class="stat-number" style="color:#10B981;">99.4%</div><div class="stat-title">YOLOv8 Scan Accuracy</div></div>', unsafe_allow_html=True)
    with m4:
        st.markdown('<div class="stat-box"><div class="stat-number">₹2.7 Cr</div><div class="stat-title">Est. Preventative Savings</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### System Command Modules")
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("""
            <div class="nav-card">
                <h3 style="font-size: 1.1rem; margin-bottom: 4px;">🏛️ Municipal Command Center</h3>
                <p style="color: #888; font-size: 0.83rem; margin-bottom: 12px;">Real-time Mapbox spatial heatmap and multi-vehicle road safety profiling (2-wheelers, 4-wheelers, heavy vehicles).</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("OPEN COMMAND CENTER", key="btn_cmd"):
            st.session_state.current_page = "🏛️ Municipal Command"
            st.rerun()
            
        st.markdown("""
            <div class="nav-card" style="margin-top: 15px;">
                <h3 style="font-size: 1.1rem; margin-bottom: 4px;">👁️ Neural Vision Lab</h3>
                <p style="color: #888; font-size: 0.83rem; margin-bottom: 12px;">Upload pavement images to trigger automated tensor crack, pothole, and subsidence diagnostics.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("OPEN VISION LAB", key="btn_vis"):
            st.session_state.current_page = "👁️ Neural Vision Lab"
            st.rerun()

    with c2:
        st.markdown("""
            <div class="nav-card">
                <h3 style="font-size: 1.1rem; margin-bottom: 4px;">📢 Citizen Vigil Hub</h3>
                <p style="color: #888; font-size: 0.83rem; margin-bottom: 12px;">Crowdsourced road anomaly reports integrated dynamically into the municipal spatial network.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("OPEN CITIZEN HUB", key="btn_cit"):
            st.session_state.current_page = "📢 Citizen Vigil Hub"
            st.rerun()

        st.markdown("""
            <div class="nav-card" style="margin-top: 15px;">
                <h3 style="font-size: 1.1rem; margin-bottom: 4px;">📊 Financials & UN SDGs</h3>
                <p style="color: #888; font-size: 0.83rem; margin-bottom: 12px;">Evaluate cost transition metrics from reactive repair to preventative maintenance, mapped to UN SDGs 9 & 11.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("VIEW FINANCIAL & SDG IMPACT", key="btn_fin"):
            st.session_state.current_page = "📊 Financial Economics"
            st.rerun()

# ================= PAGE 1: MUNICIPAL COMMAND =================
elif st.session_state.current_page == "🏛️ Municipal Command":
    st.markdown("""
        <div class="animated-page">
            <h1 style='font-size: 2rem; margin-bottom: 2px;'>MUNICIPAL COMMAND CENTER</h1>
            <p style='color: #888; font-size: 0.9rem; margin-bottom: 20px;'>Mapbox Spatial Intelligence and Multi-Vehicle Risk Diagnostics.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col_map, col_details = st.columns([1.6, 1])
    
    with col_map:
        st.markdown("### Infrastructure Spatial Grid")
        
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position=["Longitude", "Latitude"],
            get_fill_color="color",
            get_radius=1100,
            pickable=True,
        )

        view_state = pdk.ViewState(
            latitude=9.9816,
            longitude=76.2999,
            zoom=9.8,
            pitch=30,
        )

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
                <span>🛵 <b>2-Wheelers:</b></span>
                {render_risk_badge(r_info['Two_Wheeler_Risk'])}
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span>🚗 <b>4-Wheelers:</b></span>
                {render_risk_badge(r_info['Four_Wheeler_Risk'])}
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span>🚛 <b>Heavy Vehicles:</b></span>
                {render_risk_badge(r_info['Heavy_Vehicle_Risk'])}
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if r_info['Health_Score'] < 30:
            st.error("🚨 Critical Action: Dispatching emergency PWD repair ticket.")
        else:
            st.success("✅ Operational Parameters Normal.")
        st.markdown('</div>', unsafe_allow_html=True)

# ================= PAGE 2: VISION LAB =================
elif st.session_state.current_page == "👁️ Neural Vision Lab":
    st.markdown("""
        <div class="animated-page">
            <h1 style='font-size: 2rem; margin-bottom: 2px;'>NEURAL VISION LAB</h1>
            <p style='color: #888; font-size: 0.9rem; margin-bottom: 25px;'>Automated YOLOv8 Surface Degradation Diagnostics.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col_up, col_res = st.columns(2)
    with col_up:
        st.markdown('<div class="clean-card">', unsafe_allow_html=True)
        st.markdown("### Upload Target Image")
        uploaded_img = st.file_uploader("Select pavement scan", type=["jpg", "jpeg", "png"])
        if uploaded_img:
            st.image(uploaded_img, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
            
    with col_res:
        st.markdown('<div class="clean-card">', unsafe_allow_html=True)
        st.markdown("### Diagnostic Inference")
        if uploaded_img:
            if st.button("RUN TENSOR SCAN"):
                with st.spinner("Executing neural model inference..."):
                    time.sleep(1)
                st.success("Inference Complete.")
                st.markdown("""
                    <div style="padding: 12px; border-left: 2px solid #D4AF37; margin-top: 12px; font-size: 0.88rem; line-height: 1.8;">
                        <b>Model Network:</b> YOLOv8-Pavement-X<br>
                        <b>Pothole Detection Confidence:</b> <span style="color:#D4AF37;">98.2%</span><br>
                        <b>Sub-surface Cracking Index:</b> Moderate (0.42)<br>
                        <b>Recommended Action:</b> Polymer-modified Bituminous Sealing.
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Upload an image on the left panel to begin diagnostic scan.")
        st.markdown('</div>', unsafe_allow_html=True)

# ================= PAGE 3: CITIZEN HUB =================
elif st.session_state.current_page == "📢 Citizen Vigil Hub":
    st.markdown("""
        <div class="animated-page">
            <h1 style='font-size: 2rem; margin-bottom: 2px;'>CITIZEN VIGIL HUB</h1>
            <p style='color: #888; font-size: 0.9rem; margin-bottom: 25px;'>Crowdsourced Hazard Telemetry & Civic Engagement.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col_form, col_feed = st.columns(2)
    with col_form:
        st.markdown('<div class="clean-card">', unsafe_allow_html=True)
        st.markdown("### Submit Road Hazard Report")
        with st.form("citizen_report"):
            loc_name = st.text_input("Street / Junction Name")
            hazard_type = st.selectbox("Observed Anomaly", ["Minor Crack 🟡", "Pothole / Edge Break 🟠", "Severe Road Failure 🔴"])
            submitted = st.form_submit_button("SUBMIT TELEMETRY")
            
            if submitted and loc_name:
                new_id = f"RG-E{len(df)+1}"
                score = 18 if "Severe" in hazard_type else (45 if "Pothole" in hazard_type else 70)
                new_row = {
                    "Road_ID": new_id, 
                    "Location": loc_name,
                    "Latitude": 10.01, 
                    "Longitude": 76.32,
                    "Health_Score": score, 
                    "Status": "Critical Failure" if score < 30 else "Moderate Risk",
                    "Predicted_Failure_Days": "3 Days", 
                    "Two_Wheeler_Risk": "High Risk",
                    "Four_Wheeler_Risk": "Moderate Risk",
                    "Heavy_Vehicle_Risk": "Critical High Risk"
                }
                st.session_state.road_data = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                st.success("Report dynamic injection complete! +200 Civic Points")
        st.markdown('</div>', unsafe_allow_html=True)
                
    with col_feed:
        st.markdown('<div class="clean-card">', unsafe_allow_html=True)
        st.markdown("### Recent Submissions")
        for _, row in df.tail(3).iterrows():
            st.markdown(f"""
                <div style="padding: 10px; border-radius: 6px; margin-bottom: 8px; border: 1px solid #1C1C1C; font-size: 0.83rem;">
                    📍 <b>{row['Location']}</b> — <span style="color:#D4AF37;">{row['Status']}</span>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ================= PAGE 4: FINANCIALS =================
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
                <h3 style="color: #D4AF37 !important; font-size: 1.15rem;">ROADGUARD AI Preventative Model</h3>
                <h2 style="color: #D4AF37 !important; font-size: 1.8rem; margin: 8px 0;">₹1.8 Crores <span style="font-size:0.85rem; color:#10B981;">(-60%)</span></h2>
                <p style="color: #888; font-size: 0.83rem; line-height: 1.6;">AI-driven targeted micro-interventions executed prior to structural failure, extending road lifespans by 3.5x.</p>
            </div>
        """, unsafe_allow_html=True)

# ================= PAGE 5: SDG IMPACT =================
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
st.markdown("<p style='text-align: center; color: #444; font-size: 0.72rem; letter-spacing: 1px;'>ROADGUARD AI 2.0 — KERALA MUNICIPAL INFRASTRUCTURE CONTROL</p>", unsafe_allow_html=True)
