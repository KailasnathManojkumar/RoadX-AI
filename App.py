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
    page_title="ROADX AI",
    page_icon="⚡",
    layout="centered", # Centered gives that strict, high-end mobile/landing page narrow column width
    initial_sidebar_state="collapsed"
)

# --- DEFINE-STYLE CSS INJECTION ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@450;500;600;700&family=JetBrains+Mono:wght@400;700&display=swap');

        /* Pure Pitch Black Theme */
        html, body, [data-testid="stAppViewContainer"] {
            background-color: #000000 !important;
            color: #FFFFFF !important;
            font-family: 'Space Grotesk', sans-serif;
        }

        .block-container {
            max-width: 650px !important; /* Forces that tight, sleek mobile/landing container look */
            padding-top: 3rem !important;
            padding-bottom: 5rem !important;
            padding-left: 1.5rem !important;
            padding-right: 1.5rem !important;
        }

        #MainMenu, footer, header {visibility: hidden;}

        /* Brutalist / Modern Crimson Branding */
        .brand-title {
            font-family: 'JetBrains Mono', monospace;
            font-size: 2.8rem;
            font-weight: 700;
            letter-spacing: -2px;
            color: #FFFFFF;
            text-transform: uppercase;
            margin-bottom: 0.5rem;
        }
        .brand-title span {
            color: #FF1E38; /* Signature Crimson */
        }

        .section-heading {
            font-family: 'JetBrains Mono', monospace;
            font-size: 2rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: -1px;
            margin-top: 3rem;
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
        }
        .sleek-card:hover {
            border-color: #FF1E38;
            box-shadow: 0 0 25px rgba(255, 30, 56, 0.15);
        }

        /* Pill Buttons Matching the Screenshot Style */
        .stButton>button {
            background-color: #FF1E38 !important;
            color: #FFFFFF !important;
            font-family: 'JetBrains Mono', monospace !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            border-radius: 6px !important;
            border: none !important;
            padding: 0.75rem 1.5rem !important;
            width: 100%;
            letter-spacing: 1px;
        }
        .stButton>button:hover {
            background-color: #E0112A !important;
        }

        /* Text styling */
        p, span, div {
            color: #A0A0A0;
            font-size: 1.05rem;
            line-height: 1.6;
        }
    </style>
""", unsafe_allow_html=True)

# Session state initialization
if "nav" not in st.session_state:
    st.session_state.nav = "Home"

# --- TOP BRAND HEADER ---
st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1A1A1A; padding-bottom: 20px; margin-bottom: 40px;">
        <div class="brand-title">ROADX<span>.AI</span></div>
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; color: #FF1E38; letter-spacing: 2px;">LIVE SYSTEM</div>
    </div>
""", unsafe_allow_html=True)

# --- HERO SECTION ---
st.markdown("""
    <div style="text-align: center; padding: 20px 0 40px 0;">
        <h1 style="font-family: 'JetBrains Mono', monospace; font-size: 3rem; font-weight: 700; color: #FFF; line-height: 1.1; margin-bottom: 20px;">
            BUILD BEYOND <span style="color: #FF1E38;">BOUNDARIES.</span>
        </h1>
        <p>Autonomous sub-surface infrastructure monitoring deployed for modern smart cities.</p>
    </div>
""", unsafe_allow_html=True)

# Action CTA matching the reference "Apply with Devfolio" pill box vibe
if st.button("LAUNCH TELEMETRY COMMAND"):
    st.session_state.nav = "Command"

# --- TIMELINE / SECTION MOCKUP ---
st.markdown('<div class="section-heading">The Verticals</div>', unsafe_allow_html=True)

st.markdown("""
    <div class="sleek-card">
        <h3 style="color: #FFF; font-family: 'JetBrains Mono', monospace; margin-bottom: 10px;">01 // HARDWARE</h3>
        <p>Sub-surface acoustic ground-penetrating sensors mapping structural soil erosion in real-time.</p>
    </div>
    <div class="sleek-card">
        <h3 style="color: #FFF; font-family: 'JetBrains Mono', monospace; margin-bottom: 10px;">02 // SOFTWARE</h3>
        <p>YOLOv8 computer vision models detecting micro-cracks and structural shifts instantly.</p>
    </div>
""", unsafe_allow_html=True)

# --- FAQ SECTION (Like the screenshot accordion layout) ---
st.markdown('<div class="section-heading">Frequently Asked</div>', unsafe_allow_html=True)

with st.expander("Who can deploy and utilize this system?"):
    st.markdown("Municipal corporations and smart-city infrastructure engineers can integrate via standard API webhooks.")

with st.expander("Is there a live testing sandbox?"):
    st.markdown("Yes, live city corridors in Trivandrum are actively mapped on our telemetry engine.")

# --- FOOTER NAV LINKS ---
st.markdown("""
    <div style="border-top: 1px solid #1A1A1A; margin-top: 60px; padding-top: 40px; text-align: center;">
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.2rem; color: #FFF; font-weight: 700; margin-bottom: 20px;">ROADX.AI</div>
        <div style="display: flex; justify-content: center; gap: 20px; font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: #666; margin-bottom: 20px;">
            <span>home</span>
            <span>about</span>
            <span>verticals</span>
            <span>timeline</span>
        </div>
        <p style="font-size: 0.75rem; color: #444;">© All rights reserved RoadX 2026</p>
    </div>
""", unsafe_allow_html=True)
