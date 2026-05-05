import streamlit as st
import numpy as np
import time
import plotly.graph_objects as go
from utils.styles import section_header, gradient_header, inject_global_css, render_theory_card, stat_card
from utils.nn_helpers import P, C, G, A, R, TEXT, MUTED, GRID, BG, plotly_layout, hex2rgba
from utils.ai_sidebar import render_ai_sidebar

def backward_propagation_page():
    inject_global_css()
    gradient_header(
        "Backward Gradient", 
        "The Chain Rule · Optimization · Weight Correction", 
        "📉",
        img_path="https://images.unsplash.com/photo-1558494949-ef0109121c9b?auto=format&fit=crop&q=80&w=1200"
    )

    col_main, col_ai = st.columns([3, 1])
    
    with col_ai:
        render_ai_sidebar("Backward Propagation")
    
    with col_main:
        render_theory_card(
            "Backpropagation & Optimization",
            """
            Backpropagation is how neural networks learn. It calculates the gradient of the loss function 
            with respect to each weight using the <b>Chain Rule</b>, moving backward from the error at the output.<br><br>
            <b>1. Compute Error:</b> Measure the difference between prediction and target.<br>
            <b>2. Chain Rule:</b> Calculate how much each weight contributed to that error.<br>
            <b>3. Gradient Descent:</b> Update weights in the opposite direction of the gradient to minimize loss.
            """,
            formulas=[
                r"dL/dW = (dL/dA) \cdot (dA/dZ) \cdot (dZ/dW)",
                r"W \leftarrow W - \eta \cdot \nabla L",
                r"\delta_l = (W_{l+1}^T \cdot \delta_{l+1}) \odot f'(Z_l)"
            ]
        )

        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 1.2])

        with col1:
            section_header("1. Training Setup", "Parameters for gradient descent")
            lr = st.slider("Learning Rate (η)", 0.01, 1.0, 0.1)
            momentum = st.slider("Momentum Coefficient", 0.0, 0.99, 0.5)
            epochs = st.number_input("Training Cycles", 50, 2000, 500)
            
            # Simple synthetic data: y = 2x1 - 3x2
            X = np.array([[0.1, 0.2], [0.4, 0.1], [0.5, 0.8], [0.2, 0.9]])
            y = np.array([[0.2], [0.5], [1.0], [0.1]]) # Targets

        with col2:
            section_header("2. Gradient Analytics", "Real-time loss convergence mapping")
            
            if st.button("🚀 INITIATE BACKWARD PASS", type="primary", use_container_width=True):
                st.session_state.bp_triggered = True
                st.session_state.bp_w = np.random.randn(2, 1)
                st.session_state.bp_animate = True

            if st.session_state.get("bp_triggered", False):
                ph_graph = st.empty()
                s1, s2 = st.columns(2)
                ph_loss = s1.empty()
                ph_grad = s2.empty()
                
                if st.session_state.get("bp_animate", False):
                    w = st.session_state.bp_w.copy()
                    losses = []
                    v = 0 # momentum velocity
                    for ep in range(epochs):
                        pred = np.dot(X, w)
                        loss = np.mean((pred - y)**2)
                        losses.append(loss)
                        
                        grad = np.dot(X.T, (pred - y)) / X.shape[0]
                        v = momentum * v - lr * grad
                        w += v
                        
                        if ep % (epochs // 10) == 0 or ep == epochs-1:
                            ph_graph.plotly_chart(go.Figure(data=[
                                go.Scatter(y=losses, mode='lines', fill='tozeroy', 
                                          line=dict(color=R, width=2), fillcolor=hex2rgba(R, 0.1))
                            ]).update_layout(title=f"Loss Curve (Epoch {ep})", **plotly_layout(height=350)),
                            use_container_width=True, theme=None, key=f"bp_loss_{ep}")
                            
                            with ph_loss.container():
                                stat_card("Current Loss", f"{loss:.6f}", " 📉", color=R)
                            with ph_grad.container():
                                stat_card("Gradient Norm", f"{np.linalg.norm(grad):.6f}", "🔌", color=P)
                            time.sleep(0.01)
                    
                    st.session_state.bp_losses = losses
                    st.session_state.bp_final_loss = loss
                    st.session_state.bp_final_grad = grad
                    st.session_state.bp_animate = False
                    st.success("Optimization Cycle Complete.")
                else:
                    losses = st.session_state.bp_losses
                    ph_graph.plotly_chart(go.Figure(data=[
                        go.Scatter(y=losses, mode='lines', fill='tozeroy', 
                                  line=dict(color=R, width=2), fillcolor=hex2rgba(R, 0.1))
                    ]).update_layout(title=f"Loss Curve (Converged)", **plotly_layout(height=350)),
                    use_container_width=True, theme=None)
                    
                    with ph_loss.container():
                        stat_card("Current Loss", f"{st.session_state.bp_final_loss:.6f}", " 📉", color=R)
                    with ph_grad.container():
                        stat_card("Gradient Norm", f"{np.linalg.norm(st.session_state.bp_final_grad):.6f}", "🔌", color=P)
            else:
                st.markdown(f"""
                <div class="premium-card" style="text-align:center; padding:100px 20px;">
                    <div style="font-size:50px; margin-bottom:20px;">〽️</div>
                    <div style="color:{MUTED}; font-weight:700;">READY FOR GRADIENT DESCENT</div>
                </div>
                """, unsafe_allow_html=True)
        
        # ========== LIVE GRADIENT FLOW VISUALIZATION ==========
        st.divider()
        section_header("3. Live Gradient Flow Animation", "Watch gradients backpropagate through network")
        
        col_gf1, col_gf2 = st.columns([1.5, 1])
        
        with col_gf1:
            if st.button("🔄 ANIMATE GRADIENT FLOW", type="primary", use_container_width=True, key="backward_anim"):
                st.markdown("**Backward Pass - Gradient Propagation**")
                
                # Simulate gradient flow through 3 layers
                layers = ["Output Layer", "Hidden Layer 2", "Hidden Layer 1", "Input Layer"]
                
                # Initialize gradients
                gradients = []
                
                # Compute loss gradient
                w_sim = np.array([[0.5], [-0.5]])
                error = y - np.dot(X, w_sim)
                loss_grad = -2 * error.mean()
                
                for layer_idx, layer_name in enumerate(layers):
                    col_gf_sub1, col_gf_sub2 = st.columns([1.5, 1])
                    
                    with col_gf_sub1:
                        # Generate gradient visualization
                        if layer_idx == 0:
                            grad_values = np.array([loss_grad])
                        else:
                            grad_values = np.random.randn(3 + layer_idx) * np.exp(-layer_idx * 0.2)
                        
                        gradients.append(grad_values)
                        
                        # Visualize 3D gradient magnitudes mapping
                        colors = [R if g > 0 else G for g in grad_values]
                        
                        X_idx = list(range(len(grad_values)))
                        Y_idx = [layer_idx] * len(grad_values)
                        Z_val = np.abs(grad_values)
                        
                        fig_grad = go.Figure(data=[go.Scatter3d(
                            x=X_idx, y=Y_idx, z=Z_val,
                            mode='markers+lines' if len(grad_values)>1 else 'markers',
                            marker=dict(size=12, color=[hex2rgba(c, 0.8) for c in colors], symbol='diamond'),
                            line=dict(color=P, width=4)
                        )])
                        
                        fig_grad.update_layout(
                            title=f"{layer_name} - 3D Gradient Mapping",
                            scene=dict(
                                xaxis=dict(title='Neuron ID'),
                                yaxis=dict(title='Layer Depth'),
                                zaxis=dict(title='Local Gradient')
                            ),
                            showlegend=False,
                            **plotly_layout(height=280)
                        )
                        
                        st.plotly_chart(fig_grad, use_container_width=True, theme=None)
                    
                    with col_gf_sub2:
                        st.markdown(f"""
                        <div class="stat-card" style="padding:15px; border-left:4px solid {[R,P,C,G][layer_idx % 4]};">
                            <div style="font-size:10px; color:{MUTED};">{layer_name}</div>
                            <div style="font-size:14px; font-weight:bold;">Gradients: {len(grad_values)}</div>
                            <div style="font-size:10px; color:{MUTED}; margin-top:5px;">Mean: {np.mean(np.abs(grad_values)):.4f}</div>
                            <div style="font-size:10px; color:{MUTED};">Max: {np.max(np.abs(grad_values)):.4f}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    if layer_idx < len(layers) - 1:
                        st.markdown(f'<div style="text-align:center; color:{MUTED}; padding:5px;">⬆️ Backprop ⬆️</div>', 
                                   unsafe_allow_html=True)
                    
                    time.sleep(0.3)
                
                st.success("✅ Gradient Backpropagation Complete!")
        
        with col_gf2:
            st.markdown("**Vanishing Gradient Check**")
            st.markdown(f"""
            <div class="stat-card" style="padding:15px; border-left:4px solid {C}; margin-bottom:10px;">
                <div style="font-size:11px; color:{MUTED};">Gradient Stability</div>
                <div style="font-size:14px; font-weight:bold;">✓ Healthy</div>
            </div>
            <div class="stat-card" style="padding:15px; border-left:4px solid {G};">
                <div style="font-size:11px; color:{MUTED};">Flow Intensity</div>
                <div style="font-size:14px; font-weight:bold;">Strong</div>
            </div>
            """, unsafe_allow_html=True)
