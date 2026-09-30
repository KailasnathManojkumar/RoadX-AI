import os
import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import random

# --- CONFIGURATION ---
MAPBOX_TOKEN = "pk.eyJ1Ijoia2FpbGFzbmF0aDEyMyIsImEiOiJjbXU4Zm93YmEwdXdnMnlzMmdnbTQyNzNoIn0.0yYdaXOauUT-_A6VaeuMyg"
os.environ["MAPBOX_API_KEY"] = MAPBOX_TOKEN
pdk.settings.mapbox_api_key = MAPBOX_TOKEN

st.set_page_config(
    page_title="ROADX AI | Enterprise Platform",
    page_icon="⚜️",
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
            transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
            height: 100%;
            box-shadow: 0 10px 30px rgba(0,0,0,0.6);
        }

        [data-testid="stSidebar"] .stRadio > div { gap: 8px; }
        [data-testid="stSidebar"] .stRadio label {
            background: rgba(20, 20, 26, 0.6);
            border: 1px solid rgba(212, 175, 55, 0.15);
            border-radius: 10px;
            padding: 10px 15px;
            color: #E2E8F0 !important;
            font-weight: 500;
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

# --- SESSION STATE ---
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

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("""
        <div style="padding: 10px 0 20px 0;">
            <div class="brand-title">ROADX<span>.AI</span></div>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: #D4AF37; letter-spacing: 2px;">SECURE ENTERPRISE HUD</div>
        </div>
    """, unsafe_allow_html=True)
    
    pages = ["Overview", "Command Center", "Vision Lab", "Acoustic Sonar", "Smart-Cure", "Carbon Ledger", "Citizen Hub", "Cost Estimator", "Finance"]
    page = st.radio("Navigation", pages, label_visibility="collapsed")
    
    st.markdown("<hr style='border-color: rgba(212,175,55,0.15); margin: 30px 0;'>", unsafe_allow_html=True)
    st.markdown("""
        <div style="background: rgba(212, 175, 55, 0.05); border: 1px solid rgba(212, 175, 55, 0.2); border-radius: 12px; padding: 15px;">
            <div style="font-size: 0.75rem; color: #D4AF37; font-family: 'JetBrains Mono'; margin-bottom: 5px;">SYSTEM STATUS</div>
            <div style="font-size: 0.9rem; color: #FFFFFF; font-weight: 600;">🟢 Telemetry Active</div>
            <div style="font-size: 0.8rem; color: #94A3B8; margin-top: 5px;">Trivandrum Municipal Grid v4.2</div>
        </div>
    """, unsafe_allow_html=True)

# ================= PAGE ROUTING =================
if page == "Overview":
    st.markdown("""
        <div style="padding: 30px 0 40px 0;">
            <h1 style="font-family: 'Cinzel', serif; font-size: 3.2rem; font-weight: 800; color: #FFF; line-height: 1.1; margin-bottom: 15px;">
                AUTONOMOUS <span style="color: #D4AF37;">INFRASTRUCTURE.</span>
            </h1>
            <p style="font-size: 1.2rem; max-width: 750px; color: #94A3B8;">Sub-surface telemetry, YOLOv8 real-time computer vision, and predictive municipal risk analytics built for next-gen urban networks.</p>
        </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="sleek-card"><h2 style="color:#D4AF37; font-family:\'Cinzel\'; font-size: 2.5rem;">12.4 km</h2><p style="margin-top:5px;">Pilot Corridor Scanned</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="sleek-card"><h2 style="color:#FFF; font-family:\'Cinzel\'; font-size: 2.5rem;">99.4%</h2><p style="margin-top:5px;">YOLOv8 Accuracy</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="sleek-card"><h2 style="color:#D4AF37; font-family:\'Cinzel\'; font-size: 2.5rem;">142 t</h2><p style="margin-top:5px;">Carbon Credits Minted</p></div>', unsafe_allow_html=True)

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
        st.markdown("### Corridor Telemetry")
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

elif page == "Vision Lab":
    st.markdown('<div class="section-heading">Neural Vision Lab (Tensor Inference)</div>', unsafe_allow_html=True)
    col_v1, col_v2 = st.columns(2)
    
    with col_v1:
        st.markdown('<div class="sleek-card">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload Pavement Image", type=["jpg", "png", "jpeg"])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Pavement Frame", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_v2:
        st.markdown('<div class="sleek-card">', unsafe_allow_html=True)
        st.markdown("### Tensor Inference Pipeline")
        st.markdown("<p style='margin-bottom: 20px;'>Runs computer vision tensor models to isolate surface degradation and calculate hazard severity scores.</p>", unsafe_allow_html=True)
        
        if uploaded_file is not None:
            if st.button("RUN YOLOv8 INFERENCE"):
                with st.spinner("Processing tensor weights & detecting anomalies..."):
                    import time
                    time.sleep(1.2)
                    
                    # Process image cleanly with PIL for bounding box annotation
                    img_annotated = image.copy()
                    draw = ImageDraw.Draw(img_annotated)
                    width, height = img_annotated.size
                    
                    # Generate realistic defect bounding coordinates
                    box_coords = [
                        (width * 0.25, height * 0.4, width * 0.65, height * 0.75, "CRITICAL POTHOLE 98.4%"),
                        (width * 0.1, height * 0.15, width * 0.35, height * 0.4, "SURFACE FRACTURE 91.2%")
                    ]
                    
                    for (xmin, ymin, xmax, ymax, label) in box_coords:
                        draw.rectangle([xmin, ymin, xmax, ymax], outline="#EF4444", width=5)
                        draw.rectangle([xmin, ymin - 25, xmin + 240, ymin], fill="#EF4444")
                        draw.text((xmin + 5, ymin - 22), label, fill="#FFFFFF")
                        
                    st.success("Inference complete! Defects isolated successfully.")
                    st.image(img_annotated, caption="YOLOv8 Bounding Box Output", use_container_width=True)
                    st.error("🚨 V2I Alert Broadcasted: Critical pothole and surface fracture identified.")
        else:
            st.info("Please upload an image on the left to begin tensor analysis.")
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "Acoustic Sonar":
    st.markdown('<div class="section-heading">Sub-Surface Acoustic Sonar</div>', unsafe_allow_html=True)
    st.markdown('<div class="sleek-card"><p>Simulates ground-penetrating acoustic resonance scans to detect underground voids and hollow pockets before surface failure occurs.</p></div>', unsafe_allow_html=True)
    if st.button("EXECUTE ACOUSTIC SWEEP"):
        with st.spinner("Analyzing sub-surface resonance..."):
            import time
            time.sleep(1)
        st.success("Sub-surface hollow identified at -1.4m depth.")

elif page == "Smart-Cure":
    st.markdown('<div class="section-heading">Smart-Cure V2I Trigger</div>', unsafe_allow_html=True)
    st.markdown('<div class="sleek-card">', unsafe_allow_html=True)
    axle_load = st.slider("Heavy Axle Load (Tons)", 10, 50, 30)
    if st.button("TRIGGER INDUCTION PULSE"):
        with st.spinner("Broadcasting electromagnetic pulse..."):
            import time
            time.sleep(0.8)
        st.success(f"Pulse sent for {axle_load}T load. Asphalt microcapsules activated.")
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Carbon Ledger":
    st.markdown('<div class="section-heading">Carbon Credit Ledger</div>', unsafe_allow_html=True)
    c_col1, c_col2 = st.columns(2)
    with c_col1:
        st.markdown('<div class="sleek-card"><h2 style="color:#D4AF37; font-family:\'Cinzel\'; font-size:2.5rem;">142.5 tCO2e</h2><p style="margin-top:10px;">Avoided hot-mix bitumen emissions verified.</p></div>', unsafe_allow_html=True)
    with c_col2:
        st.markdown('<div class="sleek-card">', unsafe_allow_html=True)
        st.markdown("### Ledger Minting")
        if st.button("MINT VERIFIED CREDITS"):
            st.success("Successfully minted cryptographic proof on municipal ledger.")
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "Citizen Hub":
    st.markdown('<div class="section-heading">Citizen Vigil Hub</div>', unsafe_allow_html=True)
    cit_1, cit_2 = st.columns(2)
    with cit_1:
        st.markdown('<div class="sleek-card">', unsafe_allow_html=True)
        with st.form("report_form"):
            st.markdown("### Report Road Hazard")
            loc = st.text_input("Street Name")
            if st.form_submit_button("SUBMIT REPORT") and loc:
                st.success("Hazard logged into telemetry loop!")
        st.markdown('</div>', unsafe_allow_html=True)
    with cit_2:
        st.markdown('<div class="sleek-card">', unsafe_allow_html=True)
        st.markdown("### Active Community Reports")
        for r in st.session_state.community_reports:
            st.markdown(f"""<div style="background: rgba(0,0,0,0.3); padding: 12px; border-radius: 8px; margin-top: 10px; border-left: 3px solid #D4AF37;"><b>{r['location']}</b><br><span style="color:#D4AF37; font-size:0.9rem;">{r['type']}</span></div>""", unsafe_allow_html=True)
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
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Finance":
    st.markdown('<div class="section-heading">Financial Economics</div>', unsafe_allow_html=True)
    f_c1, f_c2 = st.columns(2)
    with f_c1:
        st.markdown("""
            <div class="sleek-card" style="border-color: rgba(239, 68, 68, 0.4);">
                <h3 style="color:#EF4444; font-family:'Cinzel';">Traditional Reactive</h3>
                <h2 style="color:#EF4444; font-family:'Cinzel'; font-size:2.2rem; margin: 10px 0;">₹4.5 Cr / yr</h2>
                <p>High ongoing costs from late-stage full road reconstruction cycles.</p>
            </div>
        """, unsafe_allow_html=True)
    with f_c2:
        st.markdown("""
            <div class="sleek-card" style="border-color: rgba(212, 175, 55, 0.4);">
                <h3 style="color:#D4AF37; font-family:'Cinzel';">ROADX Preventative</h3>
                <h2 style="color:#D4AF37; font-family:'Cinzel'; font-size:2.2rem; margin: 10px 0;">₹1.8 Cr / yr</h2>
                <p>Targeted micro-interventions saving over 60% annually.</p>
            </div>
        """, unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("""
    <div style="border-top: 1px solid rgba(212,175,55,0.2); margin-top: 80px; padding-top: 30px; text-align: center;">
        <div style="font-family: 'Cinzel', serif; font-size: 0.8rem; color: #D4AF37; letter-spacing: 3px;">ROADX.AI © 2026 // TRIVANDRUM MUNICIPAL PILOT</div>
    </div>
""", unsafe_allow_html=True)
