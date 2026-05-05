"""
app.py
Main Streamlit app for Face Recognition Attendance System
"""
import streamlit as st
import cv2
import numpy as np
import pandas as pd
import plotly.express as px
import time
import os
from datetime import datetime, timedelta
from database import Database
from face_utils import FaceUtils

# --- Premium Dark Theme CSS ---
st.markdown("""
    <style>
    :root {
        --bg-a: #0f172a;
        --bg-b: #1e293b;
        --panel: rgba(15, 23, 42, 0.8);
        --accent-a: #3b82f6;
        --accent-b: #06b6d4;
    }
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, var(--bg-a) 0%, var(--bg-b) 100%) !important;
        color: #f1f5f9;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    [data-testid="stVerticalBlock"] {
        background: transparent !important;
    }
    
    .main {
        background: var(--panel) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(51, 65, 85, 0.4);
        border-radius: 12px;
        padding: 32px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        max-width: 1000px;
        margin: 32px auto;
    }
    
    .stButton>button {
        background: #1e293b !important;
        border: 1.5px solid #334155 !important;
        color: #f1f5f9 !important;
        border-radius: 8px;
        padding: 0.75em 1.5em;
        font-size: 1em;
        font-weight: 700;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #334155 0%, #475569 100%) !important;
        border-color: #06b6d4 !important;
        color: #06b6d4 !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(6, 182, 212, 0.3) !important;
    }
    
    .stButton>button:active {
        transform: translateY(0px);
        box-shadow: 0 2px 8px rgba(6, 182, 212, 0.2) !important;
    }
    
    .stTextInput>div>input, .stNumberInput>div>input {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        color: #f1f5f9 !important;
        padding: 0.75em 1em !important;
    }
    
    .stTextInput>div>input:focus, .stNumberInput>div>input:focus {
        border-color: var(--accent-b) !important;
        box-shadow: 0 0 8px rgba(6, 182, 212, 0.2) !important;
    }
    
    .stSelectbox>div>div {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        color: #f1f5f9 !important;
        padding: 0.75em 1em !important;
    }
    
    .stSelectbox input {
        color: #f1f5f9 !important;
        background-color: #1e293b !important;
    }
    
    .stSelectbox input::placeholder {
        color: #64748b !important;
    }
    
    .stSelectbox>div>div input {
        color: #f1f5f9 !important;
        background-color: transparent !important;
        caret-color: #06b6d4 !important;
    }
    
    .stSelectbox>div>div:hover {
        border-color: var(--accent-b) !important;
        background-color: #334155 !important;
    }
    
    .stSelectbox>div>div:focus {
        border-color: var(--accent-b) !important;
        box-shadow: 0 0 8px rgba(6, 182, 212, 0.3) !important;
        background-color: #1e293b !important;
    }
    
    [data-testid="selectbox"] > div > div > div {
        color: #f1f5f9 !important;
    }
    
    [data-baseweb="combobox"] {
        color: #f1f5f9 !important;
    }
    
    [data-baseweb="combobox"] input {
        color: #f1f5f9 !important;
        background-color: #1e293b !important;
        caret-color: #06b6d4 !important;
    }
    
    [data-baseweb="combobox"] input::placeholder {
        color: #64748b !important;
    }
    
    [data-baseweb="combobox"] div[role="presentation"] {
        color: #f1f5f9 !important;
    }
    
    [data-baseweb="combobox"] span {
        color: #f1f5f9 !important;
    }
    
    .st-ae, .st-af, .st-cb, .st-ah, .st-ai, .st-aj {
        color: #f1f5f9 !important;
    }
    
    [data-baseweb="select"] [role="listbox"] {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        margin-top: 8px !important;
    }
    
    [data-baseweb="select"] [role="option"] {
        color: #cbd5e1 !important;
        background-color: #1e293b !important;
        padding: 12px 12px !important;
        font-size: 0.95em !important;
    }
    
    [data-baseweb="select"] [role="option"]:hover {
        background-color: #334155 !important;
        color: #f1f5f9 !important;
        transition: all 0.15s ease !important;
    }
    
    [data-baseweb="select"] [role="option"][aria-selected="true"] {
        background-color: rgba(6, 182, 212, 0.25) !important;
        color: #06b6d4 !important;
        font-weight: 700 !important;
        border-left: 3px solid #06b6d4 !important;
        padding-left: 10px !important;
    }
    
    [data-baseweb="select"] [role="option"]:focus {
        outline: none !important;
        background-color: #475569 !important;
        color: #f1f5f9 !important;
    }
    
    .stDataFrame {
        border-radius: 12px !important;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
        background: var(--panel) !important;
        border: 1px solid rgba(6, 182, 212, 0.1) !important;
    }
    
    .stDataFrame [role="presentation"] {
        background-color: #1e293b !important;
    }
    
    [data-testid="stMetricContainer"] {
        background-color: rgba(30, 41, 59, 0.6) !important;
        border: 1px solid rgba(6, 182, 212, 0.2) !important;
        border-radius: 12px !important;
        padding: 20px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
    }
    
    [data-testid="stMetricValue"] {
        color: #06b6d4 !important;
        font-size: 2.2em !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #cbd5e1 !important;
        font-size: 1em !important;
        font-weight: 600 !important;
    }
    
    [data-baseweb="progress-bar"] {
        background-color: rgba(6, 182, 212, 0.2) !important;
    }
    
    [data-baseweb="progress-bar"] [role="progressbar"] {
        background-color: #06b6d4 !important;
    }
    
    .stSelectbox label, .stNumberInput label, .stTextInput label, .stCheckbox label {
        color: #06b6d4 !important;
        font-weight: 600 !important;
        font-size: 0.95em !important;
        margin-bottom: 8px !important;
        display: block !important;
    }
    
    .stSelectbox label::after {
        content: '';
        display: block;
        margin-top: 2px;
    }
    
    .stCheckbox>label>div:first-child {
        background-color: #1e293b !important;
        border: 1.5px solid #334155 !important;
        border-radius: 4px !important;
    }
    
    .stCheckbox>label>div:first-child:hover {
        border-color: #06b6d4 !important;
    }
    
    .stCheckbox>label>div:first-child[aria-checked="true"] {
        background-color: rgba(6, 182, 212, 0.2) !important;
        border-color: #06b6d4 !important;
    }
    
    .stTabs [role="tab"] {
        background-color: transparent !important;
        border-bottom: 2px solid #334155 !important;
        color: #cbd5e1 !important;
        padding: 12px 16px !important;
    }
    
    .stTabs [role="tab"][aria-selected="true"] {
        border-color: var(--accent-b) !important;
        color: var(--accent-b) !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #f1f5f9 !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px !important;
    }
    
    h1 {
        font-size: 2.2em !important;
        margin-bottom: 20px !important;
        background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    h2 {
        font-size: 1.8em !important;
        color: #e2e8f0 !important;
        margin-top: 20px !important;
        margin-bottom: 15px !important;
    }
    
    h3 {
        color: #06b6d4 !important;
        font-size: 1.3em !important;
        margin-bottom: 12px !important;
    }
    
    .stMarkdown, p, div {
        color: #cbd5e1 !important;
        line-height: 1.6 !important;
    }
    
    hr {
        border-color: rgba(6, 182, 212, 0.2) !important;
        margin: 12px 0 !important;
    }
    
    /* Glass Card Menu Styling */
    .glass-card {
        background: rgba(30, 41, 59, 0.6) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(6, 182, 212, 0.2) !important;
        border-radius: 12px !important;
        padding: 16px !important;
        transition: all 0.3s cubic-bezier(0.83, 0, 0.17, 1) !important;
        cursor: pointer !important;
        text-align: center !important;
    }
    
    .glass-card:hover {
        border-color: #06b6d4 !important;
        background: rgba(6, 182, 212, 0.1) !important;
        transform: translateY(-4px) !important;
        box-shadow: 0 8px 24px rgba(6, 182, 212, 0.2) !important;
    }
    
    .glass-card.active {
        background: rgba(6, 182, 212, 0.2) !important;
        border-color: #06b6d4 !important;
        box-shadow: 0 0 20px rgba(6, 182, 212, 0.3) !important;
    }
    
    .glass-card-icon {
        font-size: 2.5em !important;
        margin-bottom: 8px !important;
        display: block !important;
    }
    
    .glass-card-label {
        font-size: 0.9em !important;
        font-weight: 700 !important;
        color: #cbd5e1 !important;
    }
    
    .glass-card:hover .glass-card-label {
        color: #06b6d4 !important;
    }
    
    * {
        color-scheme: dark !important;
    }
    
    input, select, textarea, button, div, span, p, label {
        color-scheme: dark !important;
    }
    
    /* Ensure all text is visible */
    .st-ae, .st-af, .st-ag, .st-ah, .st-ai, .st-aj,
    .st-ak, .st-al, .st-am, .st-an, .st-ao, .st-ap {
        color: #f1f5f9 !important;
    }
    
    /* Text inside select/combobox */
    div[data-value] {
        color: #f1f5f9 !important;
    }
    
    /* Selected item text */
    [role="combobox"], [role="listbox"], [role="option"] {
        color: #f1f5f9 !important;
        background-color: #1e293b !important;
    }
    
    /* Ensure content is visible on all backgrounds */
    body, html {
        --text-color: #f1f5f9;
    }
    
    input[type="text"],
    input[type="search"],
    input[type="email"],
    input[type="number"],
    select,
    textarea {
        color: #f1f5f9 !important;
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
    }
    
    
    .stSidebar {
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.95) 100%) !important;
        border-right: 2px solid rgba(6, 182, 212, 0.2) !important;
    }
    
    .stSidebar [data-testid="stVerticalBlock"] {
        background: transparent !important;
    }
    
    [data-testid="stSidebarContent"] {
        background: transparent !important;
        padding: 20px !important;
    }
    
    .stSlider>div>div>div>div {
        background: linear-gradient(90deg, #06b6d4 0%, #3b82f6 100%) !important;
    }
    
    .stSlider>div>div>div {
        background-color: #334155 !important;
    }
    
    .stNumberInput>div>div>input {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        color: #f1f5f9 !important;
    }
    
    .stNumberInput>div>div>input:focus {
        border-color: #06b6d4 !important;
        box-shadow: 0 0 8px rgba(6, 182, 212, 0.2) !important;
    }
    
    .stNumberInput button {
        background: #1e293b !important;
        border: 1px solid #334155 !important;
        color: #06b6d4 !important;
    }
    
    .stNumberInput button:hover {
        background: #334155 !important;
        border-color: #06b6d4 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- Caching for performance ---
@st.cache_resource

def get_face_utils():
    return FaceUtils()

@st.cache_resource

def get_db():
    return Database()

face_utils = get_face_utils()
db = get_db()


def open_camera(camera_index=0):
    """Open webcam with backend fallback for better Windows compatibility."""
    if os.name == 'nt':
        backend_options = [
            ('DirectShow', cv2.CAP_DSHOW),
            ('MSMF', cv2.CAP_MSMF),
            ('Default', cv2.CAP_ANY),
        ]
    else:
        backend_options = [('Default', cv2.CAP_ANY)]

    for backend_name, backend in backend_options:
        cap = cv2.VideoCapture(camera_index, backend)
        if cap is not None and cap.isOpened():
            # Keep only the latest frame to reduce stale frame issues.
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            return cap, backend_name
        if cap is not None:
            cap.release()

    return None, None


def read_frame_with_retry(cap, retries=3, delay=0.08):
    """Retry frame reads to smooth over intermittent webcam backend hiccups."""
    for _ in range(retries):
        ret, frame = cap.read()
        if ret and frame is not None:
            return frame
        time.sleep(delay)
    return None


def find_working_camera_index(max_index=4):
    """Return the first camera index that can produce a frame, else None."""
    for idx in range(max_index + 1):
        cap, _ = open_camera(idx)
        if cap is None:
            continue
        frame = read_frame_with_retry(cap, retries=2, delay=0.05)
        cap.release()
        if frame is not None:
            return idx
    return None

# --- Session state for attendance memory ---
if 'marked_today' not in st.session_state:
    st.session_state['marked_today'] = set()
if 'camera_index' not in st.session_state:
    st.session_state['camera_index'] = 0

def create_glass_menu_selector(menu_items, session_key='current_menu'):
    """Create an interactive glass-morphic card menu selector in sidebar."""
    if session_key not in st.session_state:
        st.session_state[session_key] = menu_items[0]
    
    # Menu icons mapping
    menu_icons = {
        'Dashboard': '📊',
        'Register New User': '👤',
        'Mark Attendance (Live Camera)': '📷',
        'Upload Image': '🖼️',
        'Upload Video': '🎥',
        'Attendance Records': '📋',
        'Analytics': '📈'
    }
    
    st.sidebar.markdown("<p style='color: #06b6d4; font-weight: 700; font-size: 1em; margin-bottom: 12px;'>📌 Select Option</p>", unsafe_allow_html=True)
    
    selected = None
    for idx, item in enumerate(menu_items):
        icon = menu_icons.get(item, '📌')
        is_active = st.session_state[session_key] == item
        
        # Create button with styling
        if st.sidebar.button(
            f"{icon} {item}",
            key=f"menu_{idx}",
            use_container_width=True,
            help=f"Click to select {item}"
        ):
            st.session_state[session_key] = item
            selected = item
            st.rerun()
        
        # Apply active styling with HTML/CSS
        if is_active:
            st.sidebar.markdown(
                f"""
                <style>
                button[key="menu_{idx}"] {{
                    background: linear-gradient(135deg, rgba(6, 182, 212, 0.25) 0%, rgba(6, 182, 212, 0.1) 100%) !important;
                    border: 1.5px solid #06b6d4 !important;
                    color: #06b6d4 !important;
                    box-shadow: 0 0 16px rgba(6, 182, 212, 0.3) !important;
                }}
                </style>
                """,
                unsafe_allow_html=True
            )
        
        if idx < len(menu_items) - 1:
            st.sidebar.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
    
    return st.session_state[session_key]

# --- Sidebar Menu ---
menu = [
    'Dashboard',
    'Register New User',
    'Mark Attendance (Live Camera)',
    'Upload Image',
    'Upload Video',
    'Attendance Records',
    'Analytics'
]

st.sidebar.markdown("---")
choice = create_glass_menu_selector(menu)
st.sidebar.markdown("---")

st.sidebar.markdown('---')
st.sidebar.markdown('**Camera Settings**')
st.session_state['camera_index'] = st.sidebar.number_input(
    'Camera Index',
    min_value=0,
    max_value=10,
    value=int(st.session_state['camera_index']),
    step=1,
)
if st.sidebar.button('Auto Detect Camera'):
    detected_index = find_working_camera_index(6)
    if detected_index is None:
        st.sidebar.error('No working camera detected.')
    else:
        st.session_state['camera_index'] = detected_index
        st.sidebar.success(f'Using camera index {detected_index}')

st.sidebar.markdown('---')

st.sidebar.markdown(
    '<a href="http://localhost:5174" target="_self">'
    '<button style="font-weight:600;border-radius:8px;transition:all 0.2s;'
    'background:#1e293b;border:1px solid #334155;color:#f1f5f9;'
    'padding:0.75rem 1.5rem;font-size:1rem;width:100%;cursor:pointer;">'
    'Back to Home Page'
    '</button></a>',
    unsafe_allow_html=True,
)

# --- Dashboard ---
def dashboard():
    st.title('📊 Dashboard Overview')
    
    users = db.get_all_users()
    attendance_today = db.get_attendance_today()
    total_users = len(users)
    present_today = len(attendance_today)
    absent_today = total_users - present_today
    attendance_pct = (present_today / total_users * 100) if total_users else 0
    
    # Key Metrics with enhanced styling
    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div style='
                background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(59, 130, 246, 0.1) 100%);
                border: 1px solid rgba(59, 130, 246, 0.3);
                border-radius: 12px;
                padding: 20px;
                text-align: center;
            '>
                <div style='color: #64748b; font-size: 0.9em; margin-bottom: 8px;'>Total Users</div>
                <div style='color: #3b82f6; font-size: 2.5em; font-weight: 700;'>""" + str(total_users) + """</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style='
                background: linear-gradient(135deg, rgba(34, 197, 94, 0.2) 0%, rgba(34, 197, 94, 0.1) 100%);
                border: 1px solid rgba(34, 197, 94, 0.3);
                border-radius: 12px;
                padding: 20px;
                text-align: center;
            '>
                <div style='color: #64748b; font-size: 0.9em; margin-bottom: 8px;'>Present Today</div>
                <div style='color: #22c55e; font-size: 2.5em; font-weight: 700;'>""" + str(present_today) + """</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div style='
                background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(239, 68, 68, 0.1) 100%);
                border: 1px solid rgba(239, 68, 68, 0.3);
                border-radius: 12px;
                padding: 20px;
                text-align: center;
            '>
                <div style='color: #64748b; font-size: 0.9em; margin-bottom: 8px;'>Absent Today</div>
                <div style='color: #ef4444; font-size: 2.5em; font-weight: 700;'>""" + str(absent_today) + """</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, rgba(06, 182, 212, 0.2) 0%, rgba(06, 182, 212, 0.1) 100%);
                border: 1px solid rgba(06, 182, 212, 0.3);
                border-radius: 12px;
                padding: 20px;
                text-align: center;
            '>
                <div style='color: #64748b; font-size: 0.9em; margin-bottom: 8px;'>Attendance %</div>
                <div style='color: #06b6d4; font-size: 2.5em; font-weight: 700;'>{attendance_pct:.1f}%</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
    
    # Charts section with tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Trends", "🏢 Department", "📊 Status", "👥 Summary"])
    
    with tab1:
        st.subheader("Attendance Trend (Last 7 Days)")
        trend = db.get_attendance_trend()
        if trend:
            df_trend = pd.DataFrame(trend, columns=['Date', 'Count'])
            df_trend = df_trend.sort_values('Date').tail(7)
            fig = px.line(
                df_trend, 
                x='Date', 
                y='Count',
                markers=True,
                line_shape='spline',
                title='Daily Attendance',
                labels={'Count': 'Attendance Count', 'Date': 'Date'},
                color_discrete_sequence=['#06b6d4']
            )
            fig.update_layout(
                template='plotly_dark',
                plot_bgcolor='rgba(30, 41, 59, 0.5)',
                paper_bgcolor='rgba(15, 23, 42, 0)',
                font=dict(color='#cbd5e1'),
                hovermode='x unified',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📊 No attendance data available yet")
    
    with tab2:
        st.subheader("Department-wise Attendance")
        dept_data = db.get_department_attendance()
        if dept_data:
            df_dept = pd.DataFrame(dept_data, columns=['Department', 'Count'])
            fig = px.bar(
                df_dept, 
                x='Department', 
                y='Count',
                title='Attendance by Department',
                color='Count',
                color_continuous_scale='Viridis',
                labels={'Count': 'Present', 'Department': 'Department'}
            )
            fig.update_layout(
                template='plotly_dark',
                plot_bgcolor='rgba(30, 41, 59, 0.5)',
                paper_bgcolor='rgba(15, 23, 42, 0)',
                font=dict(color='#cbd5e1'),
                showlegend=False,
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("🏢 No department data available yet")
    
    with tab3:
        st.subheader("Present vs Absent Today")
        col1, col2 = st.columns(2)
        
        with col1:
            present_vs_absent = pd.DataFrame({
                'Status': ['Present', 'Absent'],
                'Count': [present_today, absent_today]
            })
            fig = px.pie(
                present_vs_absent,
                names='Status',
                values='Count',
                color_discrete_map={'Present': '#22c55e', 'Absent': '#ef4444'},
                title='Attendance Distribution'
            )
            fig.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(15, 23, 42, 0)',
                font=dict(color='#cbd5e1'),
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("**Quick Stats**")
            st.markdown(f"""
                <div style='
                    background: rgba(30, 41, 59, 0.6);
                    border: 1px solid rgba(6, 182, 212, 0.2);
                    border-radius: 12px;
                    padding: 20px;
                    margin-top: 20px;
                '>
                    <div style='margin-bottom: 15px;'>
                        <div style='color: #64748b;'>Present Today</div>
                        <div style='color: #22c55e; font-size: 2em; font-weight: 700;'>{present_today}</div>
                    </div>
                    <div style='margin-bottom: 15px;'>
                        <div style='color: #64748b;'>Absent Today</div>
                        <div style='color: #ef4444; font-size: 2em; font-weight: 700;'>{absent_today}</div>
                    </div>
                    <div>
                        <div style='color: #64748b;'>Attendance Rate</div>
                        <div style='color: #06b6d4; font-size: 2em; font-weight: 700;'>{attendance_pct:.1f}%</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    with tab4:
        st.subheader("Detailed Summary")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
                <div style='
                    background: linear-gradient(135deg, rgba(59, 130, 246, 0.15) 0%, rgba(59, 130, 246, 0.05) 100%);
                    border-left: 4px solid #3b82f6;
                    border-radius: 8px;
                    padding: 16px;
                '>
                    <div style='color: #64748b; font-size: 0.9em; margin-bottom: 8px;'>Total Registered Users</div>
                    <div style='color: #3b82f6; font-size: 2.2em; font-weight: 700;'>""" + str(total_users) + """</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div style='
                    background: linear-gradient(135deg, rgba(34, 197, 94, 0.15) 0%, rgba(34, 197, 94, 0.05) 100%);
                    border-left: 4px solid #22c55e;
                    border-radius: 8px;
                    padding: 16px;
                '>
                    <div style='color: #64748b; font-size: 0.9em; margin-bottom: 8px;'>Present Today</div>
                    <div style='color: #22c55e; font-size: 2.2em; font-weight: 700;'>""" + str(present_today) + """</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
                <div style='
                    background: linear-gradient(135deg, rgba(06, 182, 212, 0.15) 0%, rgba(06, 182, 212, 0.05) 100%);
                    border-left: 4px solid #06b6d4;
                    border-radius: 8px;
                    padding: 16px;
                '>
                    <div style='color: #64748b; font-size: 0.9em; margin-bottom: 8px;'>Attendance Percentage</div>
                    <div style='color: #06b6d4; font-size: 2.2em; font-weight: 700;'>""" + str(f"{attendance_pct:.1f}%") + """</div>
                </div>
            """, unsafe_allow_html=True)
        
        # Status indicators
        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if attendance_pct >= 80:
                st.success("✅ **Excellent Attendance** - Rate is above 80%")
            elif attendance_pct >= 60:
                st.info("ℹ️ **Good Attendance** - Rate is above 60%")
            else:
                st.warning("⚠️ **Attendance Needs Attention** - Rate is below 60%")
        
        with col2:
            if absent_today == 0:
                st.success("✅ **Perfect Day** - Everyone is present!")
            elif absent_today <= 3:
                st.info(f"ℹ️ **Minor Absence** - {absent_today} person(s) absent")
            else:
                st.warning(f"⚠️ **Notable Absence** - {absent_today} people absent")

# --- Register New User ---
def register_user():
    st.title('📝 Register New User')
    # Initialize session state for registration
    if 'samples' not in st.session_state:
        st.session_state['samples'] = []
    if 'captured' not in st.session_state:
        st.session_state['captured'] = 0
    if 'last_frame' not in st.session_state:
        st.session_state['last_frame'] = None
    if 'reg_name' not in st.session_state:
        st.session_state['reg_name'] = ''
    if 'reg_user_id' not in st.session_state:
        st.session_state['reg_user_id'] = ''
    if 'reg_department' not in st.session_state:
        st.session_state['reg_department'] = ''
    if 'registration_ready' not in st.session_state:
        st.session_state['registration_ready'] = False

    st.subheader('Enter User Details')
    st.session_state['reg_name'] = st.text_input('Name', st.session_state['reg_name'])
    st.session_state['reg_user_id'] = st.text_input('Unique ID', st.session_state['reg_user_id'])
    st.session_state['reg_department'] = st.text_input('Department', st.session_state['reg_department'])

    if st.button('Start Registration'):
        # Reset session state for new registration
        st.session_state['samples'] = []
        st.session_state['captured'] = 0
        st.session_state['last_frame'] = None
        if not st.session_state['reg_name'] or not st.session_state['reg_user_id'] or not st.session_state['reg_department']:
            st.error('All fields are required!')
        else:
            user_id = st.session_state['reg_user_id']
            if face_utils.is_duplicate_registration(user_id):
                st.warning('User already registered!')
            else:
                st.session_state['registration_ready'] = True

    if st.session_state.get('registration_ready', False):
        st.info('Capture 5 face samples. Click "Capture Sample" for each sample.')
        samples = st.session_state['samples']
        captured = st.session_state['captured']
        frame_placeholder = st.empty()
        # Show last captured frame if available
        if st.session_state['last_frame'] is not None:
            frame_placeholder.image(st.session_state['last_frame'], channels='BGR')
        if st.button(f'Capture Sample {captured+1}', disabled=(captured>=5)) and captured < 5:
            cap, _ = open_camera(int(st.session_state['camera_index']))
            if cap is None:
                fallback_index = find_working_camera_index(6)
                if fallback_index is not None:
                    st.session_state['camera_index'] = fallback_index
                    cap, _ = open_camera(fallback_index)
            if cap is None:
                st.error('Camera unavailable. Close other camera apps and try again.')
                return
            frame = read_frame_with_retry(cap)
            cap.release()
            if frame is None:
                st.error('Camera frame read failed. Please try again.')
            else:
                st.session_state['last_frame'] = frame
                frame_placeholder.image(frame, channels='BGR')
                boxes = face_utils.detect_faces(frame)
                if not boxes:
                    st.warning('No face detected! Try again.')
                else:
                    encodings = face_utils.encode_faces(frame, boxes)
                    if encodings:
                        samples.append(encodings[0])
                        st.session_state['samples'] = samples
                        st.session_state['captured'] = captured + 1
                        st.success(f'Sample {captured+1} captured!')
                    else:
                        st.warning('Face encoding failed! Try again.')
        st.write(f"Samples captured: {len(samples)}/5")
        if len(samples) == 5:
            avg_encoding = np.mean(samples, axis=0)
            if st.button('Save Registration'):
                user_id = st.session_state['reg_user_id']
                face_utils.add_encoding(avg_encoding, user_id, st.session_state['reg_name'], st.session_state['reg_department'])
                db.register_user(user_id, st.session_state['reg_name'], st.session_state['reg_department'])
                st.success('User registered successfully!')
                st.session_state['samples'] = []
                st.session_state['captured'] = 0
                st.session_state['last_frame'] = None
                st.session_state['registration_ready'] = False

# --- Mark Attendance (Live Camera) ---
def mark_attendance_camera():
    st.title('📷 Mark Attendance (Live Camera)')
    threshold = st.slider('Confidence Threshold (%)', 60, 100, 70)
    st.caption('Click "Capture Frame" to read from webcam and mark attendance.')

    if not st.button('Capture Frame', key='capture_camera_frame'):
        return

    current_camera_index = int(st.session_state['camera_index'])
    cap, backend_name = open_camera(current_camera_index)
    if cap is None:
        fallback_index = find_working_camera_index(6)
        if fallback_index is not None:
            st.session_state['camera_index'] = fallback_index
            current_camera_index = fallback_index
            cap, backend_name = open_camera(current_camera_index)
    if cap is None:
        st.error('Unable to access camera. Close Zoom/Teams/Camera app and retry.')
        return

    start = time.time()
    frame = read_frame_with_retry(cap)
    cap.release()
    if frame is None:
        st.error('Camera frame read failed. Please reconnect camera and retry.')
        return

    small = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
    boxes = face_utils.detect_faces(small)
    encodings = face_utils.encode_faces(small, boxes)
    names = []
    for encoding in encodings:
        user, conf = face_utils.recognize(encoding, threshold=1-threshold/100)
        if user and conf >= threshold:
            if user['id'] not in st.session_state['marked_today']:
                if db.mark_attendance(user['id'], user['name'], user['department'], conf, 'Camera'):
                    st.session_state['marked_today'].add(user['id'])
                    st.success(f"Attendance marked for {user['name']} ({conf:.1f}%)")
                else:
                    st.info('Already marked today!')
            names.append(user['name'])
        else:
            names.append('Unknown')
            st.warning('Unknown face detected!')

    out_frame = face_utils.draw_boxes(small, boxes, names)
    st.image(out_frame, channels='BGR')
    fps = 1/(time.time()-start)
    st.caption(f'Camera index: {current_camera_index} | backend: {backend_name} | capture FPS: {fps:.2f}')

# --- Upload Image ---
def upload_image():
    st.title('🖼️ Upload Image')
    threshold = st.slider('Confidence Threshold (%)', 60, 100, 70)
    uploaded = st.file_uploader('Upload an image', type=['jpg', 'png'])
    if uploaded:
        file_bytes = np.asarray(bytearray(uploaded.read()), dtype=np.uint8)
        frame = cv2.imdecode(file_bytes, 1)
        boxes = face_utils.detect_faces(frame)
        encodings = face_utils.encode_faces(frame, boxes)
        names = []
        for encoding in encodings:
            user, conf = face_utils.recognize(encoding, threshold=1-threshold/100)
            if user and conf >= threshold:
                if user['id'] not in st.session_state['marked_today']:
                    if db.mark_attendance(user['id'], user['name'], user['department'], conf, 'Image'):
                        st.session_state['marked_today'].add(user['id'])
                        st.success(f"Attendance marked for {user['name']} ({conf:.1f}%)")
                    else:
                        st.info('Already marked today!')
                names.append(user['name'])
            else:
                names.append('Unknown')
                st.warning('Unknown face detected!')
        frame = face_utils.draw_boxes(frame, boxes, names)
        st.image(frame, channels='BGR')

# --- Upload Video ---
def upload_video():
    st.title('🎥 Upload Video')
    threshold = st.slider('Confidence Threshold (%)', 60, 100, 70)
    uploaded = st.file_uploader('Upload a video', type=['mp4', 'avi'])
    if uploaded:
        tfile = os.path.join('data', f'temp_{int(time.time())}.mp4')
        with open(tfile, 'wb') as f:
            f.write(uploaded.read())
        cap = cv2.VideoCapture(tfile)
        fps_display = st.empty()
        frame_display = st.empty()
        stop_button_placeholder = st.empty()
        while cap.isOpened():
            start = time.time()
            ret, frame = cap.read()
            if not ret:
                break
            small = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
            boxes = face_utils.detect_faces(small)
            encodings = face_utils.encode_faces(small, boxes)
            names = []
            for encoding in encodings:
                user, conf = face_utils.recognize(encoding, threshold=1-threshold/100)
                if user and conf >= threshold:
                    if user['id'] not in st.session_state['marked_today']:
                        if db.mark_attendance(user['id'], user['name'], user['department'], conf, 'Video'):
                            st.session_state['marked_today'].add(user['id'])
                            st.success(f"Attendance marked for {user['name']} ({conf:.1f}%)")
                        else:
                            st.info('Already marked today!')
                    names.append(user['name'])
                else:
                    names.append('Unknown')
                    st.warning('Unknown face detected!')
            frame = face_utils.draw_boxes(small, boxes, names)
            frame_display.image(frame, channels='BGR')
            fps = 1/(time.time()-start)
            fps_display.text(f'FPS: {fps:.2f}')
            if stop_button_placeholder.button('Stop Video', key='stop_video_btn'):
                break
        cap.release()
        os.remove(tfile)

# --- Attendance Records ---
def attendance_records():
    st.title('📋 Attendance Records')
    records = db.get_attendance_records()
    df = pd.DataFrame(records, columns=['ID', 'User ID', 'Name', 'Department', 'Date', 'Time', 'Confidence', 'Source'])
    st.dataframe(df)
    st.download_button('Download CSV', df.to_csv(index=False), file_name='attendance.csv')

    st.subheader('Delete User by User ID')
    user_id_to_delete = st.text_input('Enter User ID to delete user and all their attendance records:')
    if st.button('Delete User'):
        if user_id_to_delete:
            # Remove from DB and face encodings
            user = db.get_user(user_id_to_delete)
            if user:
                db.delete_user(user_id_to_delete)
                face_utils.delete_user(user_id_to_delete)
                st.success(f'User {user_id_to_delete} deleted successfully!')
            else:
                st.warning('User ID not found.')
        else:
            st.warning('Please enter a User ID.')

# --- Analytics ---
def analytics():
    st.title('📈 Advanced Analytics Dashboard')
    
    users = db.get_all_users()
    attendance_today = db.get_attendance_today()
    total_users = len(users)
    present_today = len(attendance_today)
    absent_today = total_users - present_today
    attendance_pct = (present_today / total_users * 100) if total_users else 0
    
    # Key Metrics with enhanced styling
    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div style='
                background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(59, 130, 246, 0.1) 100%);
                border: 1px solid rgba(59, 130, 246, 0.3);
                border-radius: 12px;
                padding: 20px;
                text-align: center;
            '>
                <div style='color: #64748b; font-size: 0.9em; margin-bottom: 8px;'>Total Users</div>
                <div style='color: #3b82f6; font-size: 2.5em; font-weight: 700;'>""" + str(total_users) + """</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style='
                background: linear-gradient(135deg, rgba(34, 197, 94, 0.2) 0%, rgba(34, 197, 94, 0.1) 100%);
                border: 1px solid rgba(34, 197, 94, 0.3);
                border-radius: 12px;
                padding: 20px;
                text-align: center;
            '>
                <div style='color: #64748b; font-size: 0.9em; margin-bottom: 8px;'>Present Today</div>
                <div style='color: #22c55e; font-size: 2.5em; font-weight: 700;'>""" + str(present_today) + """</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div style='
                background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(239, 68, 68, 0.1) 100%);
                border: 1px solid rgba(239, 68, 68, 0.3);
                border-radius: 12px;
                padding: 20px;
                text-align: center;
            '>
                <div style='color: #64748b; font-size: 0.9em; margin-bottom: 8px;'>Absent Today</div>
                <div style='color: #ef4444; font-size: 2.5em; font-weight: 700;'>""" + str(absent_today) + """</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, rgba(06, 182, 212, 0.2) 0%, rgba(06, 182, 212, 0.1) 100%);
                border: 1px solid rgba(06, 182, 212, 0.3);
                border-radius: 12px;
                padding: 20px;
                text-align: center;
            '>
                <div style='color: #64748b; font-size: 0.9em; margin-bottom: 8px;'>Attendance %</div>
                <div style='color: #06b6d4; font-size: 2.5em; font-weight: 700;'>{attendance_pct:.1f}%</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
    
    # Charts section with tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Trends", "🏢 Department", "👥 Details", "📅 Calendar", "⚡ Insights"])
    
    with tab1:
        st.subheader("Attendance Trend (Last 30 Days)")
        trend = db.get_attendance_trend()
        if trend:
            df_trend = pd.DataFrame(trend, columns=['Date', 'Count'])
            df_trend = df_trend.sort_values('Date')
            fig = px.line(
                df_trend, 
                x='Date', 
                y='Count',
                markers=True,
                line_shape='spline',
                title='Daily Attendance Pattern',
                labels={'Count': 'Attendance Count', 'Date': 'Date'},
                color_discrete_sequence=['#06b6d4']
            )
            fig.update_layout(
                template='plotly_dark',
                plot_bgcolor='rgba(30, 41, 59, 0.5)',
                paper_bgcolor='rgba(15, 23, 42, 0)',
                font=dict(color='#cbd5e1'),
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Department-wise Attendance")
        dept_data = db.get_department_attendance()
        if dept_data:
            df_dept = pd.DataFrame(dept_data, columns=['Department', 'Count'])
            fig = px.bar(
                df_dept, 
                x='Department', 
                y='Count',
                title='Attendance by Department',
                color='Count',
                color_continuous_scale='Viridis',
                labels={'Count': 'Present', 'Department': 'Department'}
            )
            fig.update_layout(
                template='plotly_dark',
                plot_bgcolor='rgba(30, 41, 59, 0.5)',
                paper_bgcolor='rgba(15, 23, 42, 0)',
                font=dict(color='#cbd5e1'),
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Attendance Details")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Present vs Absent Today**")
            present_vs_absent = pd.DataFrame({
                'Status': ['Present', 'Absent'],
                'Count': [present_today, absent_today]
            })
            fig = px.pie(
                present_vs_absent,
                names='Status',
                values='Count',
                color_discrete_map={'Present': '#22c55e', 'Absent': '#ef4444'},
                title='Distribution'
            )
            fig.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(15, 23, 42, 0)',
                font=dict(color='#cbd5e1')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("**Monthly Summary**")
            monthly_data = db.get_attendance_trend() if hasattr(db, 'get_attendance_trend') else []
            if monthly_data:
                df_monthly = pd.DataFrame(monthly_data, columns=['Date', 'Count'])
                df_monthly['Month'] = pd.to_datetime(df_monthly['Date']).dt.to_period('M')
                monthly_summary = df_monthly.groupby('Month')['Count'].mean()
                
                fig = px.bar(
                    x=monthly_summary.index.astype(str),
                    y=monthly_summary.values,
                    labels={'x': 'Month', 'y': 'Avg Attendance'},
                    title='Monthly Average Attendance',
                    color_discrete_sequence=['#06b6d4']
                )
                fig.update_layout(
                    template='plotly_dark',
                    plot_bgcolor='rgba(30, 41, 59, 0.5)',
                    paper_bgcolor='rgba(15, 23, 42, 0)',
                    font=dict(color='#cbd5e1'),
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.subheader("Calendar View")
        st.info("📅 Calendar heatmap would display attendance patterns by date and time")
        
        # Display sample calendar data
        trend = db.get_attendance_trend()
        if trend:
            df_trend = pd.DataFrame(trend, columns=['Date', 'Count'])
            df_trend['Date'] = pd.to_datetime(df_trend['Date'])
            df_trend = df_trend.sort_values('Date').tail(14)
            
            st.dataframe(
                df_trend.assign(**{'Date': df_trend['Date'].dt.strftime('%Y-%m-%d')}),
                use_container_width=True,
                hide_index=True
            )
    
    with tab5:
        st.subheader("Key Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Attendance rate
            if attendance_pct >= 80:
                st.success(f"✅ Excellent attendance rate: {attendance_pct:.1f}%")
            elif attendance_pct >= 60:
                st.warning(f"⚠️ Good attendance rate: {attendance_pct:.1f}%")
            else:
                st.error(f"❌ Low attendance rate: {attendance_pct:.1f}%")
        
        with col2:
            # Absence analysis
            if absent_today == 0:
                st.success("✅ Perfect attendance today!")
            elif absent_today <= 3:
                st.info(f"📊 {absent_today} person(s) absent today")
            else:
                st.warning(f"⚠️ {absent_today} people absent today")
        
        # Additional statistics
        st.markdown("---")
        st.markdown("**Summary Statistics**")
        
        summary_col1, summary_col2, summary_col3 = st.columns(3)
        
        with summary_col1:
            total_registered = len(users)
            st.metric("Total Registered", total_registered)
        
        with summary_col2:
            attendance_rate_avg = attendance_pct
            st.metric("Today's Rate", f"{attendance_rate_avg:.1f}%")
        
        with summary_col3:
            st.metric("Absence Count", absent_today)

# --- Main Routing ---
if choice == 'Dashboard':
    dashboard()
elif choice == 'Register New User':
    register_user()
elif choice == 'Mark Attendance (Live Camera)':
    mark_attendance_camera()
elif choice == 'Upload Image':
    upload_image()
elif choice == 'Upload Video':
    upload_video()
elif choice == 'Attendance Records':
    attendance_records()
elif choice == 'Analytics':
    analytics()
