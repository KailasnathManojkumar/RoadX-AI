import os
import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np
from PIL import Image, ImageDraw
import random

# --- CONFIGURATION ---
MAPBOX_TOKEN = "pk.eyJ1Ijoia2FpbGFzbmF0aDEyMyIsImEiOiJjbXU4Zm93YmEwdXdnMnlzMmdnbTQyNzNoIn0.0yYdaXOauUT-_A6VaeuMyg"
os.environ["MAPBOX_API_KEY"] = MAPBOX_TOKEN
pdk.settings.mapbox_api_key = MAPBOX_TOKEN

st.set_page_config(
    page_title="ROADX AI | Enterprise Platform",
    page_icon="⚜",
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

        /* Force Sidebar Toggle Arrow to be Visible & Gold */
        [data-testid="collapsedControl"] {
            display: flex !important;
            visibility: visible !important;
            color: #D4AF37 !important;
            z-index: 999999 !important;
        }

        [data-testid="collapsedControl"] svg {
            fill: #D4AF37 !important;
            color: #D4AF37 !important;
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
            box-shadow: 0 10px 30px rgba(0,0,0,0.6);
            height: 100%;
        }

        .stButton>button {
            background: linear-gradient(135deg, #D4AF37 0%, #AA8C2C 100%) !important;
            color: #030305 !important;
            font-family: 'Cinzel', serif !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            border-radius: 10px !important;
            border: 1px solid #D4AF37 !important;
            padding: 0.75rem 1rem !important;
            width: 100%;
            font-size: 0.85rem !important;
            letter-spacing: 1.5px !important;
            cursor: pointer !important;
            box-shadow: 0 4px 20px rgba(212, 175, 55, 0.3);
        }
        .stButton>button:hover {
            background: linear-gradient(135deg, #FFF 0%, #D4AF37 100%) !important;
            border-color: #FFF !important;
        }

        p, span, div, label { color: #94A3B8; font-size: 1.02rem; line-height: 1.6; }
        h1, h2, h3 { color: #FFFFFF; }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if "user_role" not in st.session_state:
    st.session_state.user_role = "Select Role"

if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False

if "carbon_credits" not in st.session_state:
    st.session_state.carbon_credits = 142.5

if "road_data" not in st.session_state:
    st.session_state.road_data = pd.DataFrame({
        "Road_ID": ["SEC-01", "SEC-02", "SEC-03", "SEC-04", "SEC-05"],
        "Location": ["Primary Corridor A", "Highway Bypass Loop", "Central Plaza Square", "North Sectorway", "Ring Route East"],
        "Latitude": [8.5331, 8.5645, 8.5175, 8.5208, 8.4842],
        "Longitude": [76.9317, 76.8782, 76.9551, 76.9382, 76.9472],
        "Health_Score": [88, 42, 94, 28, 65],
        "Status": ["Optimal", "Moderate Risk", "Optimal", "Critical Failure", "Moderate Risk"],
        "Predicted_Failure_Days": ["90+ days", "30 days", "120+ days", "4 days (Critical)", "45 days"],
        "Two_Wheeler_Risk": ["Low Risk", "High Risk", "Low Risk", "Critical High Risk", "Moderate Risk"],
    })

if "vision_database" not in st.session_state
