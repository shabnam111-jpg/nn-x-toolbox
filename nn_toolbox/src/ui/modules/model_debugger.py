"""
Model Debugger
Step-by-step visualization of forward and backward passes with neuron values and gradients.
"""

import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class NeuronDebugger:
    """Debug neural network layer-by-layer"""
    
    def __init__(self):
        self.layer_activations = {}
        self.layer_gradients = {}
        self.weight_matrices = {}
    
    def record_forward_pass(self, layer_name: str, input_data: np.ndarray,
                           output_data: np.ndarray, weights: np.ndarray):
        """Record forward pass activation"""
        self.layer_activations[layer_name] = {
            'input': input_data,
            'output': output_data,
            'weights': weights
        }
    
    def record_backward_pass(self, layer_name: str, gradients: np.ndarray,
                            input_grad: np.ndarray):
        """Record backward pass gradients"""
        self.layer_gradients[layer_name] = {
            'weight_grad': gradients,
            'input_grad': input_grad
        }
    
    def get_layer_activations(self, layer_name: str) -> dict:
        """Get activation data for a layer"""
        return self.layer_activations.get(layer_name, {})
    
    def get_layer_gradients(self, layer_name: str) -> dict:
        """Get gradient data for a layer"""
        return self.layer_gradients.get(layer_name, {})


def plot_neuron_activations(layer_name: str, activations: np.ndarray,
                           title: str = None) -> go.Figure:
    """
    Visualize neuron activation values
    """
    if activations.ndim == 1:
        # Single sample
        neurons = np.arange(len(activations))
        
        fig = go.Figure(data=[go.Bar(
            x=neurons,
            y=activations,
            marker=dict(
                color=activations,
                colorscale='RdBu',
                showscale=True,
                colorbar=dict(title="Activation")
            ),
            text=[f"{v:.3f}" for v in activations],
            textposition="auto",
            hovertemplate='Neuron %{x}<br>Activation: %{y:.4f}<extra></extra>'
        )])
    else:
        # Multiple samples
        fig = go.Figure(data=[go.Heatmap(
            z=activations,
            colorscale='RdBu',
            colorbar=dict(title="Activation"),
            hovertemplate='Sample: %{x}<br>Neuron: %{y}<br>Activation: %{z:.4f}<extra></extra>'
        )])
        fig.update_layout(
            xaxis_title="Sample",
            yaxis_title="Neuron",
        )
    
    fig.update_layout(
        title=title or f"🧠 Layer '{layer_name}' Activations",
        height=400,
        template='plotly_white',
        showlegend=False
    )
    
    return fig


def plot_neuron_gradients(layer_name: str, gradients: np.ndarray,
                         title: str = None) -> go.Figure:
    """
    Visualize neuron gradient values
    """
    if gradients.ndim == 1:
        neurons = np.arange(len(gradients))
        
        fig = go.Figure(data=[go.Bar(
            x=neurons,
            y=np.abs(gradients),
            marker=dict(
                color=np.sign(gradients),
                colorscale='RdBu',
                showscale=True,
                colorbar=dict(title="Sign")
            ),
            text=[f"{v:.2e}" for v in gradients],
            textposition="auto",
            hovertemplate='Neuron %{x}<br>Gradient: %{customdata}<extra></extra>',
            customdata=gradients
        )])
    else:
        fig = go.Figure(data=[go.Heatmap(
            z=gradients,
            colorscale='RdBu',
            colorbar=dict(title="Gradient Magnitude"),
            hovertemplate='In: %{x}<br>Out: %{y}<br>Gradient: %{z:.4f}<extra></extra>'
        )])
        fig.update_layout(
            xaxis_title="Input Neuron",
            yaxis_title="Output Neuron",
        )
    
    fig.update_layout(
        title=title or f"📊 Layer '{layer_name}' Gradients",
        height=400,
        template='plotly_white',
        showlegend=False
    )
    
    return fig


def plot_weight_impact(weights: np.ndarray, layer_name: str = None) -> go.Figure:
    """
    Visualize weight matrix with impact colors
    """
    fig = go.Figure(data=[go.Heatmap(
        z=weights,
        colorscale='RdBu_r',
        colorbar=dict(title="Weight Value"),
        hovertemplate='To Neuron: %{x}<br>From Neuron: %{y}<br>Weight: %{z:.4f}<extra></extra>'
    )])
    
    fig.update_layout(
        title=f"🔗 Weight Matrix - {layer_name or 'Layer'}",
        xaxis_title="Output Neuron",
        yaxis_title="Input Neuron",
        height=500,
        template='plotly_white'
    )
    
    return fig


def create_debug_step_comparison(layer_name: str, 
                                activations: np.ndarray,
                                gradients: np.ndarray = None) -> go.Figure:
    """
    Create side-by-side comparison of activations and gradients
    """
    if gradients is None:
        return plot_neuron_activations(layer_name, activations)
    
    # Create subplots
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=(f"Forward Pass Activations", f"Backward Pass Gradients")
    )
    
    # Activations
    fig.add_trace(
        go.Bar(
            x=np.arange(len(activations)),
            y=activations,
            marker=dict(color='#3b82f6'),
            name="Activations",
            hovertemplate='Neuron %{x}<br>Value: %{y:.4f}<extra></extra>'
        ),
        row=1, col=1
    )
    
    # Gradients
    fig.add_trace(
        go.Bar(
            x=np.arange(len(gradients)),
            y=np.abs(gradients),
            marker=dict(color='#ef4444'),
            name="Gradients",
            hovertemplate='Neuron %{x}<br>Magnitude: %{y:.2e}<extra></extra>'
        ),
        row=1, col=2
    )
    
    fig.update_xaxes(title_text="Neuron", row=1, col=1)
    fig.update_xaxes(title_text="Neuron", row=1, col=2)
    fig.update_yaxes(title_text="Activation Value", row=1, col=1)
    fig.update_yaxes(title_text="Gradient Magnitude", row=1, col=2)
    
    fig.update_layout(
        title=f"🔍 Forward/Backward Inspection - {layer_name}",
        height=400,
        template='plotly_white',
        showlegend=True
    )
    
    return fig
