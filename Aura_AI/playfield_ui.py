import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time
from utils.styles import inject_global_css, gradient_header, premium_card_wrapper, stat_card, section_header
from utils.nn_helpers import plotly_layout, C, P, G, R, hex2rgba

def playfield_ui():
    inject_global_css()
    gradient_header("Deep Playfield", "Neural Topology Sandbox · Real-time Weight Visualizer", "🧬", img_path="https://images.unsplash.com/photo-1620712014386-11236ba02deb?auto=format&fit=crop&q=90&w=1200")

    st.markdown("""
        <div class="premium-card" style="border-left: 5px solid #818CF8;">
            <p style="margin:0; font-size:16px;">
                Welcome to the <b>Synaptic Sandbox</b>. This is an experimental coordinate space where you can 
                manually trigger neural pulses and watch the signal propagate through virtual layers.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Sidebar Toolbox Settings
    with st.sidebar:
        section_header("Synaptic Calibration", "Tune signal parameters")
        strength = st.slider("Signal Pulse Strength", 0.0, 10.0, 5.0)
        noise = st.slider("Environmental Noise", 0.0, 1.0, 0.2)
        layers = st.number_input("Virtual Layer Depth", 1, 12, 4)
        
        if st.button("🚀 INJECT SIGNAL PULSE", use_container_width=True, type="primary"):
            st.session_state.pulse_active = True
            st.rerun()

    # Main Visual Space
    st.markdown("<br>", unsafe_allow_html=True)
    if st.session_state.get("pulse_active", False):
        ph = st.empty()
        history = []
        
        for i in range(25):
            val = strength * np.sin(i * 0.5) + np.random.randn() * noise
            history.append(val)
            
            with ph.container():
                fig = go.Figure(data=[
                    go.Scatter(y=history, mode='lines+markers', 
                              line=dict(color=P, width=3), 
                              marker=dict(size=8, color=C, line=dict(width=2, color="#FFF")))
                ])
                fig.update_layout(title="Synaptic Signal Propagation", **plotly_layout(height=400))
                st.plotly_chart(fig, use_container_width=True, theme=None, key=f"play_pulse_{i}")
                time.sleep(0.05)
        
        st.session_state.pulse_active = False
        st.success("Signal pulse successfully integrated into substrate.")
    else:
        st.markdown(f"""
            <div class="premium-card" style="text-align:center; padding:100px 20px; border-style:dashed; border-color:rgba(129,140,248,0.3);">
                <div style="font-size:60px; margin-bottom:20px; opacity:0.5;">📡</div>
                <div style="color:#94A3B8; font-weight:700; text-transform:uppercase; letter-spacing:2px;">Awaiting Signal Injection</div>
            </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    playfield_ui()
