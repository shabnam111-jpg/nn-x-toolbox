"""
Loss Landscape Visualization
3D interactive visualization of loss surface around trained weights.
"""

import streamlit as st
import numpy as np
import plotly.graph_objects as go


def generate_loss_landscape(model_fn, X, y, weights_1d, loss_range=0.5, 
                           resolution=50):
    """
    Generate 3D loss landscape by perturbing weights
    
    Args:
        model_fn: Function that takes weights and returns predictions
        X, y: Training data
        weights_1d: Flattened weight vector
        loss_range: Range of perturbation (e.g., ±0.5)
        resolution: Grid resolution
    
    Returns:
        w1_grid, w2_grid, loss_grid
    """
    # Create random orthogonal directions for weight perturbation
    np.random.seed(42)
    direction1 = np.random.randn(*weights_1d.shape)
    direction1 /= np.linalg.norm(direction1)
    
    direction2 = np.random.randn(*weights_1d.shape)
    direction2 -= np.dot(direction2, direction1) * direction1
    direction2 /= np.linalg.norm(direction2)
    
    # Create grid
    alphas = np.linspace(-loss_range, loss_range, resolution)
    betas = np.linspace(-loss_range, loss_range, resolution)
    
    w1_grid, w2_grid = np.meshgrid(alphas, betas)
    loss_grid = np.zeros_like(w1_grid)
    
    # Compute loss at each grid point
    for i in range(resolution):
        for j in range(resolution):
            alpha = w1_grid[i, j]
            beta = w2_grid[i, j]
            
            # Perturb weights
            perturbed_weights = (weights_1d + 
                               alpha * direction1 + 
                               beta * direction2)
            
            # Compute loss (simplified - assumes binary cross-entropy)
            try:
                preds = model_fn(perturbed_weights)
                preds = np.clip(preds, 1e-10, 1 - 1e-10)
                loss = -np.mean(y * np.log(preds) + (1 - y) * np.log(1 - preds))
                loss_grid[i, j] = loss
            except:
                loss_grid[i, j] = np.nan
    
    return w1_grid, w2_grid, loss_grid


def plot_3d_loss_landscape(w1_grid, w2_grid, loss_grid, 
                          title="Loss Landscape") -> go.Figure:
    """
    Create 3D surface plot of loss landscape
    """
    fig = go.Figure(data=[go.Surface(
        x=w1_grid,
        y=w2_grid,
        z=loss_grid,
        colorscale='Viridis',
        colorbar=dict(title="Loss"),
        hovertemplate='α: %{x:.3f}<br>β: %{y:.3f}<br>Loss: %{z:.4f}<extra></extra>'
    )])
    
    fig.update_layout(
        title=f"🗻 {title}",
        scene=dict(
            xaxis_title="Direction α",
            yaxis_title="Direction β",
            zaxis_title="Loss",
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.3)
            )
        ),
        height=600,
        template='plotly_white'
    )
    
    return fig


def plot_loss_landscape_contour(w1_grid, w2_grid, loss_grid,
                               title="Loss Landscape Contours") -> go.Figure:
    """
    Create 2D contour plot of loss landscape (top-down view)
    """
    fig = go.Figure(data=[go.Contour(
        x=w1_grid[0, :],
        y=w2_grid[:, 0],
        z=loss_grid,
        colorscale='Viridis',
        colorbar=dict(title="Loss"),
        contours=dict(
            showlabels=True,
            labelfont=dict(size=10)
        ),
        hovertemplate='α: %{x:.3f}<br>β: %{y:.3f}<br>Loss: %{z:.4f}<extra></extra>'
    )])
    
    # Add center point (trained weights)
    fig.add_trace(go.Scatter(
        x=[0], y=[0],
        mode='markers',
        marker=dict(size=12, color='red', symbol='star'),
        name='Trained Weights',
        hovertemplate='Trained Weights<extra></extra>'
    ))
    
    fig.update_layout(
        title=f"🗺️ {title}",
        xaxis_title="Direction α",
        yaxis_title="Direction β",
        height=500,
        template='plotly_white',
        hovermode='closest'
    )
    
    return fig


def analyze_loss_landscape(loss_grid) -> dict:
    """
    Analyze properties of loss landscape
    """
    # Remove NaN values
    valid_losses = loss_grid[~np.isnan(loss_grid)]
    
    if len(valid_losses) == 0:
        return {}
    
    analysis = {
        'min_loss': float(np.min(valid_losses)),
        'max_loss': float(np.max(valid_losses)),
        'mean_loss': float(np.mean(valid_losses)),
        'std_loss': float(np.std(valid_losses)),
        'loss_range': float(np.max(valid_losses) - np.min(valid_losses)),
        'landscape_smoothness': float(np.std(np.diff(np.sort(valid_losses)))),
    }
    
    return analysis
