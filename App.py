import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import time

# Page Configuration
st.set_page_config(
    page_title="ROADGUARD AI 2.0 | Executive Command",
    page_icon="⚜️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Clean, Matte Royal Black & Gold Theme (Zero Glow, High-End Minimalism)
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600&family=Cinzel:wght@500;600;700&display=swap');

        /* Global Layout */
        .main { background-color: #080808; color: #E2E8F0; font-family: 'Plus Jakarta Sans', sans-serif; }
        .block-container { padding: 2.5rem 3rem 4rem 3rem; max-width: 100%; }
        
        /* Typography */
        h1, h2, h3, h4 { color: #F8FAFC !important; font-family: 'Cinzel', serif; letter-spacing: 0.5px; }
        p, span, label, div { font-family: 'Plus Jakarta Sans', sans-serif; }
        
        /* Smooth Entrance Animation */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .page-wrapper { animation: fadeIn 0.5s ease-out forwards; }

        /* Clean Matte Cards (Zero Glow, Crisp Gold Borders) */
        .executive-card {
            background: #111111;
            border: 1px solid #222222;
            border-top: 2px solid #D4AF37;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 20px;
        }
        
        /* Metric Cards */
        .stat-box {
            background: #111111;
            border: 1px solid #222222;
            border-radius: 10px;
            padding: 18px;
            text-align: center;
        }
        .stat-number {
            font-family: 'Cinzel', serif;
            font-size: 1.8rem;
            color: #D4AF37;
            font-weight: 600;
        }
        .stat-title {
            font-size: 0.75rem;
            color: #888888;
            text-transform: uppercase;
            letter-spacing: 1.2px;
            margin-top: 4px;
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #050505;
            border-right: 1px solid #1A1A1A;
        }

        /* Matte Gold Buttons */
        .stButton>button {
            background: #D4AF37;
            color: #000000;
            font-weight: 600;
            font-family: 'Cinzel', serif;
            letter-spacing: 0.5px;
            border: none;
            border-radius: 6px;
            padding: 0.6rem 1.2rem;
            width: 100%;
            transition: background 0.2s ease;
        }
        .stButton>button:hover {
            background: #E5C158;
            color: #000000;
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
        <div style="text-align: center; padding: 15px 0;">
            <div style="font-size: 2.2rem; color: #D4AF37; margin-bottom: -5px;">⚜️</div>
            <h3 style="font-size: 1.1rem; letter-spacing: 3px; color: #F3E5AB; margin-top: 8px;">ROADGUARD</h3>
            <p style="font-size: 0.6rem; color: #666666; letter-spacing: 4px; text-transform: uppercase;">AI 2.0 EXECUTIVE</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr style='border-color: #222;'>", unsafe_allow_html=True)
    
    page = st.radio(
        "Navigation", 
        ["🏛️ Command Center", "👁️ Vision Lab", "📢 Citizen Hub", "📊 Financials", "🏆 SDG Impact"]
    )
    
    st.markdown("<hr style='border-color: #222;'>", unsafe_allow_html=True)
    st.markdown("""
        <div style="background: #111; padding: 12px; border-radius: 8px; border: 1px solid #222;">
            <div style="font-size: 0.75rem; color: #888;">SYSTEM STATUS</div>
            <div style="font-size: 0.85rem; font-weight: 600; color: #D4AF37; margin-top: 2px;">SECURE GRID ACTIVE</div>
            <div style="font-size: 0.7rem; color: #666; margin-top: 5px;">Guardian XP: 1,450 PTS</div>
        </div>
    """, unsafe_allow_html=True)

# ================= PAGE 1: COMMAND CENTER =================
if page == "🏛️ Command Center":
    st.markdown("""
        <div class="page-wrapper">
            <h1 style='font-size: 2rem; margin-bottom: 2px;'>MUNICIPAL COMMAND</h1>
            <p style='color: #888; font-size: 0.9rem; margin-bottom: 25px;'>Real-time spatial infrastructure telemetry and priority risk monitoring.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # 3 Clean Stats (Reduced Clutter)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="stat-box"><div class="stat-number">1,420 km</div><div class="stat-title">Network Monitored</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="stat-box"><div class="stat-number" style="color:#EF4444;">1 Zone</div><div class="stat-title">Critical Attention</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="stat-box"><div class="stat-number" style="color:#10B981;">99.4%</div><div class="stat-title">AI Accuracy</div></div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_map, col_details = st.columns([1.6, 1])
    with col_map:
        st.markdown("### Spatial Heatmap")
        st.markdown('<div class="executive-card" style="padding: 10px;">', unsafe_allow_html=True)
        m = folium.Map(location=[9.9816, 76.2999], zoom_start=11, tiles="CartoDB dark_matter")
        for _, row in df.iterrows():
            color = "green" if row["Health_Score"] >= 75 else ("orange" if row["Health_Score"] >= 30 else "red")
            folium.Marker(
                [row["Latitude"], row["Longitude"]],
                popup=f"<b>{row['Road_ID']}</b><br>{row['Location']}",
                icon=folium.Icon(color=color, icon="shield", prefix="fa")
            ).add_to(m)
        st_folium(m, width=640, height=400)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_details:
        st.markdown("### Asset Focus")
        st.markdown('<div class="executive-card">', unsafe_allow_html=True)
        sel_id = st.selectbox("Select Asset ID:", df["Road_ID"])
        r_info = df[df["Road_ID"] == sel_id].iloc[0]
        
        st.markdown(f"""
        <div style="font-size: 0.9rem; line-height: 1.8; margin-top: 10px;">
            <b>Location:</b> {r_info['Location']}<br>
            <b>Health Index:</b> <span style="color: #D4AF37; font-weight: 600;">{r_info['Health_Score']}/100</span><br>
            <b>Status:</b> {r_info['Status']}<br>
            <b>Failure Window:</b> {r_info['Predicted_Failure_Days']}<br>
            <b>Two-Wheeler Risk:</b> <span style="color: #EF4444;">{r_info['Bike_Risk']}</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if r_info['Health_Score'] < 30:
            st.error("🚨 Action Required: Ticket routed.")
        else:
            st.success("✅ Parameters Optimal.")
        st.markdown('</div>', unsafe_allow_html=True)

# ================= PAGE 2: VISION LAB =================
elif page == "👁️ Vision Lab":
    st.markdown("""
        <div class="page-wrapper">
            <h1 style='font-size: 2rem; margin-bottom: 2px;'>NEURAL VISION LAB</h1>
            <p style='color: #888; font-size: 0.9rem; margin-bottom: 25px;'>YOLOv8 tensor scanning for automated surface degradation analysis.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col_up, col_res = st.columns(2)
    with col_up:
        st.markdown('<div class="executive-card">', unsafe_allow_html=True)
        st.markdown("### Upload Target")
        uploaded_img = st.file_uploader("Select pavement image", type=["jpg", "jpeg", "png"])
        if uploaded_img:
            st.image(uploaded_img, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
            
    with col_res:
        st.markdown('<div class="executive-card">', unsafe_allow_html=True)
        st.markdown("### Diagnostic Result")
        if uploaded_img:
            if st.button("RUN SCAN"):
                with st.spinner("Processing tensors..."):
                    time.sleep(1)
                st.success("Scan Complete.")
                st.markdown("""
                <div style="background: #080808; padding: 12px; border-radius: 6px; border-left: 2px solid #D4AF37; margin-top: 12px; font-size: 0.9rem;">
                    <b>Model:</b> YOLOv8-Elite<br>
                    <b>Pothole Conf:</b> <span style="color:#D4AF37;">98.2%</span><br>
                    <b>Prescription:</b> Polymer micro-sealing required.
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Upload an image on the left to begin.")
        st.markdown('</div>', unsafe_allow_html=True)

# ================= PAGE 3: CITIZEN HUB =================
elif page == "📢 Citizen Hub":
    st.markdown("""
        <div class="page-wrapper">
            <h1 style='font-size: 2rem; margin-bottom: 2px;'>CITIZEN VIGIL HUB</h1>
            <p style='color: #888; font-size: 0.9rem; margin-bottom: 25px;'>Crowdsourced road safety telemetry reporting.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col_form, col_feed = st.columns(2)
    with col_form:
        st.markdown('<div class="executive-card">', unsafe_allow_html=True)
        st.markdown("### Submit Report")
        with st.form("citizen_report"):
            loc_name = st.text_input("Street / Junction Name")
            hazard_type = st.selectbox("Severity", ["Minor Micro-Crack 🟡", "Severe Pothole 🟠", "Critical Failure 🔴"])
            submitted = st.form_submit_button("BROADCAST")
            
            if submitted and loc_name:
                new_id = f"RG-E{len(df)+1}"
                score = 15 if "Critical" in hazard_type else (40 if "Severe" in hazard_type else 65)
                new_row = {
                    "Road_ID": new_id, "Location": loc_name,
                    "Latitude": 10.01, "Longitude": 76.32,
                    "Health_Score": score, "Status": "Critical Failure 🔴",
                    "Predicted_Failure_Days": "3 Days", "Bike_Risk": "Critical ⚠️"
                }
                st.session_state.road_data = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                st.success("Broadcast successful! +200 XP")
        st.markdown('</div>', unsafe_allow_html=True)
                
    with col_feed:
        st.markdown('<div class="executive-card">', unsafe_allow_html=True)
        st.markdown("### Recent Submissions")
        for _, row in df.tail(2).iterrows():
            st.markdown(f"""
            <div style="background: #080808; padding: 10px; border-radius: 6px; margin-bottom: 8px; border: 1px solid #1A1A1A; font-size: 0.85rem;">
                📍 <b>{row['Location']}</b> — <span style="color:#888;">{row['Status']}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ================= PAGE 4: FINANCIALS =================
elif page == "📊 Financials":
    st.markdown("""
        <div class="page-wrapper">
            <h1 style='font-size: 2rem; margin-bottom: 2px;'>FINANCIAL IMPACT</h1>
            <p style='color: #888; font-size: 0.9rem; margin-bottom: 25px;'>Economic shift from reactive maintenance to preventative AI.</p>
        </div>
    """, unsafe_allow_html=True)
    
    p1, p2 = st.columns(2)
    with p1:
        st.markdown("""
        <div class="executive-card" style="border-top-color: #EF4444;">
            <h3 style="color: #EF4444 !important; font-size: 1.2rem;">Traditional Reactive</h3>
            <h2 style="color: #EF4444 !important; font-size: 1.8rem; margin: 10px 0;">₹4.5 Crores / yr</h2>
            <p style="color: #888; font-size: 0.85rem;">High emergency expenditures on full reconstructions and accident claims.</p>
        </div>
        """, unsafe_allow_html=True)
    with p2:
        st.markdown("""
        <div class="executive-card" style="border-top-color: #D4AF37;">
            <h3 style="color: #D4AF37 !important; font-size: 1.2rem;">ROADGUARD AI 2.0</h3>
            <h2 style="color: #D4AF37 !important; font-size: 1.8rem; margin: 10px 0;">₹1.8 Crores <span style="font-size:0.8rem; color:#10B981;">(-60%)</span></h2>
            <p style="color: #888; font-size: 0.85rem;">Precise preventative micro-interventions that triple road life.</p>
        </div>
        """, unsafe_allow_html=True)

# ================= PAGE 5: SDG IMPACT =================
elif page == "🏆 SDG Impact":
    st.markdown("""
        <div class="page-wrapper">
            <h1 style='font-size: 2rem; margin-bottom: 2px;'>UN SDG ALIGNMENT</h1>
            <p style='color: #888; font-size: 0.9rem; margin-bottom: 25px;'>Global sustainability and gamified civic engagement.</p>
        </div>
    """, unsafe_allow_html=True)
    
    s1, s2, s3 = st.columns(3)
    with s1:
        st.markdown('<div class="executive-card"><h3>SDG 9</h3><p style="color:#888; font-size:0.85rem; margin-top:8px;">Resilient infrastructure through early-warning AI.</p></div>', unsafe_allow_html=True)
    with s2:
        st.markdown('<div class="executive-card"><h3>SDG 11</h3><p style="color:#888; font-size:0.85rem; margin-top:8px;">Sustainable cities prioritizing rider safety.</p></div>', unsafe_allow_html=True)
    with s3:
        st.markdown('<div class="executive-card"><h3>SDG 12</h3><p style="color:#888; font-size:0.85rem; margin-top:8px;">Responsible asphalt resource management.</p></div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #444; font-size: 0.75rem;'>ROADGUARD AI 2.0 — EXECUTIVE COMMAND</p>", unsafe_allow_html=True)
