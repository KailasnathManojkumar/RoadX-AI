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
    page_title="ROADX AI | Enterprise Platform",
    page_icon="⚡",
    layout="wide", # Switch to wide layout so laptops/desktops use full space comfortably
    initial_sidebar_state="collapsed"
)

# --- DEFINE-STYLE & LAPTOP-FRIENDLY CSS INJECTION ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;700&display=swap');

        /* Pure Pitch Black Theme */
        html, body, [data-testid="stAppViewContainer"] {
            background-color: #000000 !important;
            color: #FFFFFF !important;
            font-family: 'Space Grotesk', sans-serif;
        }

        /* Adaptive width for laptop screens while maintaining clean margins */
        .block-container {
            max-width: 1200px !important;
            padding-top: 2rem !important;
            padding-bottom: 6rem !important;
            padding-left: 3rem !important;
            padding-right: 3rem !important;
        }

        #MainMenu, footer, header {visibility: hidden;}

        /* Brutalist / Modern Crimson Branding */
        .brand-title {
            font-family: 'JetBrains Mono', monospace;
            font-size: 2.2rem;
            font-weight: 700;
            letter-spacing: -2px;
            color: #FFFFFF;
            text-transform: uppercase;
        }
        .brand-title span { color: #FF1E38; }

        .section-heading {
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.6rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: -1px;
            margin-top: 2.5rem;
            margin-bottom: 1rem;
            color: #FFFFFF;
        }

        /* Sleek Red-Border Cards */
        .sleek-card {
            background: #0A0A0A;
            border: 1px solid rgba(255, 30, 56, 0.25);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 20px;
            transition: all 0.2s ease;
            height: 100%;
        }
        .sleek-card:hover {
            border-color: #FF1E38;
            box-shadow: 0 0 25px rgba(255, 30, 56, 0.15);
        }

        /* Pill Buttons */
        .stButton>button {
            background-color: #FF1E38 !important;
            color: #FFFFFF !important;
            font-family: 'JetBrains Mono', monospace !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            border-radius: 6px !important;
            border: none !important;
            padding: 0.6rem 1rem !important;
            width: 100%;
            font-size: 0.85rem !important;
            letter-spacing: 1px;
        }
        .stButton>button:hover { background-color: #E0112A !important; }

        p, span, div, label { color: #A0A0A0; font-size: 1rem; line-height: 1.6; }
        h1, h2, h3 { color: #FFFFFF; }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if "current_page" not in st.session_state:
    st.session_state.current_page = "Overview"

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

if "community_reports" not in st.session_state:
    st.session_state.community_reports = [
        {"id": 1, "location": "Ulloor Junction", "type": "Pothole / Edge Break", "status": "Active"},
        {"id": 2, "location": "Kazhakkoottam Rd", "type": "Surface Fracture", "status": "Active"}
    ]

df = st.session_state.road_data
df["color"] = df["Health_Score"].apply(lambda x: [10, 185, 129, 220] if x >= 75 else ([245, 158, 11, 220] if x >= 40 else [239, 68, 68, 220]))

# --- TOP HEADER & LAPTOP-FRIENDLY HORIZONTAL CLICK NAVBAR ---
st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1A1A1A; padding-bottom: 15px; margin-bottom: 20px;">
        <div class="brand-title">ROADX<span>.AI</span></div>
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #FF1E38; letter-spacing: 2px;">SECURE HUD // DESKTOP MODE</div>
    </div>
""", unsafe_allow_html=True)

# 9-column horizontal layout so all navigation buttons sit nicely side-by-side on laptops
nav_cols = st.columns(9)
pages = ["Overview", "Command", "Vision Lab", "Acoustic", "Smart-Cure", "Carbon", "Citizen", "Cost", "Finance"]
page_icons = ["🏠 Overview", "🏛️ Command", "👁️ Vision", "🔊 Acoustic", "⚡ Smart-Cure", "🌱 Carbon", "📢 Citizen", "💰 Cost", "📊 Finance"]

for i, col in enumerate(nav_cols):
    with col:
        if st.button(page_icons[i]):
            st.session_state.current_page = pages[i]
            st.rerun()

st.markdown("<div style='margin-bottom: 20px; border-bottom: 1px solid #1A1A1A;'></div>", unsafe_allow_html=True)

page = st.session_state.current_page

# ================= PAGE ROUTING (OPTIMIZED FOR WIDE LAPTOP GRIDS) =================
if page == "Overview":
    st.markdown("""
        <div style="text-align: center; padding: 20px 0 40px 0;">
            <h1 style="font-family: 'JetBrains Mono', monospace; font-size: 3rem; font-weight: 700; color: #FFF; line-height: 1.1; margin-bottom: 15px;">
                BUILD BEYOND <span style="color: #FF1E38;">BOUNDARIES.</span>
            </h1>
            <p style="font-size: 1.15rem; max-width: 700px; margin: 0 auto;">Autonomous sub-surface infrastructure monitoring deployed for Trivandrum municipal smart corridors.</p>
        </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="sleek-card"><h2 style="color:#FF1E38; font-family:\'JetBrains Mono\'; font-size: 2.2rem;">12.4 km</h2><p>Pilot Corridor Scanned</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="sleek-card"><h2 style="color:#FFF; font-family:\'JetBrains Mono\'; font-size: 2.2rem;">99.4%</h2><p>YOLOv8 Accuracy</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="sleek-card"><h2 style="color:#FF1E38; font-family:\'JetBrains Mono\'; font-size: 2.2rem;">142 t</h2><p>Carbon Credits Minted</p></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-heading">System Core Verticals</div>', unsafe_allow_html=True)
    v1, v2 = st.columns(2)
    with v1:
        st.markdown("""
            <div class="sleek-card">
                <h3 style="color: #FFF; font-family: 'JetBrains Mono', monospace; margin-bottom: 10px;">01 // HARDWARE</h3>
                <p>Sub-surface acoustic sensors tracking soil and structural erosion shifts in real time.</p>
            </div>
        """, unsafe_allow_html=True)
    with v2:
        st.markdown("""
            <div class="sleek-card">
                <h3 style="color: #FFF; font-family: 'JetBrains Mono', monospace; margin-bottom: 10px;">02 // SOFTWARE</h3>
                <p>Real-time computer vision threat telemetry fed directly to city dispatch and emergency response units.</p>
            </div>
        """, unsafe_allow_html=True)

elif page == "Command":
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
            <div style="margin-top: 10px;">
                <b>Location:</b> {row['Location']}<br><br>
                <b>Health Score:</b> <span style="color: #FF1E38; font-weight: 700;">{row['Health_Score']} / 100</span><br><br>
                <b>Failure ETA:</b> {row['Predicted_Failure_Days']}<br><br>
                <b>2-Wheeler Risk:</b> {row['Two_Wheeler_Risk']}
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "Vision Lab":
    st.markdown('<div class="section-heading">Neural Vision Lab</div>', unsafe_allow_html=True)
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        uploaded = st.file_uploader("Upload Pavement Image", type=["jpg", "png", "jpeg"])
        if uploaded:
            st.image(uploaded, use_container_width=True)
    with col_v2:
        st.markdown('<div class="sleeks-card">', unsafe_allow_html=True)
        st.markdown("### Tensor Inference Pipeline")
        st.markdown("<p>Upload a surface image to execute multi-class defect bounding box models via YOLOv8 architecture.</p>", unsafe_allow_html=True)
        if uploaded and st.button("RUN YOLOv8 INFERENCE"):
            with st.spinner("Processing tensor weights..."):
                time.sleep(1)
            st.error("🚨 V2I Alert Broadcasted: Critical pothole detected 50m ahead.")
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "Acoustic":
    st.markdown('<div class="section-heading">Sub-Surface Acoustic Sonar</div>', unsafe_allow_html=True)
    st.markdown('<div class="sleek-card"><p>Simulates ground-penetrating acoustic resonance scans to detect underground voids and hollow pockets before surface failure occurs.</p></div>', unsafe_allow_html=True)
    if st.button("EXECUTE ACOUSTIC SWEEP"):
        with st.spinner("Analyzing sub-surface resonance..."):
            time.sleep(1)
        st.success("Sub-surface hollow identified at -1.4m depth.")

elif page == "Smart-Cure":
    st.markdown('<div class="section-heading">Smart-Cure V2I Trigger</div>', unsafe_allow_html=True)
    axle_load = st.slider("Heavy Axle Load (Tons)", 10, 50, 30)
    if st.button("TRIGGER INDUCTION PULSE"):
        with st.spinner("Broadcasting electromagnetic pulse..."):
            time.sleep(0.8)
        st.success(f"Pulse sent for {axle_load}T load. Asphalt microcapsules activated.")

elif page == "Carbon":
    st.markdown('<div class="section-heading">Carbon Credit Ledger</div>', unsafe_allow_html=True)
    c_col1, c_col2 = st.columns(2)
    with c_col1:
        st.markdown('<div class="sleek-card"><h2 style="color:#FF1E38; font-family:\'JetBrains Mono\';">142.5 tCO2e</h2><p>Avoided hot-mix bitumen emissions verified.</p></div>', unsafe_allow_html=True)
    with c_col2:
        st.markdown('<div class="sleek-card">', unsafe_allow_html=True)
        if st.button("MINT VERIFIED CREDITS"):
            st.success("Successfully minted cryptographic proof on municipal ledger.")
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "Citizen":
    st.markdown('<div class="section-heading">Citizen Vigil Hub</div>', unsafe_allow_html=True)
    cit_1, cit_2 = st.columns(2)
    with cit_1:
        with st.form("report_form"):
            loc = st.text_input("Street Name")
            if st.form_submit_button("SUBMIT REPORT") and loc:
                st.success("Hazard logged into telemetry loop!")
    with cit_2:
        st.markdown("### Active Community Reports")
        for r in st.session_state.community_reports:
            st.markdown(f"""<div class="sleek-card"><b>{r['location']}</b><br><span style="color:#FF1E38;">{r['type']}</span></div>""", unsafe_allow_html=True)

elif page == "Cost":
    st.markdown('<div class="section-heading">Severity & Cost Estimator</div>', unsafe_allow_html=True)
    w = st.slider("Width (cm)", 10, 200, 50)
    d = st.slider("Depth (cm)", 2, 50, 10)
    cost = (w * w * d / 1000) * 2.75 + 150
    st.markdown(f'<div class="sleek-card"><h2 style="color:#FF1E38;">₹{cost:.2f}</h2><p>Estimated Repair Budget</p></div>', unsafe_allow_html=True)

elif page == "Finance":
    st.markdown('<div class="section-heading">Financial Economics</div>', unsafe_allow_html=True)
    f_c1, f_c2 = st.columns(2)
    with f_c1:
        st.markdown("""
            <div class="sleek-card" style="border-color: #FF1E38;">
                <h3 style="color:#FF1E38;">Traditional Reactive</h3>
                <h2 style="color:#FF1E38; font-family:'JetBrains Mono';">₹4.5 Cr / yr</h2>
                <p>High costs from late-stage full road reconstruction.</p>
            </div>
        """, unsafe_allow_html=True)
    with f_c2:
        st.markdown("""
            <div class="sleek-card">
                <h3 style="color:#FFF;">RoadX Preventative</h3>
                <h2 style="color:#FFF; font-family:'JetBrains Mono';">₹1.8 Cr / yr</h2>
                <p>Targeted micro-interventions saving over 60% annually.</p>
            </div>
        """, unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("""
    <div style="border-top: 1px solid #1A1A1A; margin-top: 60px; padding-top: 30px; text-align: center;">
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; color: #444;">ROADX.AI © 2026 // TRIVANDRUM MUNICIPAL PILOT</div>
    </div>
""", unsafe_allow_html=True)
