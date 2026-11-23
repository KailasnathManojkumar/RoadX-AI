import os
import uuid
import hmac
import sqlite3
from pathlib import Path
from datetime import datetime

import pandas as pd
import streamlit as st

# Optional AI dependencies
try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False

try:
    from PIL import Image
    import numpy as np
    IMAGE_TOOLS_AVAILABLE = True
except ImportError:
    IMAGE_TOOLS_AVAILABLE = False


# =========================================================
# CONFIGURATION
# =========================================================

APP_NAME = "ROADX.AI"
APP_VERSION = "2.0"

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = BASE_DIR / "uploads"
DB_PATH = DATA_DIR / "roadx.db"

DATA_DIR.mkdir(exist_ok=True)
UPLOAD_DIR.mkdir(exist_ok=True)

st.set_page_config(
    page_title="ROADX.AI | Infrastructure Intelligence",
    page_icon="🛣️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# THEME
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background-color: #090b0e;
    color: #f3f3f3;
}

[data-testid="stSidebar"] {
    background-color: #11151b;
    border-right: 1px solid #292e36;
}

h1, h2, h3 {
    color: #f5c76a !important;
}

.roadx-card {
    background: linear-gradient(145deg, #171d25, #101419);
    border: 1px solid #303640;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 12px;
}

.roadx-muted {
    color: #a6adb8;
    font-size: 13px;
}

.roadx-value {
    color: #f5c76a;
    font-size: 28px;
    font-weight: 800;
}

.roadx-brand {
    color: #f5c76a;
    font-weight: 800;
    letter-spacing: 3px;
}

div.stButton > button {
    background-color: #d9a94f;
    color: #101010;
    border: none;
    border-radius: 8px;
    font-weight: 700;
    min-height: 40px;
}

div.stButton > button:hover {
    background-color: #f5c76a;
    color: #000000;
}

[data-testid="stMetric"] {
    background: #151a21;
    border: 1px solid #303640;
    border-radius: 12px;
    padding: 14px;
}

hr {
    border-color: #303640;
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# DATABASE
# =========================================================

def get_connection():
    connection = sqlite3.connect(DB_PATH, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with get_connection() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS roads (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            health_score INTEGER NOT NULL,
            risk_level TEXT NOT NULL,
            last_inspected TEXT
        )
        """)

        conn.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id TEXT PRIMARY KEY,
            location TEXT NOT NULL,
            issue_type TEXT NOT NULL,
            description TEXT,
            latitude REAL,
            longitude REAL,
            image_path TEXT,
            source TEXT NOT NULL,
            confidence REAL,
            status TEXT NOT NULL,
            contractor TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """)

        conn.execute("""
        CREATE TABLE IF NOT EXISTS repairs (
            id TEXT PRIMARY KEY,
            report_id TEXT NOT NULL,
            repair_description TEXT,
            repair_cost REAL,
            completed_at TEXT NOT NULL,
            FOREIGN KEY(report_id) REFERENCES reports(id)
        )
        """)

        conn.execute("""
        CREATE TABLE IF NOT EXISTS finance (
            id TEXT PRIMARY KEY,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            entry_type TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """)

        conn.commit()

        count = conn.execute("SELECT COUNT(*) FROM roads").fetchone()[0]

        if count == 0:
            sample_roads = [
                ("R001", "Main Road - Sample Zone A", 8.5241, 76.9366, 82, "Low"),
                ("R002", "Highway - Sample Zone B", 8.5074, 76.9530, 54, "Medium"),
                ("R003", "Junction - Sample Zone C", 8.5310, 76.9420, 31, "High"),
                ("R004", "Residential Road - Sample Zone D", 8.5160, 76.9290, 91, "Low"),
                ("R005", "Market Road - Sample Zone E", 8.5400, 76.9500, 43, "High"),
            ]

            now = datetime.now().isoformat(timespec="seconds")

            conn.executemany("""
                INSERT INTO roads
                (id, name, latitude, longitude, health_score,
                 risk_level, last_inspected)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, [(*road, now) for road in sample_roads])

            conn.commit()


initialize_database()


# =========================================================
# GENERAL HELPERS
# =========================================================

def now_string():
    return datetime.now().isoformat(timespec="seconds")


def make_id(prefix):
    return f"{prefix}-{uuid.uuid4().hex[:10].upper()}"


def get_dataframe(query, parameters=()):
    with get_connection() as conn:
        return pd.read_sql_query(query, conn, params=parameters)


def save_uploaded_image(uploaded_file):
    if uploaded_file is None:
        return None

    allowed_types = {"image/jpeg", "image/png", "image/webp"}

    if uploaded_file.type not in allowed_types:
        st.error("Please upload a JPG, PNG, or WEBP image.")
        return None

    extension = Path(uploaded_file.name).suffix.lower()

    if extension not in {".jpg", ".jpeg", ".png", ".webp"}:
        st.error("Unsupported image extension.")
        return None

    filename = f"{uuid.uuid4().hex}{extension}"
    destination = UPLOAD_DIR / filename

    destination.write_bytes(uploaded_file.getvalue())

    return str(destination)


def create_report(
    location,
    issue_type,
    description="",
    latitude=None,
    longitude=None,
    image_path=None,
    source="Public",
    confidence=None,
):
    report_id = make_id("RX")
    timestamp = now_string()

    with get_connection() as conn:
        conn.execute("""
        INSERT INTO reports (
            id, location, issue_type, description,
            latitude, longitude, image_path,
            source, confidence, status, contractor,
            created_at, updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            report_id,
            location,
            issue_type,
            description,
            latitude,
            longitude,
            image_path,
            source,
            confidence,
            "Pending",
            None,
            timestamp,
            timestamp,
        ))
        conn.commit()

    return report_id


def update_report_status(report_id, new_status, contractor=None):
    with get_connection() as conn:
        conn.execute("""
        UPDATE reports
        SET status = ?,
            contractor = COALESCE(?, contractor),
            updated_at = ?
        WHERE id = ?
        """, (
            new_status,
            contractor,
            now_string(),
            report_id,
        ))
        conn.commit()


def add_finance_entry(description, amount, entry_type):
    with get_connection() as conn:
        conn.execute("""
        INSERT INTO finance
        (id, description, amount, entry_type, created_at)
        VALUES (?, ?, ?, ?, ?)
        """, (
            make_id("FIN"),
            description,
            float(amount),
            entry_type,
            now_string(),
        ))
        conn.commit()


def add_repair(report_id, description, cost):
    with get_connection() as conn:
        conn.execute("""
        INSERT INTO repairs
        (id, report_id, repair_description, repair_cost, completed_at)
        VALUES (?, ?, ?, ?, ?)
        """, (
            make_id("REP"),
            report_id,
            description,
            float(cost),
            now_string(),
        ))
        conn.commit()

    add_finance_entry(
        f"Repair completed: {report_id}",
        float(cost),
        "Expense",
    )


def get_metrics():
    with get_connection() as conn:
        total = conn.execute("SELECT COUNT(*) FROM reports").fetchone()[0]
        pending = conn.execute(
            "SELECT COUNT(*) FROM reports WHERE status = 'Pending'"
        ).fetchone()[0]
        active = conn.execute("""
            SELECT COUNT(*) FROM reports
            WHERE status IN ('Assigned', 'In Progress')
        """).fetchone()[0]
        completed = conn.execute(
            "SELECT COUNT(*) FROM reports WHERE status = 'Completed'"
        ).fetchone()[0]
        repair_count = conn.execute("SELECT COUNT(*) FROM repairs").fetchone()[0]
        expenses = conn.execute("""
            SELECT COALESCE(SUM(amount), 0)
            FROM finance WHERE entry_type = 'Expense'
        """).fetchone()[0]

    return {
        "total": total,
        "pending": pending,
        "active": active,
        "completed": completed,
        "repairs": repair_count,
        "expenses": expenses,
    }


# =========================================================
# OPTIONAL YOLO MODEL
# =========================================================

def get_model_path():
    env_path = os.getenv("ROADX_MODEL_PATH")

    if env_path:
        return env_path.strip()

    try:
        secret_val = st.secrets.get("ROADX_MODEL_PATH", "")
        return str(secret_val).strip() if secret_val else ""
    except Exception:
        return ""


def resolve_model_path(raw_path: str):
    if not raw_path:
        return None

    candidate = Path(raw_path)
    if candidate.is_file():
        return candidate

    from_base = BASE_DIR / raw_path
    if from_base.is_file():
        return from_base

    return candidate


@st.cache_resource
def load_yolo_model(model_path: str):
    if not YOLO_AVAILABLE:
        return None, "Ultralytics is not installed."

    resolved = resolve_model_path(model_path)
    if resolved is None or not resolved.is_file():
        return None, f"Model file not found at '{model_path}'."

    try:
        return YOLO(str(resolved)), None
    except Exception as error:
        return None, f"Failed to load model '{resolved.name}': {error}"


def run_detection(image_path: str, conf_threshold: float = 0.15):
    model_path = get_model_path()

    if not IMAGE_TOOLS_AVAILABLE:
        return None, "Pillow and NumPy are required."

    if not YOLO_AVAILABLE:
        return None, "Ultralytics is not installed."

    if not model_path:
        return None, "No trained YOLO model path is configured."

    model, load_error = load_yolo_model(model_path)
    if load_error or model is None:
        return None, load_error or "The configured model could not be loaded."

    try:
        results = model(image_path, conf=conf_threshold, verbose=False)
        detections = []

        for result in results:
            names = result.names or {}
            if result.boxes is None:
                continue

            for box in result.boxes:
                class_id = int(box.cls[0].item())
                confidence = float(box.conf[0].item())

                detections.append({
                    "class": str(names.get(class_id, class_id)),
                    "confidence": confidence,
                })

        return detections, None

    except Exception as error:
        return None, f"Detection failed: {error}"


# =========================================================
# SIDEBAR AND ROLE SELECTION
# =========================================================

if "role" not in st.session_state:
    st.session_state.role = "Public"

if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False

with st.sidebar:
    st.markdown(
        '<p class="roadx-brand">ROADX.AI</p>',
        unsafe_allow_html=True,
    )
    st.caption("INFRASTRUCTURE INTELLIGENCE")
    st.divider()

    selected_role = st.selectbox(
        "Select workspace",
        ["Public", "Contractor", "Admin"],
        index=["Public", "Contractor", "Admin"].index(
            st.session_state.role
        ),
    )

    st.session_state.role = selected_role

    if st.session_state.role == "Public":
        public_page = st.radio(
            "Citizen navigation",
            ["Report & Overview", "Community Updates"],
        )
    elif st.session_state.role == "Contractor":
        contractor_page = st.radio(
            "Contractor navigation",
            ["Operations Hub"],
        )
    else:
        admin_page = st.radio(
            "Admin navigation",
            [
                "Overview",
                "Vision Lab",
                "Command Center",
                "Report Management",
                "Cost Estimator",
            ],
        )
        if st.session_state.admin_authenticated and st.button("Lock admin session"):
            st.session_state.admin_authenticated = False
            st.rerun()

    st.divider()
    st.caption(f"Version {APP_VERSION}")
    st.caption("Road infrastructure management platform")


# =========================================================
# HEADER
# =========================================================

st.markdown("# ROADX.AI")
st.markdown(
    "### Autonomous Infrastructure Health & Safety Intelligence"
)
st.markdown(
    '<p class="roadx-muted">Monitor road conditions. '
    'Report hazards. Coordinate repairs. Improve safety.</p>',
    unsafe_allow_html=True,
)
st.divider()


# =========================================================
# PUBLIC WORKSPACE
# =========================================================

def public_home():
    st.subheader("Public Infrastructure Portal")

    metrics = get_metrics()

    col1, col2, col3 = st.columns(3)

    col1.metric("Reports submitted", metrics["total"])
    col2.metric("Pending reports", metrics["pending"])
    col3.metric("Completed reports", metrics["completed"])

    st.markdown("### Report a road hazard")
    st.write(
        "Help identify road damage and safety hazards "
        "by submitting a report."
    )

    with st.form("public_report_form"):
        location = st.text_input(
            "Road or location name",
            placeholder="Example: Main road near the bus stop",
        )

        issue_type = st.selectbox(
            "Type of issue",
            [
                "Pothole",
                "Road cracking",
                "Surface damage",
                "Waterlogging",
                "Broken road edge",
                "Other",
            ],
        )

        description = st.text_area(
            "Additional details",
            placeholder="Describe the issue and its location...",
        )

        col1, col2 = st.columns(2)

        with col1:
            latitude = st.number_input(
                "Latitude (optional)",
                min_value=-90.0,
                max_value=90.0,
                value=0.0,
                format="%.6f",
            )

        with col2:
            longitude = st.number_input(
                "Longitude (optional)",
                min_value=-180.0,
                max_value=180.0,
                value=0.0,
                format="%.6f",
            )

        uploaded_file = st.file_uploader(
            "Upload road image (optional)",
            type=["jpg", "jpeg", "png", "webp"],
        )

        submitted = st.form_submit_button(
            "Submit road report",
            use_container_width=True,
        )

        if submitted:
            if not location.strip():
                st.error("Please enter a location.")
            else:
                image_path = save_uploaded_image(uploaded_file)

                if uploaded_file is None or image_path:
                    report_id = create_report(
                        location=location.strip(),
                        issue_type=issue_type,
                        description=description.strip(),
                        latitude=latitude if latitude != 0 else None,
                        longitude=longitude if longitude != 0 else None,
                        image_path=image_path,
                        source="Public",
                    )

                    st.success(
                        f"Report submitted successfully. Reference: {report_id}"
                    )
                    st.info(
                        "Your report has been saved with Pending status. "
                        "It has not yet been independently verified."
                    )

    st.divider()
    st.markdown("### Recent community reports")

    reports = get_dataframe("""
        SELECT id, location, issue_type, status, created_at
        FROM reports
        ORDER BY created_at DESC
        LIMIT 10
    """)

    if reports.empty:
        st.info("No reports have been submitted yet.")
    else:
        st.dataframe(reports, use_container_width=True, hide_index=True)


def public_updates():
    st.subheader("Community Updates")

    reports = get_dataframe("""
        SELECT id, location, issue_type, status, contractor, updated_at
        FROM reports
        ORDER BY updated_at DESC
    """)

    if reports.empty:
        st.info("There are currently no community updates.")
    else:
        st.dataframe(
            reports,
            use_container_width=True,
            hide_index=True,
        )


# =========================================================
# CONTRACTOR WORKSPACE
# =========================================================

def contractor_dashboard():
    st.subheader("Contractor Operations Hub")

    st.info(
        "Prototype workspace: contractor identity and assignment "
        "permissions must be connected to a proper authentication system "
        "before real-world deployment."
    )

    reports = get_dataframe("""
        SELECT *
        FROM reports
        ORDER BY
            CASE status
                WHEN 'Pending' THEN 1
                WHEN 'Assigned' THEN 2
                WHEN 'In Progress' THEN 3
                ELSE 4
            END,
            created_at DESC
    """)

    if reports.empty:
        st.info("No road reports are currently available.")
        return

    st.markdown("### Available road tickets")

    st.dataframe(
        reports[
            ["id", "location", "issue_type", "status", "created_at"]
        ],
        use_container_width=True,
        hide_index=True,
    )

    st.divider()
    st.markdown("### Update ticket")

    report_ids = reports["id"].tolist()

    selected_id = st.selectbox(
        "Select ticket",
        report_ids,
    )

    selected_report = reports[
        reports["id"] == selected_id
    ].iloc[0]

    st.write(f"**Location:** {selected_report['location']}")
    st.write(f"**Issue:** {selected_report['issue_type']}")
    st.write(f"**Current status:** {selected_report['status']}")

    contractor_name = st.text_input(
        "Contractor or team name",
        value=selected_report["contractor"] or "",
    )

    new_status = st.selectbox(
        "New status",
        ["Pending", "Assigned", "In Progress", "Completed"],
        index=[
            "Pending", "Assigned", "In Progress", "Completed"
        ].index(selected_report["status"]),
    )

    if st.button("Save ticket update"):
        update_report_status(
            selected_id,
            new_status,
            contractor_name.strip() or None,
        )

        st.success("Ticket status updated.")
        st.rerun()

    if new_status == "Completed":
        st.divider()
        st.markdown("### Record completed repair")

        repair_description = st.text_input(
            "Repair work performed"
        )

        repair_cost = st.number_input(
            "Repair cost (₹)",
            min_value=0.0,
            value=0.0,
            step=100.0,
        )

        if st.button("Save repair record"):
            if not repair_description.strip():
                st.error("Enter a repair description.")
            else:
                add_repair(
                    selected_id,
                    repair_description.strip(),
                    repair_cost,
                )
                st.success("Repair record saved.")
                st.rerun()


# =========================================================
# VISION LAB (ADMIN WORKSPACE)
# =========================================================

def vision_lab():
    st.subheader("ROADX Vision Lab")

    st.write(
        "Upload a road image to inspect it using a configured "
        "YOLO model. Tune the confidence threshold to test model sensitivity."
    )

    model_path = get_model_path()

    if not YOLO_AVAILABLE:
        st.warning(
            "Ultralytics is not installed. Install it using "
            "`pip install ultralytics` to enable detection."
        )
    elif not model_path:
        st.warning(
            "No trained model is configured. Set ROADX_MODEL_PATH "
            "to the path of your trained model weights."
        )
    else:
        resolved = resolve_model_path(model_path)
        if resolved and resolved.is_file():
            st.success(f"Model file ready: `{resolved.name}`")
        else:
            st.warning(
                f"Configured `ROADX_MODEL_PATH` (`{model_path}`) was not found."
            )

    conf_threshold = st.slider(
        "Confidence threshold",
        min_value=0.05,
        max_value=0.90,
        value=0.15,
        step=0.05,
        key="vision_conf_threshold",
    )

    uploaded_file = st.file_uploader(
        "Upload road image",
        type=["jpg", "jpeg", "png", "webp"],
        key="vision_upload",
    )

    if uploaded_file:
        image_path = save_uploaded_image(uploaded_file)

        if image_path:
            image = Image.open(image_path).convert("RGB")
            st.image(image, caption="Uploaded road image", use_container_width=True)

            if st.button("Run AI inspection"):
                with st.spinner("Inspecting image..."):
                    detections, error = run_detection(
                        image_path,
                        conf_threshold=conf_threshold,
                    )

                if error:
                    st.error(error)
                elif not detections:
                    st.info(
                        "No objects were returned at this confidence threshold. "
                        "Try lowering the confidence slider or testing another road photo."
                    )
                else:
                    st.success(
                        f"Model returned {len(detections)} detection(s)."
                    )

                    detection_df = pd.DataFrame(detections)
                    st.dataframe(
                        detection_df,
                        use_container_width=True,
                        hide_index=True,
                    )

                    best_detection = max(
                        detections,
                        key=lambda item: item["confidence"],
                    )

                    st.markdown("### Create a ticket from this inspection")

                    location = st.text_input(
                        "Inspection location",
                        key="vision_location",
                    )

                    if st.button("Create inspection ticket"):
                        if not location.strip():
                            st.error("Enter the inspection location.")
                        else:
                            report_id = create_report(
                                location=location.strip(),
                                issue_type=best_detection["class"],
                                description=(
                                    "Created from ROADX Vision Lab. "
                                    "AI detection requires human verification."
                                ),
                                image_path=image_path,
                                source="AI inspection",
                                confidence=best_detection["confidence"],
                            )

                            st.success(
                                f"Ticket created: {report_id}"
                            )


# =========================================================
# ADMIN AUTHENTICATION
# =========================================================

def get_admin_password():
    env_password = os.getenv("ROADX_ADMIN_PASSWORD")

    if env_password:
        return env_password.strip()

    try:
        secret_val = st.secrets.get("ROADX_ADMIN_PASSWORD", "")
        return str(secret_val).strip() if secret_val else ""
    except Exception:
        return ""


def admin_login():
    st.subheader("Administrator Authentication")

    configured_password = get_admin_password()

    if not configured_password:
        st.error(
            "Admin access is not configured. Set ROADX_ADMIN_PASSWORD "
            "as an environment variable or in Streamlit secrets."
        )
        return False

    password = st.text_input(
        "Administrator password",
        type="password",
    )

    if st.button("Authenticate"):
        if hmac.compare_digest(password, configured_password):
            st.session_state.admin_authenticated = True
            st.success("Authentication successful.")
            st.rerun()
        else:
            st.error("Incorrect password.")

    return st.session_state.admin_authenticated


# =========================================================
# ADMIN OVERVIEW
# =========================================================

def admin_overview():
    st.subheader("Infrastructure Command Overview")

    metrics = get_metrics()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total reports", metrics["total"])
    c2.metric("Pending", metrics["pending"])
    c3.metric("Active", metrics["active"])
    c4.metric("Completed", metrics["completed"])

    st.divider()

    c1, c2 = st.columns(2)

    c1.metric("Recorded repairs", metrics["repairs"])
    c2.metric(
        "Recorded expenses",
        f"₹{metrics['expenses']:,.2f}",
    )

    st.markdown("### Report status distribution")

    status_data = get_dataframe("""
        SELECT status, COUNT(*) AS count
        FROM reports
        GROUP BY status
    """)

    if status_data.empty:
        st.info("No report data is available.")
    else:
        st.bar_chart(
            status_data.set_index("status")["count"]
        )

    st.caption(
        "Metrics are calculated from records stored in the local database. "
        "Seed road locations are illustrative sample data."
    )


# =========================================================
# ADMIN COMMAND CENTER
# =========================================================

def command_center():
    st.subheader("Geospatial Road Intelligence")

    roads = get_dataframe("""
        SELECT id, name, latitude, longitude,
               health_score, risk_level, last_inspected
        FROM roads
    """)

    if roads.empty:
        st.info("No road assets have been registered.")
        return

    st.write(
        "The initial road assets are sample locations. "
        "Replace them with verified road coordinates before deployment."
    )

    st.map(
        roads.rename(
            columns={
                "latitude": "lat",
                "longitude": "lon",
            }
        ),
        latitude="lat",
        longitude="lon",
        size=80,
    )

    st.markdown("### Road asset register")

    st.dataframe(
        roads,
        use_container_width=True,
        hide_index=True,
    )

    st.divider()
    st.markdown("### Update road health assessment")

    road_id = st.selectbox(
        "Select road asset",
        roads["id"].tolist(),
    )

    road = roads[roads["id"] == road_id].iloc[0]

    health = st.slider(
        "Health score",
        min_value=0,
        max_value=100,
        value=int(road["health_score"]),
    )

    if health < 40:
        risk = "High"
    elif health < 70:
        risk = "Medium"
    else:
        risk = "Low"

    st.write(f"Calculated risk category: **{risk}**")

    if st.button("Save road assessment"):
        with get_connection() as conn:
            conn.execute("""
                UPDATE roads
                SET health_score = ?,
                    risk_level = ?,
                    last_inspected = ?
                WHERE id = ?
            """, (
                health,
                risk,
                now_string(),
                road_id,
            ))
            conn.commit()

        st.success("Road assessment updated.")
        st.rerun()


# =========================================================
# ADMIN REPORT MANAGEMENT
# =========================================================

def admin_reports():
    st.subheader("Road Report Management")

    reports = get_dataframe("""
        SELECT *
        FROM reports
        ORDER BY created_at DESC
    """)

    if reports.empty:
        st.info("No reports have been submitted.")
        return

    status_filter = st.selectbox(
        "Filter by status",
        [
            "All",
            "Pending",
            "Assigned",
            "In Progress",
            "Completed",
        ],
    )

    if status_filter != "All":
        reports = reports[
            reports["status"] == status_filter
        ]

    st.dataframe(
        reports[
            [
                "id", "location", "issue_type",
                "source", "status", "contractor",
                "created_at",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )

    st.divider()
    st.markdown("### Review individual report")

    all_reports = get_dataframe("""
        SELECT * FROM reports ORDER BY created_at DESC
    """)

    report_id = st.selectbox(
        "Choose report",
        all_reports["id"].tolist(),
    )

    report = all_reports[
        all_reports["id"] == report_id
    ].iloc[0]

    st.write(f"**Location:** {report['location']}")
    st.write(f"**Issue:** {report['issue_type']}")
    st.write(f"**Description:** {report['description'] or 'None'}")
    st.write(f"**Source:** {report['source']}")
    st.write(f"**Status:** {report['status']}")

    if pd.notna(report["confidence"]):
        st.write(
            f"**Model confidence:** {report['confidence']:.1%}"
        )

    if report["image_path"] and Path(report["image_path"]).is_file():
        st.image(
            report["image_path"],
            caption="Submitted road image",
            use_container_width=True,
        )

    new_status = st.selectbox(
        "Set report status",
        ["Pending", "Assigned", "In Progress", "Completed"],
        index=[
            "Pending", "Assigned", "In Progress", "Completed"
        ].index(report["status"]),
        key="admin_report_status",
    )

    contractor = st.text_input(
        "Assigned contractor",
        value=report["contractor"] or "",
        key="admin_contractor",
    )

    if st.button("Update report"):
        update_report_status(
            report_id,
            new_status,
            contractor.strip() or None,
        )
        st.success("Report updated.")
        st.rerun()


# =========================================================
# COST ESTIMATOR
# =========================================================

def cost_estimator():
    st.subheader("Road Repair Cost Estimator")

    st.write(
        "Estimate repair costs using transparent dimensions and "
        "editable unit rates. These are planning assumptions, "
        "not supplier quotations."
    )

    col1, col2 = st.columns(2)

    with col1:
        length = st.number_input(
            "Repair length (metres)",
            min_value=0.1,
            value=2.0,
            step=0.5,
        )

        width = st.number_input(
            "Repair width (metres)",
            min_value=0.1,
            value=1.0,
            step=0.1,
        )

        depth = st.number_input(
            "Repair depth (metres)",
            min_value=0.01,
            value=0.05,
            step=0.01,
        )

    with col2:
        material_rate = st.number_input(
            "Material rate (₹ per cubic metre)",
            min_value=0.0,
            value=8000.0,
            step=500.0,
        )

        labour_rate = st.number_input(
            "Labour and equipment (₹)",
            min_value=0.0,
            value=1500.0,
            step=100.0,
        )

        contingency = st.slider(
            "Contingency (%)",
            min_value=0,
            max_value=30,
            value=10,
        )

    volume = length * width * depth
    material_cost = volume * material_rate
    subtotal = material_cost + labour_rate
    contingency_cost = subtotal * contingency / 100
    total = subtotal + contingency_cost

    st.divider()

    c1, c2, c3 = st.columns(3)

    c1.metric("Repair volume", f"{volume:.3f} m³")
    c2.metric("Material cost", f"₹{material_cost:,.2f}")
    c3.metric("Estimated total", f"₹{total:,.2f}")

    st.write(
        f"Labour and equipment: ₹{labour_rate:,.2f}"
    )
    st.write(
        f"Contingency: ₹{contingency_cost:,.2f}"
    )

    st.caption(
        "Actual costs may vary depending on site conditions, "
        "materials, and municipal rates."
    )


# =========================================================
# WORKSPACE ROUTER
# =========================================================

if st.session_state.role == "Public":
    if public_page == "Report & Overview":
        public_home()
    else:
        public_updates()

elif st.session_state.role == "Contractor":
    contractor_dashboard()

elif st.session_state.role == "Admin":
    if st.session_state.admin_authenticated or admin_login():
        if admin_page == "Overview":
            admin_overview()
        elif admin_page == "Vision Lab":
            vision_lab()
        elif admin_page == "Command Center":
            command_center()
        elif admin_page == "Report Management":
            admin_reports()
        elif admin_page == "Cost Estimator":
            cost_estimator()
