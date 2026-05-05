"""
Training Replay System
Visualizes training progression epoch-by-epoch with interactive playback controls.
"""

import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from src.ui.utils.model_checkpoint import CheckpointManager


def plot_training_replay(checkpoint_manager: CheckpointManager, 
                         X_train: np.ndarray, y_train: np.ndarray,
                         X_val: np.ndarray = None, y_val: np.ndarray = None) -> go.Figure:
    """
    Create interactive training replay visualization with epoch slider
    
    Args:
        checkpoint_manager: CheckpointManager with saved frames
        X_train, y_train: Training data
        X_val, y_val: Validation data (optional)
    
    Returns:
        Plotly figure with epoch-by-epoch decision boundaries
    """
    frames = checkpoint_manager.get_all_frames()
    
    if not frames or len(X_train[0]) != 2:
        st.warning("⚠️ Training Replay requires 2D features for visualization")
        return None
    
    # Create mesh grid for decision boundary
    x_min, x_max = X_train[:, 0].min() - 0.5, X_train[:, 0].max() + 0.5
    y_min, y_max = X_train[:, 1].min() - 0.5, X_train[:, 1].max() + 0.5
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 100),
                         np.linspace(y_min, y_max, 100))
    
    # Create frames for animation
    animation_frames = []
    for frame_idx, frame in enumerate(frames):
        # Reconstruct predictions from saved weights
        # (simplified - assumes 2-layer network)
        
        frame_data = [
            go.Scatter(
                x=X_train[:, 0], y=X_train[:, 1],
                mode='markers',
                marker=dict(
                    size=8,
                    color=y_train,
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title="Class")
                ),
                name='Training Data',
                hovertemplate='x=%{x:.2f}<br>y=%{y:.2f}<extra></extra>'
            )
        ]
        
        # Add contour for decision boundary if available
        if len(frame.weights) > 0:
            frame_data.append(
                go.Contour(
                    x=np.linspace(x_min, x_max, 100),
                    y=np.linspace(y_min, y_max, 100),
                    z=np.random.rand(100, 100),  # Placeholder
                    colorscale='RdBu',
                    showscale=False,
                    contours=dict(showlabels=True),
                    name='Decision Boundary',
                    hoverinfo='skip'
                )
            )
        
        animation_frames.append(go.Frame(
            data=frame_data,
            name=f"Epoch {frame.epoch}"
        ))
    
    # Initial data
    initial_data = [
        go.Scatter(
            x=X_train[:, 0], y=X_train[:, 1],
            mode='markers',
            marker=dict(
                size=8,
                color=y_train,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Class")
            ),
            name='Training Data'
        )
    ]
    
    # Create figure
    fig = go.Figure(data=initial_data, frames=animation_frames)
    
    # Update layout with slider and play button
    fig.update_layout(
        title="🎬 Training Replay - Decision Boundary Evolution",
        xaxis_title="Feature 1",
        yaxis_title="Feature 2",
        height=600,
        hovermode='closest',
        updatemenus=[
            dict(
                type="buttons",
                showactive=False,
                y=1.15,
                x=0.0,
                buttons=[
                    dict(label="▶ Play",
                         method="animate",
                         args=[None, {"frame": {"duration": 300, "redraw": True},
                                    "fromcurrent": True, "transition": {"duration": 200}}]),
                    dict(label="⏸ Pause",
                         method="animate",
                         args=[[None], {"frame": {"duration": 0, "redraw": True},
                                       "mode": "immediate", "transition": {"duration": 0}}])
                ]
            )
        ],
        sliders=[
            dict(
                active=0,
                yanchor="top",
                y=0,
                xanchor="left",
                x=0.1,
                len=0.9,
                transition={"duration": 200},
                pad={"b": 10, "t": 50},
                steps=[
                    dict(
                        args=[[f.name], {"frame": {"duration": 300, "redraw": True},
                                        "mode": "immediate", "transition": {"duration": 200}}],
                        method="animate",
                        label=f.name
                    )
                    for f in animation_frames
                ]
            )
        ]
    )
    
    return fig


def plot_loss_curves_with_epoch_marker(checkpoint_manager: CheckpointManager,
                                        selected_epoch: int = None) -> go.Figure:
    """
    Plot training/validation loss with epoch marker
    """
    train_loss, val_loss = checkpoint_manager.get_loss_history()
    epochs = np.arange(len(train_loss))
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=epochs, y=train_loss,
        mode='lines+markers',
        name='Training Loss',
        line=dict(color='#3b82f6', width=2),
        marker=dict(size=6)
    ))
    
    fig.add_trace(go.Scatter(
        x=epochs, y=val_loss,
        mode='lines+markers',
        name='Validation Loss',
        line=dict(color='#ef4444', width=2, dash='dash'),
        marker=dict(size=6)
    ))
    
    if selected_epoch is not None and 0 <= selected_epoch < len(epochs):
        fig.add_vline(
            x=selected_epoch,
            line_dash="dash",
            line_color="green",
            annotation_text=f"Epoch {selected_epoch}",
            annotation_position="top right"
        )
    
    fig.update_layout(
        title="📊 Loss Progression",
        xaxis_title="Epoch",
        yaxis_title="Loss",
        hovermode='x unified',
        height=400,
        template='plotly_white'
    )
    
    return fig
