import streamlit as st
from streamlit.errors import StreamlitAPIException

st.set_page_config(
    page_title="Aura AI Studio",
    page_icon="AI",
    layout="wide",
    initial_sidebar_state="expanded",
)

from Aura_AI.chatbot_ui import chatbot_ui
from Aura_AI.playfield_ui import playfield_ui
from Aura_AI.ai_assistant_ui import ai_assistant_page
from Backward_Propagation.backward_propagation import backward_propagation_page
from Deep_Belief_Network.dbn_ui import dbn_page
from Forward_Propagation.forward_propagation import forward_propagation_page
from Gradient_Descent.gradient_descent_ui import gradient_descent_page
from Hopfield.hopfield_ui import hopfield_page
try:
    from OpenCV_Detection.opencv_hub import (
        opencv_attendance_page,
        opencv_detection_page,
        opencv_face_scan_page,
        opencv_palm_page,
        opencv_sign_page,
        opencv_vehicle_page,
    )
    OPENCV_AVAILABLE = True
except ImportError as e:
    OPENCV_AVAILABLE = False
    OPENCV_ERROR = str(e)
from Perceptron.perceptron_ui import perceptron_page
from Sentiment_Analysis.sentiment_analysis import sentiment_analysis_page
from utils.ai_sidebar import render_global_ai_hub, render_global_robot
from utils.styles import inject_global_css, get_base64_bin_str


MODULE_REGISTRY = {
    "home": {"label": "Home", "render": None},
    "aura_chat": {"label": "Aura Assistant", "render": chatbot_ui},
    "aura_playfield": {"label": "Deep Playfield", "render": playfield_ui},
    "aura_ai_studio": {"label": "AI Assistant Studio", "render": ai_assistant_page},
    "m1": {"label": "Perceptron", "render": perceptron_page},
    "m2": {"label": "Forward Propagation", "render": forward_propagation_page},
    "m3": {"label": "Backward Propagation", "render": backward_propagation_page},
    "m_gd": {"label": "Gradient Descent", "render": gradient_descent_page},
    "m4": {"label": "Sentiment Intelligence", "render": sentiment_analysis_page},
    "m5": {"label": "Associative Memory", "render": hopfield_page},
    "m6": {"label": "Optical Intelligence", "render": opencv_detection_page},
    "cv_gallery": {"label": "OpenCV Gallery", "render": opencv_detection_page},
    "cv_attendance": {"label": "OpenCV Attendance", "render": opencv_attendance_page},
    "cv_face_scan": {"label": "OpenCV Face Scanner", "render": opencv_face_scan_page},
    "cv_vehicle": {"label": "OpenCV Vehicle", "render": opencv_vehicle_page},
    "cv_sign": {"label": "OpenCV Sign Detection", "render": opencv_sign_page},
    "cv_palm": {"label": "OpenCV Palm Reading", "render": opencv_palm_page},
    "m7": {"label": "Deep Belief Network", "render": dbn_page},
}


def _is_columns_nesting_error(exc: Exception) -> bool:
    msg = str(exc)
    return (
        "Columns can only be placed inside other columns up to one level of nesting" in msg
        or "Columns may not be nested inside other columns" in msg
    )


def sidebar_navigation():
    st.sidebar.markdown(
        """
        <div style="text-align:center; margin-bottom:28px;">
            <div style="font-size:44px; font-weight:800; color:#F8FAFC;
                background:linear-gradient(90deg, #60A5FA, #22D3EE, #34D399);
                -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
                AURA
            </div>
            <div style="color:#94A3B8; font-size:12px; font-weight:700; letter-spacing:3px;">
                AI STUDIO CONTROL
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    sections = {
        "Studio": {"Aura Dashboard": "home"},
        "AI": {
            "AI Architect Chat": "aura_chat",
            "Deep Playfield": "aura_playfield",
            "AI Assistant Studio": "aura_ai_studio",
        },
        "Core Mechanics": {
            "Perceptron Engine": "m1",
            "Forward Synapse": "m2",
            "Backward Gradient": "m3",
            "Descent Optimization": "m_gd",
        },
        "Advanced Systems": {
            "Associative Memory": "m5",
            "Semantic NLP Engine": "m4",
            "Optical Intelligence": "m6",
            "Deep Belief Network": "m7",
        },
    }

    active_selection = st.session_state.get("nav_selection", "home")
    for section, entries in sections.items():
        st.sidebar.markdown(
            f"""
            <div style="font-size:11px; color:#94A3B8; font-weight:800;
                text-transform:uppercase; letter-spacing:1.8px; margin-top:22px; margin-bottom:12px;">
                {section}
            </div>
            """,
            unsafe_allow_html=True,
        )
        for label, value in entries.items():
            button_type = "primary" if active_selection == value else "secondary"
            if st.sidebar.button(label, key=f"nav_{value}", use_container_width=True, type=button_type):
                st.session_state["nav_selection"] = value
                st.rerun()

    return st.session_state.get("nav_selection", "home")


def app_home():
    inject_global_css()
    
    # Hero Section with Image (Local Asset with Base64 fallback)
    hero_b64 = get_base64_bin_str("assets/dashboard_hero_1776259997183.png")
    hero_url = f"data:image/png;base64,{hero_b64}" if hero_b64 else "https://images.unsplash.com/photo-1620712943543-bcc4638ef80b?auto=format&fit=crop&q=80&w=1600"
    
    st.markdown(
        f"""
        <div style="background: linear-gradient(rgba(10,14,26,0.8), rgba(10,14,26,0.8)), 
                    url('{hero_url}');
                    background-size: cover; background-position: center;
                    border-radius: 32px; padding: 80px 40px; text-align: center; margin-bottom: 60px;
                    border: 1px solid rgba(34, 211, 238, 0.2); box-shadow: 0 20px 60px rgba(0,0,0,0.6);">
            <div style="display:inline-block; border:1px solid rgba(52,211,153,0.4);
                background:rgba(52,211,153,0.1); padding:8px 20px; border-radius:999px; margin-bottom:24px; backdrop-filter: blur(10px);">
                <span style="color:#34D399; font-size:12px; font-weight:700; letter-spacing:2px;">SYSTEM ONLINE</span>
            </div>
            <h1 style="font-size:72px; margin:0; font-weight:800; color:#F8FAFC; line-height:1.05; text-shadow: 0 10px 30px rgba(0,0,0,0.5);">
                Aura AI Studio
            </h1>
            <p style="font-size:20px; color:#CBD5E1; max-width:840px; margin:28px auto 0; line-height:1.8; font-weight: 500;">
                Architecting the future of neural intelligence through interactive synthesis.
                Explore advanced models with our global assistant and high-fidelity visual engine.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cards = [
        {
            "id": "m1", 
            "title": "Perceptron Engine", 
            "desc": "Binary linear classification mechanics.",
            "img": "assets/m1_perceptron_1776260062584.png"
        },
        {
            "id": "m2", 
            "title": "Forward Synapse", 
            "desc": "Non-linear signal flow through deep layers.",
            "img": "assets/m2_forward_synapse_1776260230911.png"
        },
        {
            "id": "m3", 
            "title": "Backward Gradient", 
            "desc": "Optimization via error backpropagation.",
            "img": "assets/m3_backward_gradient_1776260275678.png"
        },
        {
            "id": "m5", 
            "title": "Associative Memory", 
            "desc": "Pattern recall in Hopfield energy basins.",
            "img": "assets/m5_associative_memory_1776260558181.png"
        },
        {
            "id": "m4", 
            "title": "Semantic NLP", 
            "desc": "Sequence modeling with LSTM intelligence.",
            "img": "assets/m4_semantic_nlp_1776260699489.png"
        },
        {
            "id": "m6", 
            "title": "Optical Vision", 
            "desc": "Real-time OpenCV detection pipelines.",
            "img": "assets/dashboard_image_1.jpg"
        },
        {
            "id": "m7", 
            "title": "Deep Belief Net", 
            "desc": "Stacked RBM pretraining and latent features.",
            "img": "assets/dashboard_image_2.jpg"
        },
    ]

    from utils.styles import image_card
    cols = st.columns(3)
    for index, card in enumerate(cards):
        with cols[index % 3]:
            image_card(card["title"], card["desc"], card["img"])
            if st.button(f"Launch {card['title']}", key=f"home_{card['id']}", use_container_width=True):
                st.session_state["nav_selection"] = card["id"]
                st.rerun()


def main():
    selection = sidebar_navigation()
    module = MODULE_REGISTRY.get(selection, MODULE_REGISTRY["home"])
    module_label = module["label"]

    render_global_ai_hub(module_label)
    render_global_robot(module_label)

    if selection == "home":
        app_home()
        return

    if selection in ["m6", "cv_gallery", "cv_attendance", "cv_face_scan", "cv_vehicle", "cv_sign", "cv_palm"]:
        if not OPENCV_AVAILABLE:
            st.error("### 🛑 Computer Vision Module Unavailable")
            st.warning(f"Error: `{OPENCV_ERROR}`")
            st.info("""
                This is usually due to missing system libraries on Streamlit Cloud. 
                
                **To resolve this:**
                1. Ensure `packages.txt` exists in your root directory.
                2. Add `libgl1` to it.
                3. If the error persists, try adding `ffmpeg` or `libglib2.0-dev` (checking for conflicts).
                
                The app is currently rebuilding to try and resolve this automatically.
            """)
            return

    renderer = module["render"]
    if renderer:
        try:
            renderer()
        except StreamlitAPIException as exc:
            if _is_columns_nesting_error(exc):
                st.warning("This module hit a layout compatibility constraint and was stopped safely.")
                st.info("Technical traceback has been hidden to keep the app responsive.")
                st.caption(f"Module: {module_label}")
                return
            raise


if __name__ == "__main__":
    main()
