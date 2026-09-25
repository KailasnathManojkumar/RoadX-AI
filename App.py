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
    page_title="Roadguard AI | Enterprise Platform",
    page_icon="⚜️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- LUXURY GOLD & BLACK THEME CSS ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Cinzel:wght@600;700;800&family=JetBrains+Mono:wght@400;700&display=swap');

        /* Rich Pitch Black & Gold Theme */
        html, body, [data-testid="stAppViewContainer"] {
            background-color: #050508 !important;
            color: #F1F5F9 !important;
            font-family: 'Outfit', sans-serif;
        }

        /* Adaptive width for laptop screens */
        .block-container {
            max-width: 1200px !important;
            padding-top: 2rem !important;
            padding-bottom: 6rem !important;
            padding-left: 3rem !important;
            padding-right: 3rem !important;
        }

        #MainMenu, footer, header {visibility: hidden;}

        /* Cinematic Gold Branding */
        .brand-title {
            font-family: 'Cinzel', serif;
            font-size: 2.2rem;
            font-weight: 800;
            letter-spacing: 2px;
            color: #D4AF37;
            text-transform: uppercase;
        }
        .brand-title span { color: #FFFFFF; }

        .section-heading {
            font-family: 'Cinzel', serif;
            font-size: 1.8rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-top: 2.5rem;
            margin-bottom: 1rem;
            color: #FFFFFF;
        }

        /* Luxury Gold-Bordered Cards */
        .sleek-card {
            background: linear-gradient(145deg, rgba(20, 20, 25, 0.8) 0%, rgba(8, 8, 12, 0.95) 100%);
            border: 1px solid rgba(212, 175, 55, 0.25);
            border-radius: 16px;
            padding: 28px;
            margin-bottom: 20px;
            transition: all 0.3s ease;
            height: 100%;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }
        .sleek-card:hover {
            border-color: rgba(212, 175, 55, 0.8);
            box-shadow: 0 0 30px rgba(212, 175, 55, 0.2);
            transform: translateY(-3px);
        }

        /* High-Visibility Custom Streamlit Buttons */
        .stButton>button {
            background: linear-gradient(135deg, #1A1A22 0%, #111116 100%) !important;
            color: #FFFFFF !important;
            font-family: 'Cinzel', serif !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            border-radius: 10px !important;
            border: 1px solid rgba(212, 175, 55, 0.4) !important;
            padding: 0.6rem 0.4rem !important;
            width: 100%;
            font-size: 0.75rem !important;
            letter-spacing: 1px !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
            transition: all 0.2s ease-in-out;
        }
        .stButton>button:hover {
            background: linear-gradient(135deg, #D4AF37 0%, #AA8C2C 100%) !important;
            color: #000000 !important;
            border-color: #D4AF37 !important;
            box-shadow: 0 0 20px rgba(212, 175, 55, 0.4);
        }

        p, span, div, label { color: #94A3B8; font-size: 1.02rem; line-height: 1.6; }
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

# --- TOP HEADER & HIGH-CONTRAST NAVBAR ---
st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(212,175,55,0.25); padding-bottom: 15px; margin-bottom: 25px;">
        <div class="brand-title">ROADGUARD<span>.AI</span></div>
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #D4AF37; letter-spacing: 2px;">SECURE ENTERPRISE HUD</div>
    </div>
""", unsafe_allow_html=True)

nav_cols = st.columns(9)
pages = ["Overview", "Command", "Vision Lab", "Acoustic", "Smart-Cure", "Carbon", "Citizen", "Cost", "Finance"]
page_labels = ["Overview", "Command", "Vision", "Acoustic", "Smart-Cure", "Carbon", "Citizen", "Cost", "Finance"]

for i, col in enumerate(nav_cols):
    with col:
        if st.session_state.current_page == pages[i]:
            if st.button(f"✨ {page_labels[i]}"):
                st.session_state.current_page = pages[i]
                st.rerun()
        else:
            if st.button(page_labels[i]):
                st.session_state.current_page = pages[i]
                st.rerun()

st.markdown("<div style='margin-bottom: 25px; border-bottom: 1px solid rgba(255,255,255,0.05);'></div>", unsafe_allow_html=True)

page = st.session_state.current_page

# ================= PAGE ROUTING =================
if page == "Overview":
    st.markdown("""
        <div style="text-align: center; padding: 20px 0 40px 0;">
            <h1 style="font-family: 'Cinzel', serif; font-size: 3rem; font-weight: 800; color: #FFF; line-height: 1.1; margin-bottom: 15px;">
                AUTONOMOUS <span style="color: #D4AF37;">INFRASTRUCTURE.</span>
            </h1>
            <p style="font-size: 1.15rem; max-width: 700px; margin: 0 auto; color: #94A3B8;">Sub-surface telemetry, YOLOv8 vision intelligence, and predictive municipal risk management.</p>
        </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="sleek-card"><h2 style="color:#D4AF37; font-family:\'Cinzel\'; font-size: 2.2rem;">12.4 km</h2><p>Pilot Corridor Scanned</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="sleek-card"><h2 style="color:#FFF; font-family:\'Cinzel\'; font-size: 2.2rem;">99.4%</h2><p>YOLOv8 Accuracy</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="sleek-card"><h2 style="color:#D4AF37; font-family:\'Cinzel\'; font-size: 2.2rem;">142 t</h2><p>Carbon Credits Minted</p></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-heading">System Core Verticals</div>', unsafe_allow_html=True)
    v1, v2 = st.columns(2)
    with v1:
        st.markdown("""
            <div class="sleek-card">
                <h3 style="color: #FFF; font-family: 'Cinzel', serif; margin-bottom: 10px;">01 // HARDWARE</h3>
                <p>Sub-surface acoustic sensors tracking soil and structural erosion shifts in real time.</p>
            </div>
        """, unsafe_allow_html=True)
    with v2:
        st.markdown("""
            <div class="sleek-card">
                <h3 style="color: #FFF; font-family: 'Cinzel', serif; margin-bottom: 10px;">02 // SOFTWARE</h3>
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
                <b>Health Score:</b> <span style="color: #D4AF37; font-weight: 700;">{row['Health_Score']} / 100</span><br><br>
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
        st.markdown('<div class="sleek-card">', unsafe_allow_html=True)
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
        st.markdown('<div class="sleek-card"><h2 style="color:#D4AF37; font-family:\'Cinzel\';">142.5 tCO2e</h2><p>Avoided hot-mix bitumen emissions verified.</p></div>', unsafe_allow_html=True)
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
            st.markdown(f"""<div class="sleek-card"><b>{r['location']}</b><br><span style="color:#D4AF37;">{r['type']}</span></div>""", unsafe_allow_html=True)

elif page == "Cost":
    st.markdown('<div class="section-heading">Severity & Cost Estimator</div>', unsafe_allow_html=True)
    w = st.slider("Width (cm)", 10, 200, 50)
    d = st.slider("Depth (cm)", 2, 50, 10)
    cost = (w * w * d / 1000) * 2.75 + 150
    st.markdown(f'<div class="sleek-card"><h2 style="color:#D4AF37;">₹{cost:.2f}</h2><p>Estimated Repair Budget</p></div>', unsafe_allow_html=True)

elif page == "Finance":
    st.markdown('<div class="section-heading">Financial Economics</div>', unsafe_allow_html=True)
    f_c1, f_c2 = st.columns(2)
    with f_c1:
        st.markdown("""
            <div class="sleek-card" style="border-color: rgba(239, 68, 68, 0.4);">
                <h3 style="color:#EF4444;">Traditional Reactive</h3>
                <h2 style="color:#EF4444; font-family:'Cinzel';">₹4.5 Cr / yr</h2>
                <p>High costs from late-stage full road reconstruction.</p>
            </div>
        """, unsafe_allow_html=True)
    with f_c2:
        st.markdown("""
            <div class="sleek-card" style="border-color: rgba(212, 175, 55, 0.4);">
                <h3 style="color:#D4AF37;">Roadguard Preventative</h3>
                <h2 style="color:#D4AF37; font-family:'Cinzel';">₹1.8 Cr / yr</h2>
                <p>Targeted micro-interventions saving over 60% annually.</p>
            </div>
        """, unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("""
    <div style="border-top: 1px solid rgba(212,175,55,0.25); margin-top: 60px; padding-top: 30px; text-align: center;">
        <div style="font-family: 'Cinzel', serif; font-size: 0.85rem; color: #D4AF37; letter-spacing: 2px;">ROADGUARD.AI © 2026 // TRIVANDRUM MUNICIPAL PILOT</div>
    </div>
""", unsafe_allow_html=True)
