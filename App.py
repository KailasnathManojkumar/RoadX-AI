import os
import streamlit as st
import pandas as pd
import pydeck as pdk
import time

# --- CONFIGURATION ---
MAPBOX_TOKEN = "pk.eyJ1Ijoia2FpbGFzbmF0aDEyMyIsImEiOiJjbXU4Zm93YmEwdXdnMnlzMmdnbTQyNzNoIn0.0yYdaXOauUT-_A6VaeuMyg"
os.environ["MAPBOX_API_KEY"] = MAPBOX_TOKEN
pdk.settings.mapbox_api_key = MAPBOX_TOKEN

st.set_page_config(
    page_title="ROADX AI | Massive Infrastructure Suite",
    page_icon="⚜️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- EXPANSIVE "BIG WEBSITE" CSS INJECTION ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=Cinzel:wght@600;700;800&display=swap');

        /* Full Screen Expansion */
        html { scroll-behavior: smooth; }
        .main { background-color: #050508; color: #F1F5F9; font-family: 'Outfit', sans-serif; }
        
        .block-container { 
            padding: 0rem !important; 
            max-width: 100% !important; 
        }
        
        #MainMenu, footer, header {visibility: hidden;}

        /* Massive Cinematic Hero Section */
        .massive-hero {
            background: radial-gradient(circle at 50% 10%, #1a1500 0%, #050508 70%);
            padding: 140px 10% 100px 10%;
            text-align: center;
            border-bottom: 1px solid rgba(212, 175, 55, 0.15);
        }
        
        .massive-title {
            font-family: 'Cinzel', serif;
            font-size: 4.8rem;
            font-weight: 800;
            letter-spacing: -1px;
            background: linear-gradient(135deg, #FFFFFF 20%, #D4AF37 80%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 24px;
            line-height: 1.1;
        }

        .massive-subtitle {
            font-size: 1.4rem;
            color: #94A3B8;
            max-width: 850px;
            margin: 0 auto 50px auto;
            line-height: 1.7;
        }

        /* Massive Section Containers */
        .content-section {
            padding: 90px 8%;
            border-bottom: 1px solid rgba(255, 255, 255, 0.04);
        }

        .section-header {
            font-family: 'Cinzel', serif;
            font-size: 2.8rem;
            color: #FFFFFF;
            margin-bottom: 16px;
            font-weight: 700;
        }

        .section-desc {
            font-size: 1.15rem;
            color: #94A3B8;
            margin-bottom: 50px;
            max-width: 700px;
        }

        /* Huge Metric Cards */
        .huge-stat-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 30px;
            margin-bottom: 60px;
        }

        .huge-stat-card {
            background: linear-gradient(145deg, rgba(20, 20, 25, 0.7) 0%, rgba(8, 8, 12, 0.9) 100%);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-top: 3px solid #D4AF37;
            border-radius: 20px;
            padding: 35px 30px;
            text-align: left;
            box-shadow: 0 20px 50px rgba(0,0,0,0.6);
        }

        .huge-stat-number {
            font-family: 'Cinzel', serif;
            font-size: 3.2rem;
            color: #D4AF37;
            font-weight: 800;
            line-height: 1;
            margin-bottom: 12px;
        }

        .huge-stat-label {
            font-size: 0.85rem;
            color: #94A3B8;
            text-transform: uppercase;
            letter-spacing: 2px;
            font-weight: 600;
        }

        /* Grand Feature Cards */
        .grand-card {
            background: linear-gradient(145deg, rgba(15, 15, 20, 0.8) 0%, rgba(5, 5, 8, 0.95) 100%);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 24px;
            padding: 50px;
            margin-bottom: 30px;
            box-shadow: 0 25px 60px rgba(0,0,0,0.5);
            transition: transform 0.3s ease, border-color 0.3s ease;
        }
        .grand-card:hover {
            transform: translateY(-6px);
            border-color: rgba(212, 175, 55, 0.4);
        }

        /* Custom Streamlit Button Expansion */
        .stButton>button {
            background: linear-gradient(135deg, #D4AF37 0%, #AA8C2C 100%) !important;
            color: #050508 !important;
            font-weight: 800 !important;
            font-family: 'Cinzel', serif !important;
            letter-spacing: 1.5px !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 0.9rem 2rem !important;
            font-size: 1.05rem !important;
            box-shadow: 0 10px 30px rgba(212, 175, 55, 0.3) !important;
            width: 100%;
        }
    </style>
""", unsafe_allow_html=True)

# Session state setup
if "current_page" not in st.session_state:
    st.session_state.current_page = "🏠 Overview"

# Dummy Data
df = pd.DataFrame({
    "Road_ID": ["TVM-01", "TVM-02", "TVM-03", "TVM-04", "TVM-05"],
    "Location": ["MC Road, Ulloor", "NH-66 Bypass", "Kowdiar Square", "Pattom Corridor", "East Fort Ring"],
    "Latitude": [8.5331, 8.5645, 8.5175, 8.5208, 8.4842],
    "Longitude": [76.9317, 76.8782, 76.9551, 76.9382, 76.9472],
    "Health_Score": [88, 42, 94, 28, 65],
    "Status": ["Optimal", "Moderate Risk", "Optimal", "Critical Failure", "Moderate Risk"],
})
df["color"] = df["Health_Score"].apply(lambda x: [10, 185, 129, 220] if x >= 75 else ([245, 158, 11, 220] if x >= 40 else [239, 68, 68, 220]))

# --- TOP MASSIVE NAVBAR ---
st.markdown("""
    <div style="background: rgba(5, 5, 8, 0.9); backdrop-filter: blur(20px); border-bottom: 1px solid rgba(255,255,255,0.06); padding: 22px 8%; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 99999;">
        <div style="font-family: 'Cinzel', serif; font-size: 1.4rem; font-weight: 800; color: #D4AF37; letter-spacing: 3px;">ROADX<span style="color:#FFF;">.AI</span></div>
        <div style="color: #94A3B8; font-size: 0.9rem; font-weight: 500; letter-spacing: 1px;">ENTERPRISE INFRASTRUCTURE PLATFORM</div>
    </div>
""", unsafe_allow_html=True)

# Navigation Bar Selector
nav_cols = st.columns([4, 1])
with nav_cols[0]:
    pages = ["🏠 Overview", "🏛️ Command Center", "👁️ Neural Vision Lab", "🔊 Acoustic Sonar", "📊 Economics"]
    selected_page = st.selectbox("Navigation Gateway", pages, label_visibility="collapsed")
with nav_cols[1]:
    if st.button("JUMP TO MODULE"):
        st.session_state.current_page = selected_page
        st.rerun()

st.session_state.current_page = selected_page

# ================= HOMEPAGE / OVERVIEW =================
if st.session_state.current_page == "🏠 Overview":
    # 1. Massive Hero Section
    st.markdown("""
        <div class="massive-hero">
            <div class="massive-title">Autonomous Infrastructure Intelligence</div>
            <div class="massive-subtitle">Deploying real-time sub-surface telemetry, YOLOv8 computer vision, and multi-vehicle risk modeling across global municipal corridors.</div>
        </div>
    """, unsafe_allow_html=True)

    # 2. Huge Metric Counters Grid (replaces standard small metrics)
    st.markdown("""
        <div class="content-section" style="padding-bottom: 20px;">
            <div class="huge-stat-grid">
                <div class="huge-stat-card">
                    <div class="huge-stat-number">12.4</div>
                    <div class="huge-stat-label">Kilometers Monitored</div>
                </div>
                <div class="huge-stat-card">
                    <div class="huge-stat-number" style="color: #EF4444;">1</div>
                    <div class="huge-stat-label">Critical Asset Alerts</div>
                </div>
                <div class="huge-stat-card">
                    <div class="huge-stat-number" style="color: #10B981;">99.4%</div>
                    <div class="huge-stat-label">Neural Scan Accuracy</div>
                </div>
                <div class="huge-stat-card">
                    <div class="huge-stat-number">142 t</div>
                    <div class="huge-stat-label">Carbon Credits Minted</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 3. Expansive Feature Showcase Section
    st.markdown("""
        <div class="content-section">
            <div class="section-header">Enterprise Architectural Modules</div>
            <div class="section-desc">Engineered from the ground up for sub-millisecond edge data execution loops and municipal command oversight.</div>
    """, unsafe_allow_html=True)

    f1, f2 = st.columns(2, gap="large")
    with f1:
        st.markdown("""
            <div class="grand-card">
                <h3 style="font-family: 'Cinzel', serif; font-size: 1.6rem; color: #FFF; margin-bottom: 15px;">🏛️ Municipal Command Center</h3>
                <p style="color: #94A3B8; font-size: 1.05rem; line-height: 1.7; margin-bottom: 25px;">Real-time GIS spatial mapping powered by Mapbox integration, tracking structural degradation indices down to individual road segments.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("LAUNCH COMMAND MODULE", key="btn_c1"):
            st.session_state.current_page = "🏛️ Command Center"
            st.rerun()

    with f2:
        st.markdown("""
            <div class="grand-card">
                <h3 style="font-family: 'Cinzel', serif; font-size: 1.6rem; color: #FFF; margin-bottom: 15px;">🔊 Sub-Surface Acoustic Lab</h3>
                <p style="color: #94A3B8; font-size: 1.05rem; line-height: 1.7; margin-bottom: 25px;">Simulates ground-penetrating acoustic resonance scans to forecast hidden underground sinkholes weeks before surface cracking occurs.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("LAUNCH ACOUSTIC LAB", key="btn_c2"):
            st.session_state.current_page = "🔊 Acoustic Sonar"
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ================= COMMAND CENTER =================
elif st.session_state.current_page == "🏛️ Command Center":
    st.markdown("""
        <div class="content-section">
            <div class="section-header">Municipal Command Grid</div>
            <div class="section-desc">Spatial telemetry overview across Trivandrum test deployment sectors.</div>
        </div>
    """, unsafe_allow_html=True)
    
    m_col1, m_col2 = st.columns([1.6, 1], gap="large")
    with m_col1:
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position=["Longitude", "Latitude"],
            get_fill_color="color",
            get_radius=400,
            pickable=True,
        )
        view_state = pdk.ViewState(latitude=8.5241, longitude=76.9366, zoom=12, pitch=30)
        deck = pdk.Deck(layers=[layer], initial_view_state=view_state, map_style="mapbox://styles/mapbox/dark-v10")
        st.pydeck_chart(deck, use_container_width=True)
        
    with m_col2:
        st.markdown("""
            <div class="grand-card">
                <h3 style="font-family: 'Cinzel', serif; font-size: 1.4rem; color: #FFF; margin-bottom: 20px;">Asset Diagnostics</h3>
        """, unsafe_allow_html=True)
        sel_id = st.selectbox("Select Asset Corridor", df["Road_ID"])
        row = df[df["Road_ID"] == sel_id].iloc[0]
        st.markdown(f"""
            <div style="font-size: 1.05rem; line-height: 2.2; color: #94A3B8; margin-top: 15px;">
                <b>Location:</b> {row['Location']}<br>
                <b>Health Score:</b> <span style="color: #D4AF37; font-weight: 800;">{row['Health_Score']} / 100</span><br>
                <b>Status:</b> {row['Status']}
            </div>
            </div>
        """, unsafe_allow_html=True)

# ================= OTHER MODULES PLACEHOLDERS =================
elif st.session_state.current_page == "👁️ Neural Vision Lab":
    st.markdown('<div class="content-section"><div class="section-header">Neural Vision Lab</div><div class="section-desc">YOLOv8 automated surface degradation scan pipeline.</div></div>', unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload Pavement Image", type=["jpg", "png", "jpeg"])
    if uploaded:
        st.image(uploaded, width=600)

elif st.session_state.current_page == "🔊 Acoustic Sonar":
    st.markdown('<div class="content-section"><div class="section-header">Sub-Surface Acoustic Sonar Lab</div><div class="section-desc">Detecting hidden sub-base voids using acoustic telemetry.</div></div>', unsafe_allow_html=True)
    if st.button("RUN ACOUSTIC SWEEP"):
        with st.spinner("Analyzing sub-surface frequency shifts..."):
            time.sleep(1)
        st.success("Analysis Complete: Sub-surface hollow detected at -1.5m depth.")

elif st.session_state.current_page == "📊 Economics":
    st.markdown('<div class="content-section"><div class="section-header">Financial Economics</div><div class="section-desc">Comparative analysis of reactive vs preventative municipal spending.</div></div>', unsafe_allow_html=True)
    e1, e2 = st.columns(2, gap="large")
    with e1:
        st.markdown('<div class="grand-card"><h3 style="color:#EF4444;">Traditional Reactive</h3><h1 style="color:#EF4444; font-size:2.8rem;">₹4.5 Cr / yr</h1><p style="color:#94A3B8;">High costs from late-stage full relaying.</p></div>', unsafe_allow_html=True)
    with e2:
        st.markdown('<div class="grand-card"><h3 style="color:#D4AF37;">RoadX Preventative</h3><h1 style="color:#D4AF37; font-size:2.8rem;">₹1.8 Cr / yr</h1><p style="color:#94A3B8;">Targeted micro-interventions saving 60%.</p></div>', unsafe_allow_html=True)
