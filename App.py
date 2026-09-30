import os
import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np
from PIL import Image, ImageDraw
import random
import datetime

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
if "work_orders" not in st.session_state:
    st.session_state.work_orders = [
        {"id": "WO-9041", "lat": 8.5331, "lon": 76.9317, "location": "MC Road Corridor, Sector 4", "severity": "CRITICAL", "cost": "₹12,450", "status": "Dispatched to Contractor", "time": "10 mins ago"},
        {"id": "WO-9042", "lat": 8.5645, "lon": 76.8782, "location": "NH-66 Bypass Junction", "severity": "MODERATE", "cost": "₹5,200", "status": "Pending Verification", "time": "1 hour ago"}
    ]

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("""
        <div style="padding: 10px 0 20px 0;">
            <div class="brand-title">ROADX<span>.AI</span></div>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: #D4AF37; letter-spacing: 2px;">ENTERPRISE AUTO-DISPATCH</div>
        </div>
    """, unsafe_allow_html=True)
    
    pages = ["Overview", "Fleet Stream Ingestion", "Auto-Dispatch Work Orders", "Command Center", "Finance"]
    page = st.radio("Navigation", pages, label_visibility="collapsed")
    
    st.markdown("<hr style='border-color: rgba(212,175,55,0.15); margin: 30px 0;'>", unsafe_allow_html=True)
    st.markdown("""
        <div style="background: rgba(212, 175, 55, 0.05); border: 1px solid rgba(212, 175, 55, 0.2); border-radius: 12px; padding: 15px;">
            <div style="font-size: 0.75rem; color: #D4AF37; font-family: 'JetBrains Mono'; margin-bottom: 5px;">SYSTEM STATUS</div>
            <div style="font-size: 0.9rem; color: #FFFFFF; font-weight: 600;">🟢 Fleet Feed Active</div>
            <div style="font-size: 0.8rem; color: #94A3B8; margin-top: 5px;">Connected Vehicles: 42 Units</div>
        </div>
    """, unsafe_allow_html=True)

# ================= PAGE ROUTING =================
if page == "Overview":
    st.markdown("""
        <div style="padding: 30px 0 40px 0;">
            <h1 style="font-family: 'Cinzel', serif; font-size: 3.2rem; font-weight: 800; color: #FFF; line-height: 1.1; margin-bottom: 15px;">
                CLOSED-LOOP <span style="color: #D4AF37;">AUTO-DISPATCH.</span>
            </h1>
            <p style="font-size: 1.2rem; max-width: 750px; color: #94A3B8;">Moving beyond static photo uploads. ROADX ingests live commercial fleet dashcam streams, calculates defect severity, and automatically pushes active work orders to ground contractors.</p>
        </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="sleek-card"><h2 style="color:#D4AF37; font-family:\'Cinzel\'; font-size: 2.5rem;">42</h2><p style="margin-top:5px;">Active Fleet Vehicles</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="sleek-card"><h2 style="color:#FFF; font-family:\'Cinzel\'; font-size: 2.5rem;">0 sec</h2><p style="margin-top:5px;">Manual Upload Delay</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="sleek-card"><h2 style="color:#D4AF37; font-family:\'Cinzel\'; font-size: 2.5rem;">₹14.2 Lakh</h2><p style="margin-top:5px;">SLA Penalties Avoided</p></div>', unsafe_allow_html=True)

elif page == "Fleet Stream Ingestion":
    st.markdown('<div class="section-heading">Automated Fleet Dashcam Ingestion</div>', unsafe_allow_html=True)
    
    col_f1, col_f2 = st.columns([1, 1])
    with col_f1:
        st.markdown('<div class="sleek-card">', unsafe_allow_html=True)
        st.markdown("### Live Feed Simulator")
        st.markdown("Simulating continuous video stream from commercial delivery fleet vehicle **FL-TRUCK-08** on NH-66 corridor.")
        
        uploaded_file = st.file_uploader("Test Custom Fleet Frame (Optional)", type=["jpg", "png", "jpeg"])
        if uploaded_file is not None:
            active_img = Image.open(uploaded_file)
        else:
            # Create a clean default sample frame if none uploaded
            active_img = Image.new('RGB', (800, 500), color=(30, 30, 40))
            d = ImageDraw.Draw(active_img)
            d.rectangle([200, 150, 600, 350], outline="#666666", width=10)
            d.text((220, 220), "LIVE DASHCAM FRAME [FL-TRUCK-08]", fill="#AAAAAA")
            
        st.image(active_img, caption="Incoming Telemetry Frame from Vehicle Camera", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_f2:
        st.markdown('<div class="sleek-card">', unsafe_allow_html=True)
        st.markdown("### Automated AI Processing & Dispatch Engine")
        st.markdown("When a vehicle passes a defect, edge AI instantly executes inference, logs geolocation coordinates, and triggers work orders.")
        
        if st.button("SIMULATE AUTOMATED FRAME DETECTION"):
            with st.spinner("Extracting GPS metadata & running edge inference..."):
                import time
                time.sleep(1.2)
                
                # Annotate image
                annotated = active_img.copy()
                draw = ImageDraw.Draw(annotated)
                w, h = annotated.size
                draw.rectangle([w*0.3, h*0.3, w*0.7, h*0.7], outline="#EF4444", width=4)
                draw.rectangle([w*0.3, h*0.3 - 25, w*0.3 + 260, h*0.3], fill="#EF4444")
                draw.text((w*0.3 + 5, h*0.3 - 22), "CRITICAL POTHOLE 99.1%", fill="#FFFFFF")
                
                st.success("Edge Inference Successful!")
                st.image(annotated, caption="Bounding Box & Telemetry Tagged", use_container_width=True)
                
                # Automatically create work order
                new_wo = {
                    "id": f"WO-{random.randint(9050,9999)}",
                    "lat": 8.5208,
                    "lon": 76.9382,
                    "location": "Pattom Junction Corridor",
                    "severity": "CRITICAL",
                    "cost": f"₹{random.randint(8000, 18000):,}",
                    "status": "Auto-Dispatched",
                    "time": "Just now"
                }
                st.session_state.work_orders.insert(0, new_wo)
                st.error("🚨 CLOSED-LOOP TRIGGER: Work order automatically generated and dispatched to municipal contractor mobile app!")
        
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "Auto-Dispatch Work Orders":
    st.markdown('<div class="section-heading">Closed-Loop Work Order Dashboard</div>', unsafe_allow_html=True)
    st.markdown("<p style='margin-bottom: 25px;'>This is what replaces manual human reporting. Every time the AI flags a critical defect from fleet feeds, a live work ticket is instantly created and sent to local road repair contractors.</p>", unsafe_allow_html=True)
    
    for wo in st.session_state.work_orders:
        st.markdown(f"""
            <div class="sleek-card" style="border-left: 4px solid #D4AF37;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <h3 style="color: #D4AF37; margin: 0; font-family: 'JetBrains Mono';">{wo['id']}</h3>
                    <span style="background: rgba(239, 68, 68, 0.15); color: #EF4444; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 700; border: 1px solid rgba(239, 68, 68, 0.3);">{wo['severity']}</span>
                </div>
                <div style="display: grid; grid-template-columns: 2fr 1fr 1fr; gap: 15px; margin-top: 15px;">
                    <div><b>Location:</b><br>{wo['location']}</div>
                    <div><b>Estimated Repair Cost:</b><br><span style="color: #D4AF37; font-weight: 700;">{wo['cost']}</span></div>
                    <div><b>Status:</b><br><span style="color: #10B981;">{wo['status']}</span></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

elif page == "Command Center":
    st.markdown('<div class="section-heading">Active Fleet & Hazard Map</div>', unsafe_allow_html=True)
    
    # Map work orders
    wo_df = pd.DataFrame(st.session_state.work_orders)
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=wo_df,
        get_position=["lon", "lat"],
        get_fill_color="[239, 68, 68, 220]",
        get_radius=400,
        pickable=True,
    )
    view_state = pdk.ViewState(latitude=8.5241, longitude=76.9366, zoom=12, pitch=30)
    deck = pdk.Deck(layers=[layer], initial_view_state=view_state, map_style="mapbox://styles/mapbox/dark-v10")
    st.pydeck_chart(deck, use_container_width=True)

elif page == "Finance":
    st.markdown('<div class="section-heading">SLA Penalty Prevention Economics</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="sleek-card" style="border-color: rgba(239,68,68,0.4);"><h3 style="color:#EF4444; font-family:\'Cinzel\';">Without Auto-Dispatch</h3><h2 style="color:#EF4444; font-size:2.2rem; margin:10px 0;">14 Days</h2><p>Average time taken for citizen complaints to reach repair contractors, resulting in heavy highway penalty fines.</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="sleek-card" style="border-color: rgba(212,175,55,0.4);"><h3 style="color:#D4AF37; font-family:\'Cinzel\';">With ROADX Closed-Loop</h3><h2 style="color:#D4AF37; font-size:2.2rem; margin:10px 0;">< 4 Hours</h2><p>Automated fleet ingestion to contractor dispatch loop, eliminating administrative delays and financial penalties.</p></div>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("""
    <div style="border-top: 1px solid rgba(212,175,55,0.2); margin-top: 80px; padding-top: 30px; text-align: center;">
        <div style="font-family: 'Cinzel', serif; font-size: 0.8rem; color: #D4AF37; letter-spacing: 3px;">ROADX.AI © 2026 // AUTONOMOUS FLEET TELEMETRY</div>
    </div>
""", unsafe_allow_html=True)
