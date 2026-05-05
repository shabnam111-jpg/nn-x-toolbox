import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import time
from plotly.subplots import make_subplots
from utils.styles import section_header, render_log, render_nlp_insight, gradient_header, inject_global_css, stat_card, render_theory_card
from utils.nlp_engine import generate_perceptron_insight
from utils.nn_helpers import P, C, G, A, R, TEXT, MUTED, GRID, BG, PLOTLY_BASE, plotly_layout
from utils.ai_sidebar import render_ai_sidebar

GATES = {
    "AND":  {"data":[(0,0,0),(0,1,0),(1,0,0),(1,1,1)],"sep":True, "icon":"⊗"},
    "OR":   {"data":[(0,0,0),(0,1,1),(1,0,1),(1,1,1)],"sep":True, "icon":"⊕"},
    "NAND": {"data":[(0,0,1),(0,1,1),(1,0,1),(1,1,0)],"sep":True, "icon":"↑"},
    "NOR":  {"data":[(0,0,1),(0,1,0),(1,0,0),(1,1,0)],"sep":True, "icon":"↓"},
    "XOR":  {"data":[(0,0,0),(0,1,1),(1,0,1),(1,1,0)],"sep":False,"icon":"⊻"},
    "XNOR": {"data":[(0,0,1),(0,1,0),(1,0,0),(1,1,1)],"sep":False,"icon":"⊙"},
}

def _live_dashboard_fig(X, y, w, b, losses, acc, ep, max_ep):
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Decision Boundary", "Live Loss Curve"))
    
    for cls, col, sym in [(0, R, "circle"), (1, G, "diamond")]:
        m = y == cls
        if m.any():
            fig.add_trace(go.Scatter(x=X[m,0], y=X[m,1], mode="markers",
                name=f"Class {cls}",
                marker=dict(size=14, color=col, line=dict(width=1.5, color="#FFF"), symbol=sym)),
                row=1, col=1)
    
    if abs(w[1]) > 1e-9:
        xs = np.linspace(X[:,0].min()-0.5, X[:,0].max()+0.5, 300)
        ys = -(w[0]*xs+b)/w[1]
        fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", name="Boundary",
            line=dict(color=P, width=3, dash="dash")), row=1, col=1)
    
    ep_x = list(range(1, len(losses)+1))
    fig.add_trace(go.Scatter(x=ep_x, y=losses, mode="lines", fill="tozeroy",
        name="Total Error", line=dict(color=C, width=3),
        fillcolor="rgba(34, 211, 238, 0.1)"), row=1, col=2)
    
    fig.update_layout(
        title_text=f"Live Convergence Dashboard — Epoch {ep}/{max_ep} | Accuracy: {acc:.1f}%",
        **plotly_layout(height=420)
    )
    return fig

def perceptron_page():
    inject_global_css()
    gradient_header(
        "Neural Perceptron", 
        "Linear Binary Classification · Weight Convergence Matrix", 
        "⚡",
        img_path="https://images.unsplash.com/photo-1620712943543-bcc4638ef80b?auto=format&fit=crop&q=80&w=1200"
    )

    col_main, col_ai = st.columns([3, 1])
    
    with col_ai:
        render_ai_sidebar("Perceptron")
    
    with col_main:
        render_theory_card(
            "The Perceptron Learning Rule",
            """
            The perceptron is the fundamental building block of neural networks. It computes a linear 
            combination of inputs and applies a step function activation.<br><br>
            <b>1. Forward Pass:</b> z = Σ wᵢxᵢ + b <br>
            <b>2. Activation:</b> ŷ = 1 if z ≥ 0 else 0 <br>
            <b>3. Learning:</b> Weights are adjusted only when the prediction is wrong: Δw = η(y - ŷ)x.
            """,
            formulas=["z = w · x + b", "ŷ = f(z)", "Δw = η(y - ŷ)x"]
        )

        st.markdown("<br>", unsafe_allow_html=True)
        section_header("1. Dataset Hub", "Define input space and linear constraints")
        with st.container(border=True):
            c1, c2 = st.columns([1,1])
            with c1:
                gate = st.selectbox("Logic Gate Architecture", list(GATES.keys()), index=0)
                ginfo = GATES[gate]
                X = np.array([[r[0],r[1]] for r in ginfo["data"]], dtype=float)
                y = np.array([r[2] for r in ginfo["data"]], dtype=int)
                if not ginfo["sep"]: st.warning("Notice: This gate is not linearly separable (XOR/XNOR).")
            with c2:
                df_tt = pd.DataFrame(ginfo["data"], columns=["X1","X2","Target"])
                st.dataframe(df_tt, use_container_width=True, hide_index=True)

        section_header("2. Hyperparameter Forge", "Calibrate synaptic plasticity")
        with st.container(border=True):
            h1, h2, h3 = st.columns(3)
            lr = h1.number_input("Learning Rate (η)", 0.001, 1.0, 0.1, 0.01)
            max_ep = h2.slider("Max Epochs", 10, 500, 100)
            delay = h3.slider("Animation Latency (s)", 0.0, 0.5, 0.05, 0.05)

        if st.button("🚀 INITIATE TRAINING SESSION", type="primary", use_container_width=True):
            st.session_state.perc_triggered = True
            st.session_state.perc_animate = True

        if st.session_state.get("perc_triggered", False):
            master_ph = st.empty()
            
            if st.session_state.get("perc_animate", False):
                w = np.random.uniform(-0.5, 0.5, 2)
                b = np.random.uniform(-0.5, 0.5)
                losses = []
                
                for ep in range(1, max_ep+1):
                    err = 0
                    for xi, yi in zip(X, y):
                        z = np.dot(w, xi) + b
                        pred = 1 if z >= 0 else 0
                        e = yi - pred
                        err += abs(e)
                        if e != 0:
                            w += lr * e * xi
                            b += lr * e
                    
                    losses.append(err)
                    acc = int(np.sum((X@w+b>=0).astype(int)==y)) / len(y) * 100
                    
                    with master_ph.container():
                        m1, m2, m3, m4 = st.columns(4)
                        stat_card("Epoch", ep, "🔄")
                        stat_card("Error", f"{err:.1f}", "📉", color=R)
                        stat_card("Accuracy", f"{acc:.1f}%", "🎯", color=G)
                        stat_card("Bias", f"{b:.2f}", "⚖️", color=C)
                        
                        st.plotly_chart(_live_dashboard_fig(X, y, w, b, losses, acc, ep, max_ep), use_container_width=True, theme=None, key=f"p_live_{ep}")
                    
                    if delay > 0: time.sleep(delay)
                    if err == 0: break
                
                st.session_state.perc_w = w
                st.session_state.perc_b = b
                st.session_state.perc_losses = losses
                st.session_state.perc_acc = acc
                st.session_state.perc_ep = ep
                st.session_state.perc_err = err
                st.session_state.perc_animate = False
                st.success(f"System: Convergence achieved at Epoch {ep}.")
            else:
                w = st.session_state.perc_w
                b = st.session_state.perc_b
                losses = st.session_state.perc_losses
                acc = st.session_state.perc_acc
                ep = st.session_state.perc_ep
                err = st.session_state.perc_err
                
                with master_ph.container():
                    m1, m2, m3, m4 = st.columns(4)
                    stat_card("Epoch", ep, "🔄")
                    stat_card("Error", f"{err:.1f}", "📉", color=R)
                    stat_card("Accuracy", f"{acc:.1f}%", "🎯", color=G)
                    stat_card("Bias", f"{b:.2f}", "⚖️", color=C)
                    st.plotly_chart(_live_dashboard_fig(X, y, w, b, losses, acc, ep, max_ep), use_container_width=True, theme=None)
            
            insight = generate_perceptron_insight(ep, acc/100, err, acc == 100.0)
            render_nlp_insight(insight, "AI Core Analysis // Decision Boundary Insight", A)
        
        # ========== LIVE NEURAL NETWORK SIMULATION ==========
        st.divider()
        section_header("3. Live Neural Animation", "Real-time weight & signal visualization")
        
        col_sim1, col_sim2 = st.columns([1.5, 1])
        
        with col_sim1:
            st.markdown("**Dynamic Network Evolution**")
            
            if st.button("🧠 VISUALIZE NETWORK DYNAMICS", type="primary", use_container_width=True, key="perceptron_viz"):
                # Simulate network with live visualization
                np.random.seed(42)
                
                # Initialize with trained weights or random
                w_sim = np.array([0.5, -0.3])
                b_sim = 0.1
                
                weights_history = []
                activations_history = []
                
                sim_progress = st.progress(0)
                sim_status = st.empty()
                
                # Simulation steps
                for step in range(50):
                    # Feed random inputs
                    x_input = np.random.randn(2)
                    activation = np.dot(w_sim, x_input) + b_sim
                    
                    # Update weights slightly
                    w_sim += np.random.randn(2) * 0.05
                    b_sim += np.random.randn() * 0.05
                    
                    weights_history.append(w_sim.copy())
                    activations_history.append(activation)
                    
                    sim_progress.progress((step + 1) / 50)
                    sim_status.info(f"Simulation Step {step+1}/50 | Activation: {activation:.3f}")
                    time.sleep(0.05)
                
                sim_progress.empty()
                sim_status.empty()
                
                # Visualize 3D weight trajectory
                weights_array = np.array(weights_history)
                
                fig_weights = go.Figure()
                fig_weights.add_trace(go.Scatter3d(
                    x=weights_array[:, 0], y=weights_array[:, 1], z=activations_history,
                    mode='markers+lines',
                    marker=dict(
                        size=6,
                        color=np.arange(len(weights_array)),
                        colorscale='Viridis',
                        showscale=False
                    ),
                    line=dict(color=C, width=4),
                    name='3D Phase Plot',
                    hovertemplate='W1:%{x:.3f} | W2:%{y:.3f} | Act:%{z:.3f}<extra></extra>',
                ))
                
                fig_weights.update_layout(
                    title="Live Simulation: 3D Parameter & Activation Space",
                    scene=dict(xaxis_title="W1", yaxis_title="W2", zaxis_title="Neuron Activation"),
                    **plotly_layout(height=400)
                )
                
                st.plotly_chart(fig_weights, use_container_width=True, theme=None)
                fig_act = go.Figure()
                fig_act.add_trace(go.Scatter(
                    y=activations_history,
                    mode='lines',
                    fill='tozeroy',
                    line=dict(color=P, width=2),
                    fillcolor=f"rgba({int(P[1:3], 16)}, {int(P[3:5], 16)}, {int(P[5:7], 16)}, 0.2)",
                    name='Activation Signal'
                ))
                
                fig_act.update_layout(
                    title="Live Neural Activation Signal",
                    xaxis_title="Time Step",
                    yaxis_title="Activation",
                    **plotly_layout(height=300)
                )
                
                st.plotly_chart(fig_act, use_container_width=True, theme=None)
        
        with col_sim2:
            st.markdown("**Network Metrics**")
            st.markdown(f"""
            <div class="stat-card" style="padding:20px; border-left:4px solid {P}; margin-bottom:10px;">
                <div style="font-size:12px; color:{MUTED};">Input Neurons</div>
                <div style="font-size:20px; font-weight:bold;">2</div>
            </div>
            <div class="stat-card" style="padding:20px; border-left:4px solid {C}; margin-bottom:10px;">
                <div style="font-size:12px; color:{MUTED};">Output Neurons</div>
                <div style="font-size:20px; font-weight:bold;">1</div>
            </div>
            <div class="stat-card" style="padding:20px; border-left:4px solid {G};">
                <div style="font-size:12px; color:{MUTED};">Total Weights</div>
                <div style="font-size:20px; font-weight:bold;">2 + 1 bias</div>
            </div>
            """, unsafe_allow_html=True)
