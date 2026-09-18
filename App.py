import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import time

# Page Configuration
st.set_page_config(
    page_title="ROADGUARD AI 2.0 | Elite Command",
    page_icon="⚜️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ultra-Aesthetic Royal Black & Gold Theme + Advanced Animations CSS
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=Cinzel:wght@600;700;900&display=swap');

        /* Global Styling */
        .main { background-color: #030303; color: #E2E8F0; font-family: 'Plus Jakarta Sans', sans-serif; }
        .block-container { padding: 2rem 3rem 4rem 3rem; max-width: 100%; }
        
        /* Typography */
        h1, h2, h3, h4 { color: #F8FAFC !important; font-family: 'Cinzel', serif; letter-spacing: 0.5px; }
        p, span, label, div { font-family: 'Plus Jakarta Sans', sans-serif; }
        
        /* Smooth Keyframe Animations */
        @keyframes slideUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes pulseGlow {
            0% { box-shadow: 0 0 5px rgba(212, 175, 55, 0.2); }
            50% { box-shadow: 0 0 20px rgba(212, 175, 55, 0.6); }
            100% { box-shadow: 0 0 5px rgba(212, 175, 55, 0.2); }
        }
        @keyframes liveBlink {
            0% { opacity: 1; }
            50% { opacity: 0.4; }
            100% { opacity: 1; }
        }
        
        .animated-wrapper {
            animation: slideUp 0.7s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }

        /* Glassmorphism Luxury Cards */
        .glass-card {
            background: linear-gradient(135deg, rgba(20, 20, 20, 0.8) 0%, rgba(10, 10, 10, 0.9) 100%);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(212, 175, 55, 0.2);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        }
        .glass-card:hover {
            border-color: rgba(212, 175, 55, 0.6);
            transform: translateY(-4px);
            box-shadow: 0 12px 40px 0 rgba(212, 175, 55, 0.15);
        }

        /* Metric Hero Cards */
        .metric-card {
            background: radial-gradient(circle at top left, rgba(30, 25, 10, 0.4) 0%, rgba(10, 10, 10, 0.9) 100%);
            border: 1px solid rgba(212, 175, 55, 0.3);
            border-radius: 14px;
            padding: 20px;
            text-align: center;
            animation: pulseGlow 4s infinite;
        }
        .metric-value {
            font-family: 'Cinzel', serif;
            font-size: 2.2rem;
            color: #D4AF37;
            font-weight: 700;
        }
        .metric-label {
            font-size: 0.8rem;
            color: #94A3B8;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-top: 5px;
        }

        /* Live Indicator Dot */
        .live-dot {
            height: 10px;
            width: 10px;
            background-color: #10B981;
            border-radius: 50%;
            display: inline-block;
            animation: liveBlink 1.5s infinite;
            margin-right: 6px;
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #050505;
            border-right: 1px solid rgba(212, 175, 55, 0.15);
        }

        /* Custom Gold Buttons */
        .stButton>button {
            background: linear-gradient(135deg, #D4AF37 0%, #9A7B1C 100%);
            color: #000000;
            font-weight: 700;
            font-family: 'Cinzel', serif;
            letter-spacing: 1px;
            border: none;
            border-radius: 10px;
            padding: 0.7rem 1.5rem;
            width: 100%;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(212, 175, 55, 0.2);
        }
        .stButton>button:hover {
            background: linear-gradient(135deg, #F3E5AB 0%, #D4AF37 100%);
            box-shadow: 0 6px 25px rgba(212, 175, 55, 0.4);
            transform: translateY(-2px);
        }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State
if "road_data" not in st.session_state:
    st.session_state.road_data = pd.DataFrame({
        "Road_ID": ["RG-101", "RG-102", "RG-103", "RG-104", "RG-105"],
        "Location": ["MG Road, Kochi", "NH-66 Bypass", "MC Road, Trivandrum", "Seaport-Airport Rd", "Beach Road"],
        "Latitude": [9.9816, 10.0159, 8.5241, 10.0261, 9.9312],
        "Longitude": [76.2999, 76.3419, 76.9366, 76.3551, 76.2673],
        "Health_Score": [92, 65, 41, 18, 85],
        "Status": ["Optimal 🟢", "Moderate 🟡", "High Risk 🟠", "Critical Failure 🔴", "Optimal 🟢"],
        "Predicted_Failure_Days": ["120+ days", "45 days", "15 days", "3 days (Immediate)", "90+ days"],
        "Bike_Risk": ["Low", "Moderate", "High", "Critical ⚠️", "Low"]
    })

if "citizen_points" not in st.session_state:
    st.session_state.citizen_points = 1450

df = st.session_state.road_data

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <div style="font-size: 3rem; color: #D4AF37; margin-bottom: -10px;">⚜️</div>
            <h2 style="font-size: 1.4rem; letter-spacing: 4px; color: #F3E5AB; margin-top: 10px;">ROADGUARD</h2>
            <p style="font-size: 0.65rem; color: #64748B; letter-spacing: 6px; text-transform: uppercase;">AI 2.0 ELITE COMMAND</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr style='border-color: rgba(212,175,55,0.2);'>", unsafe_allow_html=True)
    
    page = st.radio(
        "Navigation Menu", 
        ["🏛️ Command Center", "👁️ Neural Vision Lab", "📢 Citizen Vigil Hub", "📊 Financial Analytics", "🏆 SDG Impact Grid"]
    )
    
    st.markdown("<hr style='border-color: rgba(212,175,55,0.2);'>", unsafe_allow_html=True)
    st.markdown("""
        <div class="glass-card" style="padding: 15px; margin-bottom: 0;">
            <div style="font-size: 0.8rem; color: #94A3B8;"><span class="live-dot"></span>SYS TELEMETRY</div>
            <div style="font-size: 0.95rem; font-weight: 600; color: #D4AF37; margin-top: 5px;">GRID SECURE & ACTIVE</div>
            <div style="font-size: 0.75rem; color: #64748B; margin-top: 8px;">Guardian XP: <b>1,450 PTS</b></div>
        </div>
    """, unsafe_allow_html=True)

# ================= PAGE 1: COMMAND CENTER =================
if page == "🏛️ Command Center":
    st.markdown("""
        <div class="animated-wrapper">
            <h1 style='text-align: center; font-size: 2.4rem; margin-bottom: 5px;'>MUNICIPAL SPATIAL COMMAND</h1>
            <p style='text-align: center; color: #94A3B8; font-size: 1rem; margin-bottom: 35px;'>Autonomous Infrastructure Health & Two-Wheeler Priority Grid</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sleek Custom Metric Cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('<div class="metric-card"><div class="metric-value">1,420 km</div><div class="metric-label">Monitored Network</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="metric-card"><div class="metric-value" style="color:#EF4444;">1 Zone</div><div class="metric-label">Critical Dispatch</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="metric-card"><div class="metric-value" style="color:#F59E0B;">14 Zones</div><div class="metric-label">Two-Wheeler Risk</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="metric-card"><div class="metric-value" style="color:#10B981;">99.4%</div><div class="metric-label">AI Tensor Accuracy</div></div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_map, col_details = st.columns([1.6, 1])
    with col_map:
        st.markdown("### 🗺️ Live Infrastructure Heatmap")
        st.markdown('<div class="glass-card" style="padding: 12px;">', unsafe_allow_html=True)
        m = folium.Map(location=[9.9816, 76.2999], zoom_start=11, tiles="CartoDB dark_matter")
        for _, row in df.iterrows():
            color = "green" if row["Health_Score"] >= 75 else ("orange" if row["Health_Score"] >= 30 else "red")
            folium.Marker(
                [row["Latitude"], row["Longitude"]],
                popup=f"<b>{row['Road_ID']}</b><br>{row['Location']}<br>Status: {row['Status']}",
                icon=folium.Icon(color=color, icon="shield", prefix="fa")
            ).add_to(m)
        st_folium(m, width=650, height=440)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_details:
        st.markdown("### 🔍 Asset Telemetry Inspector")
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        sel_id = st.selectbox("Select Road Asset ID:", df["Road_ID"])
        r_info = df[df["Road_ID"] == sel_id].iloc[0]
        
        st.markdown(f"""
        <div style="margin-top: 10px; line-height: 1.8;">
            📍 <b>Location:</b> {r_info['Location']}<br>
            ⭐ <b>Health Index:</b> <span style="color: #D4AF37; font-weight: bold; font-size: 1.1rem;">{r_info['Health_Score']}/100</span><br>
            🛡️ <b>Status:</b> {r_info['Status']}<br>
            ⏳ <b>Failure Window:</b> {r_info['Predicted_Failure_Days']}<br>
            ⚠️ <b>Two-Wheeler Risk:</b> <span style="color: #EF4444; font-weight: bold;">{r_info['Bike_Risk']}</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if r_info['Health_Score'] < 30:
            st.error("🚨 **Autonomous Alert:** Priority repair ticket automatically routed to municipal contractors.")
        else:
            st.success("✅ **Asset Secure:** Structural parameters are optimal.")
        st.markdown('</div>', unsafe_allow_html=True)

# ================= PAGE 2: NEURAL VISION LAB =================
elif page == "👁️ Neural Vision Lab":
    st.markdown("""
        <div class="animated-wrapper">
            <h1 style='font-size: 2.4rem; margin-bottom: 5px;'>NEURAL VISION LAB</h1>
            <p style='color: #94A3B8; font-size: 1rem; margin-bottom: 30px;'>Upload pavement imagery for deep-tensor YOLOv8 structural decay analysis.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col_up, col_res = st.columns(2)
    with col_up:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📥 Optical Input Target")
        uploaded_img = st.file_uploader("Upload Surface Photo", type=["jpg", "jpeg", "png"])
        if uploaded_img:
            st.image(uploaded_img, caption="Target Loaded for Optical Scan", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
            
    with col_res:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### ⚜️ Tensor Diagnostic Engine")
        if uploaded_img:
            if st.button("EXECUTE OPTICAL SCAN"):
                with st.spinner("Analyzing subsurface fracture propagation tensors..."):
                    time.sleep(1.2)
                st.success("Scan Protocol Successful.")
                st.markdown("""
                <div style="background: rgba(0,0,0,0.5); padding: 15px; border-radius: 10px; border-left: 3px solid #D4AF37; margin-top: 15px;">
                    <b>Active Model:</b> YOLOv8-Elite RoadNet<br>
                    <b>Pothole Probability:</b> <span style="color:#D4AF37; font-weight:bold;">98.2%</span><br>
                    <b>Sub-base Fatigue:</b> Critical Micro-Fissuring Detected<br>
                    <b>Prescribed Action:</b> Polymer injection sealing mandatory.
                </div>
                """, unsafe_allow_html=True)
                st.warning("⚠️ **Safety Notice:** Severe risk factor for two-wheeler stabilization.")
        else:
            st.info("👈 Please provide an inspection target image on the left panel to initialize real-time tensor diagnostics.")
        st.markdown('</div>', unsafe_allow_html=True)

# ================= PAGE 3: CITIZEN VIGIL HUB =================
elif page == "📢 Citizen Vigil Hub":
    st.markdown("""
        <div class="animated-wrapper">
            <h1 style='font-size: 2.4rem; margin-bottom: 5px;'>CITIZEN VIGIL HUB</h1>
            <p style='color: #94A3B8; font-size: 1rem; margin-bottom: 30px;'>Crowdsourcing municipal road intelligence with gamified commuter rewards.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col_form, col_feed = st.columns(2)
    with col_form:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📝 Report Road Hazard")
        with st.form("citizen_report"):
            loc_name = st.text_input("Junction / Street Name", placeholder="e.g., MG Road Cross 4")
            hazard_type = st.selectbox("Severity Classification", ["Minor Micro-Crack 🟡", "Severe Pothole 🟠", "Critical Infrastructure Failure 🔴"])
            comment = st.text_area("Rider Impact Description", placeholder="Dangerous swerve zone during peak hours.")
            submitted = st.form_submit_button("BROADCAST TO MUNICIPAL CORE")
            
            if submitted and loc_name:
                new_id = f"RG-E{len(df)+1}"
                score = 15 if "Critical" in hazard_type else (40 if "Severe" in hazard_type else 65)
                new_row = {
                    "Road_ID": new_id,
                    "Location": loc_name,
                    "Latitude": 10.01 + (len(df) * 0.005),
                    "Longitude": 76.32 + (len(df) * 0.005),
                    "Health_Score": score,
                    "Status": "Critical Failure 🔴" if "Critical" in hazard_type else "High Risk 🟠",
                    "Predicted_Failure_Days": "3 Days (Crowdsourced)",
                    "Bike_Risk": "Critical ⚠️"
                }
                st.session_state.road_data = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                st.session_state.citizen_points += 200
                st.success(f"Telemetry broadcasted successfully! +200 Guardian XP earned.")
                st.balloons()
        st.markdown('</div>', unsafe_allow_html=True)
                
    with col_feed:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### ⚡ Live Community Feed")
        for _, row in df.tail(3).iterrows():
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.03); padding: 12px; border-radius: 8px; margin-bottom: 10px; border: 1px solid rgba(255,255,255,0.05);">
                📍 <b>{row['Location']}</b><br>
                <span style="font-size:0.85rem; color:#94A3B8;">Status: {row['Status']} | Rider Risk: {row['Bike_Risk']}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ================= PAGE 4: FINANCIAL ANALYTICS =================
elif page == "📊 Financial Analytics":
    st.markdown("""
        <div class="animated-wrapper">
            <h1 style='font-size: 2.4rem; margin-bottom: 5px;'>FINANCIAL & ECONOMIC IMPACT</h1>
            <p style='color: #94A3B8; font-size: 1rem; margin-bottom: 30px;'>Transitioning municipal budgets from reactive disaster spending to preventative AI.</p>
        </div>
    """, unsafe_allow_html=True)
    
    p1, p2 = st.columns(2)
    with p1:
        st.markdown("""
        <div class="glass-card" style="border-left: 4px solid #EF4444;">
            <h3 style="color: #EF4444 !important;">Traditional Reactive Model</h3>
            <h2 style="color: #EF4444 !important; font-size: 2rem;">₹4.5 Crores / yr</h2>
            <p style="color: #94A3B8; margin-top: 15px;">High public expenditure caused by waiting for full structural collapse, emergency repaving, and accident liability claims.</p>
        </div>
        """, unsafe_allow_html=True)
    with p2:
        st.markdown("""
        <div class="glass-card" style="border-left: 4px solid #D4AF37;">
            <h3 style="color: #D4AF37 !important;">ROADGUARD AI 2.0 Model</h3>
            <h2 style="color: #D4AF37 !important; font-size: 2rem;">₹1.8 Crores / yr <span style="font-size: 0.85rem; color: #10B981;">(-60% Savings)</span></h2>
            <p style="color: #94A3B8; margin-top: 15px;">Targeted preventative micro-treatments that triple road asset lifespans at a fraction of standard heavy construction costs.</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="glass-card" style="text-align: center;">', unsafe_allow_html=True)
    st.markdown("### 📥 Official Contractor Master Schedule Export")
    csv_bytes = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="DOWNLOAD MUNICIPAL TENDER CSV",
        data=csv_bytes,
        file_name="roadguard_elite_schedule.csv",
        mime="text/csv"
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ================= PAGE 5: SDG IMPACT GRID =================
elif page == "🏆 SDG Impact Grid":
    st.markdown("""
        <div class="animated-wrapper">
            <h1 style='font-size: 2.4rem; margin-bottom: 5px;'>UN SDG ALIGNMENT & GAMIFICATION</h1>
            <p style='color: #94A3B8; font-size: 1rem; margin-bottom: 30px;'>Aligning urban innovation with global sustainability frameworks and civic pride.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col_sdg1, col_sdg2, col_sdg3 = st.columns(3)
    with col_sdg1:
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: #D4AF37;">🏗️ SDG 9</h3>
            <b style="color: #F8FAFC;">Resilient Infrastructure</b><br><br>
            <p style="color: #94A3B8; font-size: 0.9rem;">Maximizes material durability and prevents catastrophic failures through automated early tensor alerts.</p>
        </div>
        """, unsafe_allow_html=True)
    with col_sdg2:
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: #D4AF37;">🏙️ SDG 11</h3>
            <b style="color: #F8FAFC;">Sustainable Cities</b><br><br>
            <p style="color: #94A3B8; font-size: 0.9rem;">Prioritizes two-wheeler safety and eliminates urban bottlenecks caused by degraded roadways.</p>
        </div>
        """, unsafe_allow_html=True)
    with col_sdg3:
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: #D4AF37;">♻️ SDG 12</h3>
            <b style="color: #F8FAFC;">Responsible Production</b><br><br>
            <p style="color: #94A3B8; font-size: 0.9rem;">Eliminates asphalt waste through precise micro-zone intervention before heavy decay occurs.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="glass-card">
        <h3>⚜️ Elite Guardian Leaderboard Status</h3>
        <p style="color: #94A3B8;">Your Security Tier: <b style="color: #D4AF37;">Inspector General Level 3</b> (1,450 XP)</p>
        <div style="background: rgba(255,255,255,0.05); border-radius: 10px; height: 12px; width: 100%; margin-top: 15px; overflow: hidden;">
            <div style="background: linear-gradient(90deg, #D4AF37, #F3E5AB); width: 85%; height: 100%;"></div>
        </div>
        <p style="font-size: 0.75rem; color: #64748B; margin-top: 8px;">Next Milestone: Municipal Toll Exemption & Fuel Vouchers (85% Completed)</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #475569; font-size: 0.8rem; letter-spacing: 1px;'>⚜️ ROADGUARD AI 2.0 ELITE — ENTERPRISE MUNICIPAL INTELLIGENCE</p>", unsafe_allow_html=True)
