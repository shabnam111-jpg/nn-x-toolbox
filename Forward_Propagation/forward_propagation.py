import streamlit as st
import numpy as np
import time
import plotly.graph_objects as go
from utils.styles import section_header, gradient_header, inject_global_css, render_log, stat_card, render_theory_card
from utils.nn_helpers import draw_network, P, C, G, A, R, TEXT, MUTED, GRID, BG, plotly_layout, hex2rgba
from utils.ai_sidebar import render_ai_sidebar

def sigmoid(z): return 1 / (1 + np.exp(-z))
def relu(z): return np.maximum(0, z)
def identity(z): return z

def forward_propagation_page():
    inject_global_css()
    gradient_header(
        "Forward Synapse", 
        "Multi-Layer Information Flow · Activation Dynamics", 
        "🔄",
        img_path="https://images.unsplash.com/photo-1509228468518-180dd4864904?auto=format&fit=crop&q=80&w=1200"
    )

    col_main, col_ai = st.columns([3, 1])
    
    with col_ai:
        render_ai_sidebar("Forward Propagation")
    
    with col_main:
        render_theory_card(
            "Forward Signal Propagation",
            """
            Forward propagation is the process where input data is transformed layer by layer until it produces 
            an output. Each neuron represents a linear transformation followed by a non-linear activation.<br><br>
            <b>1. Linear Combination:</b> Z = W · A_prev + b <br>
            <b>2. Non-Linear Activation:</b> A = f(Z) <br>
            <b>3. Depth:</b> Deep networks can approximate any continuous function (Universal Approximation Theorem).
            """,
            formulas=[r"Z = W \cdot A_{prev} + b", r"A = \sigma(Z)", r"f(x) = \max(0, x)"]
        )

        st.markdown("<br>", unsafe_allow_html=True)
        section_header("1. Architectural Blueprints", "Configure the neural topology")
        
        with st.container(border=True):
            c1, c2, c3 = st.columns(3)
            num_hidden = c1.number_input("Hidden Layers", 1, 3, 1)
            nodes = [c2.slider(f"Nodes in Layer {i+1}", 1, 8, 4) for i in range(num_hidden)]
            act_choice = c3.selectbox("Activation Signature", ["Sigmoid", "ReLU", "Linear"])
            
            # Full arch: 2 inputs, hidden nodes, 1 output
            arch = [2] + nodes + [1]
            labels = ["Input Layer"] + [f"Hidden {i+1}" for i in range(num_hidden)] + ["Output Prediction"]

        col1, col2 = st.columns([1, 1])
        with col1:
            section_header("2. Input State", "Define the feature vector")
            x1 = st.slider("Feature X1 Intensity", -1.0, 1.0, 0.5)
            x2 = st.slider("Feature X2 Intensity", -1.0, 1.0, -0.2)
            
            st.divider()
            fig_net = draw_network(arch, labels)
            fig_net.update_layout(title="Neural Connection Map", **plotly_layout(height=450))
            st.plotly_chart(fig_net, use_container_width=True, theme=None)

        with col2:
            section_header("3. Synaptic Execution", "Visualizing forward signal flow")
            
            if st.button("🧠 TRIGGER SIGNAL FLOW", type="primary", use_container_width=True):
                st.session_state.fw_triggered = True
                st.session_state.fw_weights = [np.random.randn(arch[i+1], arch[i]) * 0.5 for i in range(len(arch)-1)]
                st.session_state.fw_biases = [np.random.randn(arch[i+1]) * 0.1 for i in range(len(arch)-1)]
                st.session_state.fw_animate = True

            if st.session_state.get("fw_triggered", False):
                ph = st.empty()
                inputs = np.array([x1, x2])
                weights = st.session_state.fw_weights
                biases = st.session_state.fw_biases
                activations = [inputs]
                zs = []
                f = sigmoid if act_choice=="Sigmoid" else relu if act_choice=="ReLU" else identity
                
                if st.session_state.get("fw_animate", False):
                    for i in range(len(weights)):
                        with ph.container():
                            st.info(f"System: Synchronizing Layer {i+1}...")
                            bar = st.progress(0)
                            for p in range(101):
                                time.sleep(0.003); bar.progress(p)
                    st.session_state.fw_animate = False
                
                for i in range(len(weights)):
                    z = np.dot(weights[i], activations[-1]) + biases[i]
                    a = f(z)
                    zs.append(z)
                    activations.append(a)
                
                with ph.container():
                    st.success("Forward Pass Finalized.")
                    res = activations[-1][0]
                    stat_card("Network Prediction", f"{res:.4f}", "🎯", color=P)
                    
                    # 3D Activation Landscape
                    steps = 20
                    x_r = np.linspace(-2, 2, steps)
                    y_r = np.linspace(-2, 2, steps)
                    X, Y = np.meshgrid(x_r, y_r)
                    Z = np.zeros_like(X)
                    for i in range(steps):
                        for j in range(steps):
                            val = np.array([X[i,j], Y[i,j]])
                            for w, b in zip(weights, biases):
                                val = f(np.dot(w, val) + b)
                            Z[i,j] = val[0]
                    
                    fig_surf = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale="Viridis", opacity=0.85)])
                    fig_surf.update_layout(title="Neural Response Surface (Global)", **plotly_layout(height=350))
                    st.plotly_chart(fig_surf, use_container_width=True, theme=None)
            else:
                st.markdown(f"""
                <div class="premium-card" style="text-align:center; padding:80px 20px;">
                    <div style="font-size:50px; margin-bottom:20px;">⚡</div>
                    <div style="color:{MUTED}; font-weight:700;">AWAITING NEURAL TRIGGER</div>
                </div>
                """, unsafe_allow_html=True)
        
        # ========== LIVE LAYER-BY-LAYER ANIMATION ==========
        st.divider()
        section_header("4. Live Activation Flow Animation", "Watch data propagate through network")
        
        if st.button("🎬 ANIMATE FORWARD PASSAGE", type="primary", use_container_width=True, key="forward_anim"):
            num_hidden = len(nodes)
            animation_container = st.container()
            with animation_container:
                st.markdown("**3D Volumetric Signal Propagation**")
                
                for layer_idx in range(num_hidden + 1):
                    col_anim1, col_anim2 = st.columns([1.5, 1])
                    with col_anim1:
                        if layer_idx == 0:
                            layer_name = "Input Layer"
                            values = np.array([x1, x2, (x1+x2)/2])
                        else:
                            layer_name = f"Hidden Layer {layer_idx}" if layer_idx < num_hidden else "Output Layer"
                            values = np.random.randn(nodes[min(layer_idx-1, len(nodes)-1)] * 2) * 0.5 + 0.3
                        
                        # Generate 3D Torus/Surface for active neuron simulation
                        v_len = max(len(values), 3)
                        u = np.linspace(0, 2*np.pi, v_len)
                        v = np.linspace(0, 2*np.pi, v_len)
                        U, V = np.meshgrid(u, v)
                        # Create topological morphing based on neuron activation array
                        X_3d = (2 + np.cos(V)) * np.cos(U) * values.mean() * 3
                        Y_3d = (2 + np.cos(V)) * np.sin(U) * values.std() * 3
                        Z_3d = np.sin(V) + (np.outer(values[:v_len], values[:v_len]) if len(values) >= v_len else np.sin(U))
                        
                        fig_layer = go.Figure(data=[go.Surface(
                            z=Z_3d, x=X_3d, y=Y_3d,
                            colorscale='Plasma' if layer_idx%2==0 else 'Cyan',
                            showscale=False,
                            opacity=0.9
                        )])
                        fig_layer.update_layout(
                            title=f"{layer_name} - 3D Activation Topology",
                            scene=dict(xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False)),
                            **plotly_layout(height=300)
                        )
                        st.plotly_chart(fig_layer, use_container_width=True, theme=None)
                    
                    with col_anim2:
                        st.markdown(f"""
                        <div class="stat-card" style="padding:15px; border-left:4px solid {[P,C,G,R][layer_idx % 4]}; margin-bottom:5px; height:100%;">
                            <div style="font-size:11px; color:{MUTED};">{layer_name}</div>
                            <div style="font-size:14px; font-weight:bold;">{len(values)} Neurons Interfaced</div>
                            <div style="font-size:10px; color:{MUTED}; margin-top:5px;">Activation Amplitude: {np.mean(values):.3f} V</div>
                            <div style="font-size:10px; color:{MUTED};">Signal Variance: {np.std(values):.3f}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    if layer_idx < num_hidden:
                        st.markdown(f'<div style="text-align:center; color:{MUTED}; font-weight:800; padding:10px;">⬇️ TENSOR FLOW ⬇️</div>', unsafe_allow_html=True)
                    time.sleep(0.5)
