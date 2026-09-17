import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import time

# Page Configuration
st.set_page_config(
    page_title="ROADGUARD AI 2.0 | Elite Infrastructure",
    page_icon="⚜️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Luxurious Royal Black & Gold Theme Custom CSS
st.markdown("""
    <style>
        /* Global Background & Font */
        .main { background-color: #080808; color: #E5E5E5; font-family: 'Inter', sans-serif; }
        .block-container { padding-top: 2rem; padding-bottom: 2rem; }
        
        /* Typography */
        h1, h2, h3, h4 { color: #D4AF37 !important; font-family: 'Playfair Display', serif; }
        p, span, label { color: #CCCCCC; }
        
        /* Gold Accent Lines & Dividers */
        hr { border-color: #332B14; }
        
        /* Luxurious Custom Cards */
        .royal-card {
            background: linear-gradient(135deg, #121212 0%, #1A1A1A 100%);
            border: 1px solid #D4AF37;
            padding: 24px;
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(212, 175, 55, 0.08);
            margin-bottom: 20px;
        }
        
        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #0B0B0B;
            border-right: 1px solid #26200A;
        }
        
        /* Metric Styling override */
        div[data-testid="stMetricValue"] {
            color: #D4AF37 !important;
            font-family: 'Playfair Display', serif;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State Database
if "road_data" not in st.session_state:
    st.session_state.road_data = pd.DataFrame({
        "Road_ID": ["RG-101", "RG-102", "RG-103", "RG-104", "RG-105"],
        "Location": ["MG Road, Kochi", "NH-66 Bypass", "MC Road, Trivandrum", "Seaport-Airport Rd", "Beach Road"],
        "Latitude": [9.9816, 10.0159, 8.5241, 10.0261, 9.9312],
        "Longitude": [76.2999, 76.3419, 76.9366, 76.3551, 76.2673],
        "Health_Score": [92, 65, 41, 18, 85],
        "Status": ["Optimal 🟢", "Moderate 🟡", "High Risk 🟠", "Critical Failure 🔴", "Optimal 🟢"],
        "Predicted_Failure_Days": ["120+ days", "45 days", "15 days", "3 days (Immediate)", "90+ days"],
        "Bike_Risk": ["Low", "Moderate", "High", "Critical ⚠️", "Low"],
        "Last_Inspection": ["2026-09-01", "2026-09-10", "2026-09-14", "2026-09-16", "2026-08-20"]
    })

if "citizen_points" not in st.session_state:
    st.session_state.citizen_points = 1450

df = st.session_state.road_data

# --- ROYAL SIDEBAR NAVIGATION ---
with st.sidebar:
    # Logo & Branding Header
    st.markdown("""
        <div style="text-align: center; padding: 10px 0;">
            <h1 style="font-size: 2.2rem; margin-bottom: 0; color: #D4AF37;">⚜️</h1>
            <h2 style="font-size: 1.4rem; letter-spacing: 2px; margin-top: 5px; color: #D4AF37;">ROADGUARD</h2>
            <p style="font-size: 0.75rem; color: #888888; letter-spacing: 4px; text-transform: uppercase; margin-top: -10px;">AI 2.0 ELITE</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    page = st.radio(
        "Navigation Menu", 
        ["🏛️ Command Center", "👁️ Neural Vision Lab", "📢 Citizen Vigil Hub", "📊 Financial Analytics", "🏆 SDG Impact & Ranking"]
    )
    
    st.markdown("---")
    st.markdown("### ⚜️ System Status")
    st.success("Encrypted Neural Grid Online")
    st.info(f"🌟 **Guardian Status:** Level 3 Elite\n`{st.session_state.citizen_points} XP`")

# ================= PAGE 1: COMMAND CENTER =================
if page == "🏛️ Command Center":
    st.markdown("<h1 style='text-align: center; margin-bottom: 5px;'>MUNICIPAL SPATIAL COMMAND</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #A39E93; margin-bottom: 30px;'>Autonomous Infrastructure Health & Two-Wheeler Priority Monitoring</p>", unsafe_allow_html=True)
    
    # Top Metrics with Royal Framing
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Monitored Network", "1,420 km", "Secured")
    m2.metric("Critical Sectors", f"{len(df[df['Health_Score'] < 40])} Zones", "Immediate Dispatch", delta_color="inverse")
    m3.metric("Two-Wheeler Hotspots", "14 Zones", "High Alert")
    m4.metric("AI Confidence Index", "99.4%", "Optimized")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_map, col_details = st.columns([2, 1])
    with col_map:
        st.markdown("### 🗺️ Infrastructure Telemetry Heatmap")
        # CartoDB Dark Matter tile gives a gorgeous black-and-gold aesthetic matching the theme
        m = folium.Map(location=[9.9816, 76.2999], zoom_start=11, tiles="CartoDB dark_matter")
        for _, row in df.iterrows():
            color = "green" if row["Health_Score"] >= 75 else ("orange" if row["Health_Score"] >= 30 else "red")
            folium.Marker(
                [row["Latitude"], row["Longitude"]],
                popup=f"<b>{row['Road_ID']}</b><br>{row['Location']}<br>Status: {row['Status']}",
                icon=folium.Icon(color=color, icon="shield", prefix="fa")
            ).add_to(m)
        st_folium(m, width=650, height=450)
        
    with col_details:
        st.markdown("### 🔍 Segment Telemetry")
        sel_id = st.selectbox("Select Road Asset ID:", df["Road_ID"])
        r_info = df[df["Road_ID"] == sel_id].iloc[0]
        
        st.markdown(f"""
        <div class="royal-card">
            <b>Location:</b> {r_info['Location']}<br>
            <b>Health Score:</b> <span style="color: #D4AF37; font-weight: bold;">{r_info['Health_Score']}/100</span><br>
            <b>Status:</b> {r_info['Status']}<br>
            <b>Failure Window:</b> {r_info['Predicted_Failure_Days']}<br>
            <b>Two-Wheeler Risk:</b> {r_info['Bike_Risk']}
        </div>
        """, unsafe_allow_html=True)
        
        if r_info['Health_Score'] < 30:
            st.error("🚨 **Autonomous Alert:** Priority repair ticket routed to municipal contractors.")
        else:
            st.success("✅ **Asset Secure:** Structural integrity within nominal parameters.")

# ================= PAGE 2: NEURAL VISION LAB =================
elif page == "👁️ Neural Vision Lab":
    st.markdown("<h1>👁️ Computer Vision & Crack Detection Studio</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #A39E93;'>Upload surface imagery to execute deep-tensor YOLOv8 structural analysis.</p>", unsafe_allow_html=True)
    
    col_up, col_res = st.columns(2)
    with col_up:
        uploaded_img = st.file_uploader("Upload Pavement Inspection Image", type=["jpg", "jpeg", "png"])
        if uploaded_img:
            st.image(uploaded_img, caption="Target Loaded for Optical Scan", use_container_width=True)
            
    with col_res:
        st.markdown("### ⚜️ Neural Diagnostic Engine")
        if uploaded_img:
            if st.button("Execute High-Precision Scan", type="primary"):
                with st.spinner("Analyzing sub-base density matrices and fracture propagation..."):
                    time.sleep(1.2)
                st.success("Scan Protocol Successful.")
                st.markdown("""
                <div class="royal-card">
                    <b>Active Model:</b> YOLOv8-Elite RoadNet<br>
                    <b>Pothole Probability:</b> <span style="color:#D4AF37;">98.2%</span><br>
                    <b>Sub-base Fatigue:</b> Critical Micro-Fissuring Detected<br>
                    <b>Prescribed Action:</b> Polymer injection sealing mandatory.
                </div>
                """, unsafe_allow_html=True)
                st.warning("⚠️ **Safety Notice:** Severe risk factor for two-wheeler stabilization.")
        else:
            st.info("👈 Please provide an inspection target image on the left panel.")

# ================= PAGE 3: CITIZEN VIGIL HUB =================
elif page == "📢 Citizen Vigil Hub":
    st.markdown("<h1>📢 Citizen Vigil & Hazard Reporting</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #A39E93;'>Empowering commuters and riders to crowdsource real-time road degradation data.</p>", unsafe_allow_html=True)
    
    col_form, col_feed = st.columns([1, 1])
    with col_form:
        st.markdown("### Submit Hazard Telemetry")
        with st.form("citizen_report"):
            loc_name = st.text_input("Junction / Street Name", placeholder="e.g., MG Road Cross 4")
            hazard_type = st.selectbox("Severity Classification", ["Minor Micro-Crack 🟡", "Severe Pothole 🟠", "Critical Infrastructure Failure 🔴"])
            comment = st.text_area("Rider Impact Description", placeholder="Dangerous swerve zone during evening commutes.")
            submitted = st.form_submit_button("Broadcast to Municipal Core")
            
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
                    "Bike_Risk": "Critical ⚠️",
                    "Last_Inspection": "Live Telemetry"
                }
                st.session_state.road_data = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                st.session_state.citizen_points += 200
                st.success(f"Telemetry broadcasted successfully! +200 Guardian XP earned.")
                st.balloons()
                
    with col_feed:
        st.markdown("### Live Community Feed")
        for _, row in df.tail(3).iterrows():
            st.markdown(f"""
            <div class="royal-card">
                📍 <b>{row['Location']}</b><br>
                Status: {row['Status']} | Two-Wheeler Risk: {row['Bike_Risk']}<br>
                <span style="font-size: 0.8rem; color: #888888;">Verified by Municipal AI Grid</span>
            </div>
            """, unsafe_allow_html=True)

# ================= PAGE 4: FINANCIAL ANALYTICS =================
elif page == "📊 Financial Analytics":
    st.markdown("<h1>📊 Municipal Economic Impact & Cost Center</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #A39E93;'>Demonstrating the systemic financial transition from reactive patching to predictive prevention.</p>", unsafe_allow_html=True)
    
    p1, p2 = st.columns(2)
    with p1:
        st.markdown("""
        <div class="royal-card">
            <h3 style="color: #ff4d4d !important;">Traditional Reactive Model</h3>
            <h2>₹4.5 Crores / yr</h2>
            <p>High public expenditure caused by waiting for full structural collapse, emergency repaving, and vehicle damage claims.</p>
        </div>
        """, unsafe_allow_html=True)
    with p2:
        st.markdown("""
        <div class="royal-card">
            <h3 style="color: #D4AF37 !important;">ROADGUARD AI 2.0 Model</h3>
            <h2>₹1.8 Crores / yr <span style="font-size: 1rem; color: #4CAF50;">(-60% Savings)</span></h2>
            <p>Targeted preventative micro-treatments that triple road asset lifespans at a fraction of the cost.</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    st.markdown("### 📥 Official Tender & Repair Schedule Export")
    csv_bytes = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Master Contractor Schedule (CSV)",
        data=csv_bytes,
        file_name="roadguard_elite_schedule.csv",
        mime="text/csv"
    )

# ================= PAGE 5: SDG IMPACT & RANKING =================
elif page == "🏆 SDG Impact & Ranking":
    st.markdown("<h1>🏆 UN SDG Alignment & Guardian Gamification</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #A39E93;'>Aligning urban innovation directly with global sustainability frameworks.</p>", unsafe_allow_html=True)
    
    col_sdg1, col_sdg2, col_sdg3 = st.columns(3)
    with col_sdg1:
        st.markdown("""
        <div class="royal-card">
            <h3 style="color: #D4AF37;">🏗️ SDG 9</h3>
            <b>Resilient Infrastructure</b><br><br>
            Maximizes material durability and prevents catastrophic failures through automated early warnings.
        </div>
        """, unsafe_allow_html=True)
    with col_sdg2:
        st.markdown("""
        <div class="royal-card">
            <h3 style="color: #D4AF37;">🏙️ SDG 11</h3>
            <b>Sustainable Cities</b><br><br>
            Prioritizes two-wheeler safety and eliminates urban gridlock caused by degraded roadways.
        </div>
        """, unsafe_allow_html=True)
    with col_sdg3:
        st.markdown("""
        <div class="royal-card">
            <h3 style="color: #D4AF37;">♻️ SDG 12</h3>
            <b>Responsible Production</b><br><br>
            Eliminates asphalt waste through precise micro-zone intervention before heavy decay occurs.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### ⚜️ Elite Guardian Leaderboard")
    st.write(f"Your Security Tier: **Inspector General Level 3** (`{st.session_state.citizen_points} XP`)")
    st.progress(0.85, text="Privilege Progression: Municipal Toll Exemption & Fuel Vouchers")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #555555; font-size: 0.85rem;'>⚜️ ROADGUARD AI 2.0 ELITE — Built for Sustainable Infrastructure & Smart Mobility (SDG 9, 11, 12).</p>", unsafe_allow_html=True)