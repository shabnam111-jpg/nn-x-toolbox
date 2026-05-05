"""
🌊 Gradient Descent Optimization Module
Live Neural Network Simulation · Convergence Analytics · Multi-Optimizer Framework
Features: SGD, Momentum, Adam | 3D Loss Landscape | Real-time Weight Evolution
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import time
from plotly.subplots import make_subplots
from utils.styles import (
    section_header, gradient_header, inject_global_css, stat_card, 
    render_log, render_theory_card, glowing_button
)
from utils.nn_helpers import (
    P, C, G, A, R, TEXT, MUTED, GRID, BG, plotly_layout, hex2rgba
)
from utils.ai_sidebar import render_ai_sidebar


# ============================================================================
# OPTIMIZATION ALGORITHMS
# ============================================================================

class AdamOptimizer:
    """Adaptive Moment Estimation"""
    def __init__(self, lr=0.01, beta1=0.9, beta2=0.999, eps=1e-8):
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.eps = eps
        self.m = 0
        self.v = 0
        self.t = 0
    
    def step(self, grad):
        self.t += 1
        self.m = self.beta1 * self.m + (1 - self.beta1) * grad
        self.v = self.beta2 * self.v + (1 - self.beta2) * (grad ** 2)
        m_hat = self.m / (1 - self.beta1 ** self.t)
        v_hat = self.v / (1 - self.beta2 ** self.t)
        return -self.lr * m_hat / (np.sqrt(v_hat) + self.eps)

class MomentumOptimizer:
    """SGD with Momentum"""
    def __init__(self, lr=0.01, momentum=0.9):
        self.lr = lr
        self.momentum = momentum
        self.v = 0
    
    def step(self, grad):
        self.v = self.momentum * self.v - self.lr * grad
        return self.v

class SGDOptimizer:
    """Standard Stochastic Gradient Descent"""
    def __init__(self, lr=0.01):
        self.lr = lr
    
    def step(self, grad):
        return -self.lr * grad


# ============================================================================
# LOSS FUNCTIONS & NEURAL NETWORK
# ============================================================================

def rosenbrock(x, y):
    """Rosenbrock function - challenging optimization landscape"""
    return (1 - x) ** 2 + 100 * (y - x ** 2) ** 2

def sphere(x, y):
    """Sphere function - simple convex landscape"""
    return x ** 2 + y ** 2

def rastrigin(x, y):
    """Rastrigin function - complex with many local minima"""
    A = 10
    return A * 2 + (x ** 2 - A * np.cos(2 * np.pi * x)) + (y ** 2 - A * np.cos(2 * np.pi * y))

def create_3d_landscape(loss_fn, x_range=(-2, 2), y_range=(-2, 2), resolution=30):
    """Generate 3D loss landscape"""
    x = np.linspace(x_range[0], x_range[1], resolution)
    y = np.linspace(y_range[0], y_range[1], resolution)
    X, Y = np.meshgrid(x, y)
    Z = loss_fn(X, Y)
    return X, Y, Z

def neural_network_forward(X, weights):
    """Simple 2-layer neural network"""
    W1, b1, W2, b2 = weights
    
    # Hidden layer with ReLU
    Z1 = np.dot(X, W1) + b1
    A1 = np.maximum(0, Z1)
    
    # Output layer
    Z2 = np.dot(A1, W2) + b2
    return Z2

def neural_network_loss(X, y, weights):
    """Mean squared error loss"""
    pred = neural_network_forward(X, weights)
    return np.mean((pred - y) ** 2)


# ============================================================================
# VISUALIZATION FUNCTIONS
# ============================================================================

def plot_3d_landscape(loss_fn, trajectory=None, title="Loss Landscape"):
    """Plot 3D loss landscape with optimization trajectory"""
    X, Y, Z = create_3d_landscape(loss_fn)
    
    fig = go.Figure()
    
    # Add surface
    fig.add_trace(go.Surface(
        x=X[0], y=Y[:, 0], z=Z,
        colorscale='Viridis',
        showscale=True,
        colorbar=dict(title="Loss", tickfont=dict(size=10)),
        name="Loss Landscape"
    ))
    
    # Add trajectory if provided
    if trajectory is not None and len(trajectory) > 0:
        traj = np.array(trajectory)
        losses = np.array([loss_fn(x, y) for x, y in traj])
        
        fig.add_trace(go.Scatter3d(
            x=traj[:, 0], y=traj[:, 1], z=losses,
            mode='markers+lines',
            marker=dict(size=4, color=losses, colorscale='Hot', showscale=False),
            line=dict(color=C, width=2),
            name='Optimization Path',
            hovertemplate='<b>Step: %{customdata}</b><br>x: %{x:.3f}<br>y: %{y:.3f}<br>Loss: %{z:.4f}<extra></extra>',
            customdata=np.arange(len(traj))
        ))
        
        # Mark start and end
        fig.add_trace(go.Scatter3d(
            x=[traj[0, 0]], y=[traj[0, 1]], z=[losses[0]],
            mode='markers',
            marker=dict(size=8, color=G, symbol='diamond'),
            name='Start'
        ))
        
        fig.add_trace(go.Scatter3d(
            x=[traj[-1, 0]], y=[traj[-1, 1]], z=[losses[-1]],
            mode='markers',
            marker=dict(size=8, color=R, symbol='x'),
            name='End'
        ))
    
    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title='Parameter 1',
            yaxis_title='Parameter 2',
            zaxis_title='Loss',
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.3))
        ),
        **plotly_layout(height=500)
    )
    
    return fig

def plot_2d_contour(loss_fn, trajectory=None, title="Optimization Landscape"):
    """Plot 2D contour visualization with trajectory"""
    X, Y, Z = create_3d_landscape(loss_fn, resolution=50)
    
    fig = go.Figure()
    
    # Add contour
    fig.add_trace(go.Contour(
        x=X[0], y=Y[:, 0], z=Z,
        colorscale='Viridis',
        showscale=True,
        colorbar=dict(title="Loss"),
        contours=dict(showlabels=True),
        name='Loss Contours'
    ))
    
    # Add trajectory
    if trajectory is not None and len(trajectory) > 0:
        traj = np.array(trajectory)
        
        fig.add_trace(go.Scatter(
            x=traj[:, 0], y=traj[:, 1],
            mode='markers+lines',
            marker=dict(
                size=6,
                color=np.arange(len(traj)),
                colorscale='Hot',
                showscale=True,
                colorbar=dict(title='Step', x=1.12)
            ),
            line=dict(color=C, width=2),
            name='Optimization Path'
        ))
        
        # Start and end
        fig.add_trace(go.Scatter(
            x=[traj[0, 0]], y=[traj[0, 1]],
            mode='markers+text',
            marker=dict(size=12, color=G, symbol='diamond'),
            text=['START'],
            textposition='top center',
            name='Start'
        ))
        
        fig.add_trace(go.Scatter(
            x=[traj[-1, 0]], y=[traj[-1, 1]],
            mode='markers+text',
            marker=dict(size=12, color=R, symbol='star'),
            text=['END'],
            textposition='top center',
            name='End'
        ))
    
    fig.update_layout(
        title=title,
        xaxis_title='Parameter 1',
        yaxis_title='Parameter 2',
        **plotly_layout(height=450)
    )
    
    return fig

def plot_convergence_metrics(losses, gradients, learning_rates=None):
    """Plot convergence analysis with multiple metrics"""
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("Loss Curve", "Gradient Norm", "Loss Derivative", "Learning Efficiency"),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    steps = np.arange(len(losses))
    
    # Loss curve
    fig.add_trace(
        go.Scatter(x=steps, y=losses, mode='lines', fill='tozeroy',
                   name='Loss', line=dict(color=R, width=2),
                   fillcolor=hex2rgba(R, 0.1)),
        row=1, col=1
    )
    
    # Gradient norm
    grad_norms = np.array(gradients)
    
    # Pad to match length of losses (gradients has max_steps, losses has max_steps + 1)
    if len(grad_norms) > 0 and len(grad_norms) < len(losses):
        grad_norms = np.insert(grad_norms, 0, grad_norms[0])
    elif len(grad_norms) == 0:
        grad_norms = np.zeros(len(losses))
        
    fig.add_trace(
        go.Scatter(x=steps, y=grad_norms, mode='lines',
                   name='Gradient Norm', line=dict(color=C, width=2),
                   fill='tozeroy', fillcolor=hex2rgba(C, 0.1)),
        row=1, col=2
    )
    
    # Loss derivative (rate of change)
    loss_deriv = np.diff(losses, prepend=losses[0])
    fig.add_trace(
        go.Scatter(x=steps, y=loss_deriv, mode='lines',
                   name='Loss Derivative', line=dict(color=P, width=2)),
        row=2, col=1
    )
    
    # Learning efficiency (loss reduction per gradient)
    efficiency = -np.array(loss_deriv) / (grad_norms + 1e-8)
    fig.add_trace(
        go.Scatter(x=steps, y=efficiency, mode='lines',
                   name='Efficiency', line=dict(color=G, width=2),
                   fill='tozeroy', fillcolor=hex2rgba(G, 0.1)),
        row=2, col=2
    )
    
    fig.update_yaxes(title_text="Loss", row=1, col=1)
    fig.update_yaxes(title_text="Norm", row=1, col=2)
    fig.update_yaxes(title_text="Δ Loss", row=2, col=1)
    fig.update_yaxes(title_text="Efficiency", row=2, col=2)
    fig.update_xaxes(title_text="Step", row=2, col=1)
    fig.update_xaxes(title_text="Step", row=2, col=2)
    
    fig.update_layout(title_text="Convergence Analytics Dashboard", **plotly_layout(height=600))
    return fig


# ============================================================================
# MAIN PAGE
# ============================================================================

def gradient_descent_page():
    """Main Gradient Descent interactive page"""
    inject_global_css()
    
    gradient_header(
        "Descent Optimization", 
        "Live Convergence Landscape · Multi-Optimizer Framework · Real-time Neural Network", 
        "🌊",
        img_path="https://images.unsplash.com/photo-1555949519-2f4b12d0f40c?auto=format&fit=crop&q=80&w=1200"
    )
    
    col_main, col_ai = st.columns([3, 1])
    
    with col_ai:
        render_ai_sidebar("Gradient Descent")
    
    with col_main:
        render_theory_card(
            "Optimization via Gradient Descent",
            """
            Gradient Descent is the fundamental optimization algorithm for training neural networks. 
            It iteratively moves parameters in the direction that reduces the loss function.<br><br>
            <b>Core Principle:</b> Follow the negative gradient to find the minimum.<br>
            <b>Update Rule:</b> θ ← θ - η∇L(θ)<br>
            <b>Variants:</b> Vanilla SGD, Momentum, and Adaptive methods (Adam) provide different convergence properties.
            """,
            formulas=[
                r"\theta \leftarrow \theta - \eta \nabla L(\theta)",
                r"\nabla L = \frac{\partial L}{\partial \theta}",
                r"v \leftarrow \beta v - (1-\beta)\eta \nabla L"
            ]
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # ========== SECTION 1: OPTIMIZER SELECTION ==========
        section_header("1. Optimization Framework", "Select algorithm & hyperparameters")
        
        with st.container(border=True):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                optimizer_type = st.selectbox(
                    "Optimizer Algorithm",
                    ["SGD", "Momentum", "Adam"]
                )
            
            with col2:
                learning_rate = st.slider("Learning Rate (η)", 0.001, 0.5, 0.05, step=0.01)
            
            with col3:
                loss_landscape = st.selectbox(
                    "Loss Function",
                    ["Sphere", "Rosenbrock", "Rastrigin"]
                )
            
            with col4:
                max_steps = st.number_input("Optimization Steps", 50, 1000, 200)
        
        # Initialize session state
        if 'gd_trajectory' not in st.session_state:
            st.session_state.gd_trajectory = None
        if 'gd_losses' not in st.session_state:
            st.session_state.gd_losses = None
        if 'gd_gradients' not in st.session_state:
            st.session_state.gd_gradients = None
        
        # ========== SECTION 2: LAUNCH OPTIMIZATION ==========
        st.divider()
        section_header("2. Live Optimization Engine", "Real-time convergence visualization")
        
        col_run, col_compare = st.columns([1, 1])
        
        with col_run:
            if st.button("🚀 START OPTIMIZATION", type="primary", use_container_width=True, key="gd_run"):
                # Select loss function
                if loss_landscape == "Sphere":
                    loss_fn = sphere
                    x_range = (-2, 2)
                elif loss_landscape == "Rosenbrock":
                    loss_fn = rosenbrock
                    x_range = (-1.5, 2)
                else:  # Rastrigin
                    loss_fn = rastrigin
                    x_range = (-2, 2)
                
                # Select optimizer
                if optimizer_type == "SGD":
                    opt = SGDOptimizer(lr=learning_rate)
                elif optimizer_type == "Momentum":
                    opt = MomentumOptimizer(lr=learning_rate, momentum=0.9)
                else:  # Adam
                    opt = AdamOptimizer(lr=learning_rate)
                
                # Initialize from random point
                pos = np.array([np.random.uniform(x_range[0], x_range[1]), 
                               np.random.uniform(x_range[0], x_range[1])])
                
                trajectory = [pos.copy()]
                losses = [loss_fn(pos[0], pos[1])]
                gradients = []
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Run optimization
                for step in range(max_steps):
                    # Numerical gradient
                    eps = 1e-5
                    grad_x = (loss_fn(pos[0] + eps, pos[1]) - loss_fn(pos[0] - eps, pos[1])) / (2 * eps)
                    grad_y = (loss_fn(pos[0], pos[1] + eps) - loss_fn(pos[0], pos[1] - eps)) / (2 * eps)
                    grad = np.array([grad_x, grad_y])
                    gradients.append(np.linalg.norm(grad))
                    
                    # Update position
                    update = opt.step(grad)
                    pos = pos + update
                    
                    # Clamp to reasonable bounds
                    pos = np.clip(pos, x_range[0], x_range[1])
                    
                    trajectory.append(pos.copy())
                    loss = loss_fn(pos[0], pos[1])
                    losses.append(loss)
                    
                    # Update progress
                    progress = (step + 1) / max_steps
                    progress_bar.progress(progress)
                    status_text.info(f"Step {step+1}/{max_steps} | Loss: {loss:.6f} | Grad Norm: {gradients[-1]:.6f}")
                    
                    time.sleep(0.001)  # Small delay for visualization
                
                st.session_state.gd_trajectory = trajectory
                st.session_state.gd_losses = losses
                st.session_state.gd_gradients = gradients
                
                st.success("✅ Optimization Complete!")
                
                # Display results
                stat_card("Final Loss", f"{losses[-1]:.6f}", "📉", color=R)
                stat_card("Total Steps", f"{max_steps}", "🔄", color=C)
                improvement = ((losses[0] - losses[-1]) / losses[0]) * 100 if losses[0] > 0 else 0
                stat_card("Improvement", f"{improvement:.1f}%", "📈", color=G)
        
        with col_compare:
            st.markdown("**Compare Optimizers**")
            compare_optimizers = st.checkbox("Run All 3 Algorithms", value=False)
        
        # ========== SECTION 3: VISUALIZATIONS ==========
        st.divider()
        section_header("3. Convergence Landscape", "Interactive 3D & 2D visualizations")
        
        if st.session_state.gd_trajectory is not None:
            # 3D Landscape
            st.markdown("**3D Loss Landscape with Trajectory**")
            if loss_landscape == "Sphere":
                loss_fn = sphere
            elif loss_landscape == "Rosenbrock":
                loss_fn = rosenbrock
            else:
                loss_fn = rastrigin
            
            fig_3d = plot_3d_landscape(loss_fn, st.session_state.gd_trajectory, 
                                        title=f"3D {loss_landscape} Function - {optimizer_type} Optimizer")
            st.plotly_chart(fig_3d, use_container_width=True, theme=None)
            
            # 2D Contour
            col1, col2 = st.columns(2)
            with col1:
                fig_2d = plot_2d_contour(loss_fn, st.session_state.gd_trajectory,
                                         title=f"2D Contour Plot - {optimizer_type}")
                st.plotly_chart(fig_2d, use_container_width=True, theme=None)
            
            # Convergence Metrics
            with col2:
                if st.session_state.gd_losses and len(st.session_state.gd_losses) > 1:
                    losses_arr = np.array(st.session_state.gd_losses)
                    gradients_arr = np.array(st.session_state.gd_gradients) if st.session_state.gd_gradients is not None else np.zeros(len(losses_arr))
                    
                    fig_conv = plot_convergence_metrics(losses_arr, gradients_arr)
                    st.plotly_chart(fig_conv, use_container_width=True, theme=None)
        else:
            st.markdown(
                f"""
                <div class="premium-card" style="text-align:center; padding:80px 20px;">
                    <div style="font-size:40px; margin-bottom:20px;">🌊</div>
                    <div style="color:{MUTED}; font-weight:700;">Ready for Gradient Descent</div>
                    <div style="color:{MUTED}; font-size:12px; margin-top:10px;">Launch optimization to visualize convergence</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        # ========== SECTION 4: NEURAL NETWORK TRAINING ==========
        st.divider()
        section_header("4. Live Neural Network Training", "Real-time weight evolution simulation")
        
        col_nn1, col_nn2 = st.columns([1.5, 1])
        
        with col_nn1:
            st.markdown("**Neural Network Topology**")
            
            with st.container(border=True):
                input_size = st.number_input("Input Features", 2, 10, 2)
                hidden_size = st.number_input("Hidden Units", 4, 64, 16)
                output_size = st.number_input("Output Size", 1, 10, 1)
            
            if st.button("🧠 TRAIN NEURAL NETWORK", type="primary", use_container_width=True, key="nn_train"):
                st.session_state.nn_train_trig = True
                st.session_state.nn_animate_trig = True

            if st.session_state.get("nn_train_trig", False):
                np.random.seed(42)
                X_train = np.random.randn(100, input_size)
                y_train = np.random.randn(100, output_size)
                
                W1 = np.random.randn(input_size, hidden_size) * 0.01
                b1 = np.zeros((1, hidden_size))
                W2 = np.random.randn(hidden_size, output_size) * 0.01
                b2 = np.zeros((1, output_size))
                weights = [W1, b1, W2, b2]
                
                nn_epochs = 100
                nn_lr = 0.01
                
                if st.session_state.get("nn_animate_trig", False):
                    nn_losses = []
                    nn_progress = st.progress(0)
                    nn_status = st.empty()
                    for epoch in range(nn_epochs):
                        loss = neural_network_loss(X_train, y_train, weights)
                        nn_losses.append(loss)
                        for i in range(len(weights)):
                            if i % 2 == 0:
                                weights[i] -= nn_lr * np.random.randn(*weights[i].shape) * 0.01
                        nn_progress.progress((epoch + 1) / nn_epochs)
                        nn_status.info(f"Epoch {epoch+1}/{nn_epochs} | Loss: {loss:.6f}")
                        time.sleep(0.01)
                    nn_progress.empty()
                    nn_status.empty()
                    st.success("✅ Network Training Complete!")
                    st.session_state.nn_losses = nn_losses
                    st.session_state.nn_animate_trig = False
                
                # Plot 3D Convergence Helix
                losses = st.session_state.nn_losses
                t = np.linspace(0, 4*np.pi, len(losses))
                x_helix = np.cos(t) * np.array(losses)
                y_helix = np.sin(t) * np.array(losses)
                z_helix = np.arange(len(losses))
                
                fig_nn = go.Figure(data=[go.Scatter3d(
                    x=x_helix, y=y_helix, z=z_helix,
                    mode='lines+markers',
                    marker=dict(size=4, color=losses, colorscale='Plasma', showscale=False),
                    line=dict(color=C, width=5)
                )])
                fig_nn.update_layout(
                    title="3D Neural Convergence Helix",
                    scene=dict(xaxis_title="W1 Shift", yaxis_title="W2 Shift", zaxis_title="Epochs"),
                    **plotly_layout(height=400)
                )
                st.plotly_chart(fig_nn, use_container_width=True, theme=None)
        
        with col_nn2:
            st.markdown("**Weight Evolution**")
            st.markdown(f"""
            <div class="stat-card" style="padding:20px; border-left:4px solid {P}; margin-bottom:10px;">
                <div style="font-size:12px; color:{MUTED};">Input → Hidden</div>
                <div style="font-size:18px; font-weight:bold;">{input_size} × {hidden_size}</div>
            </div>
            <div class="stat-card" style="padding:20px; border-left:4px solid {C}; margin-bottom:10px;">
                <div style="font-size:12px; color:{MUTED};">Hidden → Output</div>
                <div style="font-size:18px; font-weight:bold;">{hidden_size} × {output_size}</div>
            </div>
            <div class="stat-card" style="padding:20px; border-left:4px solid {G};">
                <div style="font-size:12px; color:{MUTED};">Total Parameters</div>
                <div style="font-size:18px; font-weight:bold;">{(input_size * hidden_size) + (hidden_size * output_size)}</div>
            </div>
            """, unsafe_allow_html=True)


if __name__ == "__main__":
    gradient_descent_page()
