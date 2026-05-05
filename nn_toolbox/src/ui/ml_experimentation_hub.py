"""
ML Experimentation Hub - Phase 1
Next-Generation Neural Network Visualization & Analysis Platform
Features: Training Replay, Gradient Analysis, Loss Landscape, Model Debugger, Learning Rate Analysis
"""

import streamlit as st
import numpy as np
from typing import Tuple
import time
from dataclasses import dataclass

# Import feature modules
from src.ui.utils.model_checkpoint import CheckpointManager
from src.ui.utils.gradient_tracker import GradientTracker
from src.ui.modules.training_replay import plot_training_replay, plot_loss_curves_with_epoch_marker
from src.ui.modules.gradient_analyzer import (
    plot_gradient_magnitudes, 
    plot_gradient_flow_timeline,
    plot_gradient_health_heatmap,
    gradient_health_summary
)
from src.ui.modules.loss_landscape import (
    generate_loss_landscape,
    plot_3d_loss_landscape,
    plot_loss_landscape_contour,
    analyze_loss_landscape
)
from src.ui.modules.model_debugger import (
    NeuronDebugger,
    plot_neuron_activations,
    plot_neuron_gradients,
    create_debug_step_comparison
)
from src.ui.modules.learning_rate_optimizer import (
    plot_learning_rate_comparison,
    plot_learning_rate_stability,
    analyze_learning_rate_effects,
    plot_learning_curve_acceleration
)


# ============================================================================
# NEURAL NETWORK IMPLEMENTATION (NumPy-based)
# ============================================================================

class NeuralNetworkDebugger:
    """Enhanced neural network with debugging capabilities"""
    
    def __init__(self, input_size: int, hidden_sizes: list, output_size: int = 1):
        self.input_size = input_size
        self.hidden_sizes = hidden_sizes
        self.output_size = output_size
        self.layer_sizes = [input_size] + hidden_sizes + [output_size]
        self.n_layers = len(self.layer_sizes) - 1
        
        self.weights = {}
        self.biases = {}
        self.initialize_params()
        
        self.debugger = NeuronDebugger()
        self.checkpoint_manager = CheckpointManager()
        self.gradient_tracker = GradientTracker()
    
    def initialize_params(self):
        """He initialization"""
        for i in range(self.n_layers):
            layer_name = f"W{i+1}"
            fan_in = self.layer_sizes[i]
            fan_out = self.layer_sizes[i + 1]
            
            self.weights[layer_name] = np.random.randn(fan_in, fan_out) * np.sqrt(2 / fan_in)
            self.biases[layer_name] = np.zeros((1, fan_out))
    
    def relu(self, x):
        return np.maximum(0, x)
    
    def relu_derivative(self, x):
        return (x > 0).astype(float)
    
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))
    
    def forward(self, X, record_debug=False):
        """Forward pass with optional debug recording"""
        self.cache = {'A0': X}
        self.activations = {'A0': X}
        
        for i in range(self.n_layers - 1):
            layer_name = f"W{i+1}"
            Z = self.cache[f'A{i}'] @ self.weights[layer_name] + self.biases[layer_name]
            A = self.relu(Z)
            
            self.cache[f'Z{i+1}'] = Z
            self.cache[f'A{i+1}'] = A
            self.activations[f'A{i+1}'] = A
            
            if record_debug:
                self.debugger.record_forward_pass(layer_name, self.cache[f'A{i}'], A, 
                                                 self.weights[layer_name])
        
        # Output layer (sigmoid for binary)
        final_layer = f"W{self.n_layers}"
        Z_out = self.cache[f'A{self.n_layers-1}'] @ self.weights[final_layer] + self.biases[final_layer]
        A_out = self.sigmoid(Z_out)
        
        self.cache[f'Z{self.n_layers}'] = Z_out
        self.cache[f'A{self.n_layers}'] = A_out
        
        return A_out
    
    def backward(self, Y, learning_rate, record_debug=False):
        """Backward pass"""
        m = Y.shape[0]
        dA = self.cache[f'A{self.n_layers}'] - Y
        
        gradients = {}
        
        for i in reversed(range(1, self.n_layers + 1)):
            layer_name = f"W{i}"
            A_prev = self.cache[f'A{i-1}']
            
            dW = (A_prev.T @ dA) / m
            db = np.sum(dA, axis=0, keepdims=True) / m
            
            gradients[layer_name] = dW
            gradients[f'b{i}'] = db
            
            if i > 1:
                dA = (dA @ self.weights[layer_name].T) * self.relu_derivative(self.cache[f'Z{i}'])
            
            if record_debug:
                self.debugger.record_backward_pass(layer_name, dW, dA)
        
        # Update weights
        for i in range(1, self.n_layers + 1):
            layer_name = f"W{i}"
            self.weights[layer_name] -= learning_rate * gradients[layer_name]
            self.biases[layer_name] -= learning_rate * gradients[f'b{i}']
        
        # Track gradients
        self.gradient_tracker.update_gradients(gradients, 
                                             [f"W{i}" for i in range(1, self.n_layers + 1)])
        
        return gradients
    
    def compute_loss(self, Y_pred, Y_true):
        """Binary cross-entropy"""
        m = Y_true.shape[0]
        Y_pred = np.clip(Y_pred, 1e-10, 1 - 1e-10)
        loss = -np.mean(Y_true * np.log(Y_pred) + (1 - Y_true) * np.log(1 - Y_pred))
        return loss
    
    def train(self, X, Y, epochs=100, learning_rate=0.01, val_split=0.2):
        """Train with checkpoint management"""
        n_val = int(X.shape[0] * val_split)
        X_train, X_val = X[:-n_val], X[-n_val:]
        Y_train, Y_val = Y[:-n_val], Y[-n_val:]
        
        for epoch in range(epochs):
            # Forward
            Y_pred = self.forward(X_train, record_debug=(epoch == epochs - 1))
            train_loss = self.compute_loss(Y_pred, Y_train)
            
            # Backward
            self.backward(Y_train, learning_rate, record_debug=(epoch == epochs - 1))
            
            # Validation
            Y_val_pred = self.forward(X_val)
            val_loss = self.compute_loss(Y_val_pred, Y_val)
            
            # Metrics
            train_acc = np.mean((Y_pred > 0.5) == Y_train)
            val_acc = np.mean((Y_val_pred > 0.5) == Y_val)
            
            # Save checkpoint every N epochs
            if epoch % max(1, epochs // 20) == 0 or epoch == epochs - 1:
                self.checkpoint_manager.save_checkpoint(
                    epoch,
                    {'weights': self.weights, 'biases': self.biases},
                    {
                        'train_loss': train_loss,
                        'val_loss': val_loss,
                        'train_acc': train_acc,
                        'val_acc': val_acc,
                        'learning_rate': learning_rate
                    }
                )
        
        return {
            'train_loss': train_loss,
            'val_loss': val_loss,
            'train_acc': train_acc,
            'val_acc': val_acc
        }


# ============================================================================
# UI PAGE
# ============================================================================

def ml_experimentation_hub():
    """Main ML Experimentation Hub page"""
    
    st.set_page_config(layout="wide")
    
    st.markdown("# 🧪 ML Experimentation Hub - Phase 1")
    st.markdown("### Next-Generation Neural Network Visualization & Analysis Platform")
    
    # Sidebar controls
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        exp_mode = st.radio("Select Feature Module", [
            "🎬 Training Replay",
            "📊 Gradient Flow Analysis",
            "🗻 Loss Landscape",
            "🔍 Model Debugger",
            "📈 Learning Rate Analysis",
        ])
    
    # Initialize session state
    if 'nn_model' not in st.session_state:
        st.session_state.nn_model = None
    if 'training_data' not in st.session_state:
        st.session_state.training_data = None
    
    # Generate/load dataset
    st.markdown("### 📊 Dataset Configuration")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        n_samples = st.slider("Samples", 50, 500, 200)
    with col2:
        noise = st.slider("Noise", 0.0, 0.8, 0.1)
    with col3:
        seed = st.number_input("Seed", 0, 1000, 42)
    
    np.random.seed(seed)
    X = np.random.randn(n_samples, 2)
    Y = (np.sum(X**2, axis=1) > 2).astype(float).reshape(-1, 1)
    if noise > 0:
        noise_mask = np.random.rand(len(Y)) < noise
        Y[noise_mask] = 1 - Y[noise_mask]
    
    # Model configuration
    st.markdown("### 🧠 Model Configuration")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        hidden_units = st.selectbox("Hidden Layer Size", [8, 16, 32, 64])
    with col2:
        learning_rate = st.select_slider("Learning Rate", 
                                        [0.001, 0.01, 0.05, 0.1, 0.5])
    with col3:
        epochs = st.slider("Epochs", 10, 200, 50)
    
    # Train model
    if st.button("🚀 Train Model with Debug Info", key="train_btn"):
        with st.spinner("Training model with instrumentation..."):
            model = NeuralNetworkDebugger(2, [hidden_units], 1)
            train_result = model.train(X, Y, epochs=epochs, learning_rate=learning_rate)
            st.session_state.nn_model = model
            st.session_state.training_data = (X, Y)
            st.success(f"✅ Training complete!\nFinal Accuracy: {train_result['val_acc']:.2%}")
    
    if st.session_state.nn_model is None:
        st.info("👈 Configure and train a model to begin analysis")
        return
    
    model = st.session_state.nn_model
    X, Y = st.session_state.training_data
    
    # ========== FEATURE 1: TRAINING REPLAY ==========
    if exp_mode == "🎬 Training Replay":
        st.markdown("## 🎬 Training Replay - Epoch-by-Epoch Visualization")
        st.markdown("Watch how the model learns over time with interactive playback controls.")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Loss curves
            fig_loss = plot_loss_curves_with_epoch_marker(model.checkpoint_manager)
            st.plotly_chart(fig_loss, use_container_width=True)
        
        with col2:
            st.markdown("### 📈 Training Summary")
            frames = model.checkpoint_manager.get_all_frames()
            if frames:
                final_frame = frames[-1]
                st.metric("Final Epoch", final_frame.epoch)
                st.metric("Train Loss", f"{final_frame.train_loss:.4f}")
                st.metric("Val Accuracy", f"{final_frame.val_acc:.2%}")
    
    # ========== FEATURE 2: GRADIENT FLOW ANALYSIS ==========
    elif exp_mode == "📊 Gradient Flow Analysis":
        st.markdown("## 📊 Gradient Flow Analysis - Debugging Gradient Propagation")
        st.markdown("Detect vanishing/exploding gradients and monitor gradient health.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_mag = plot_gradient_magnitudes(model.gradient_tracker)
            if fig_mag:
                st.plotly_chart(fig_mag, use_container_width=True)
        
        with col2:
            fig_heatmap = plot_gradient_health_heatmap(model.gradient_tracker)
            if fig_heatmap:
                st.plotly_chart(fig_heatmap, use_container_width=True)
        
        # Gradient health summary
        st.markdown("### 🔍 Gradient Health Status")
        health = gradient_health_summary(model.gradient_tracker)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Healthy Layers", len(health['healthy']))
        with col2:
            st.metric("Vanishing Gradients", len(health['vanishing']))
        with col3:
            st.metric("Exploding Gradients", len(health['exploding']))
        
        if health['vanishing']:
            st.warning(f"⚠️ Vanishing gradients detected in: {', '.join(health['vanishing'])}")
        if health['exploding']:
            st.warning(f"⚠️ Exploding gradients detected in: {', '.join(health['exploding'])}")
        
        fig_timeline = plot_gradient_flow_timeline(model.gradient_tracker)
        if fig_timeline:
            st.plotly_chart(fig_timeline, use_container_width=True)
    
    # ========== FEATURE 3: LOSS LANDSCAPE ==========
    elif exp_mode == "🗻 Loss Landscape":
        st.markdown("## 🗻 3D Loss Landscape - Weight Space Visualization")
        st.markdown("Explore the loss surface around trained weights to understand optimization geometry.")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.info("🌐 Loss Landscape is computed by perturbing learned weights in two random directions.")
            
            # Simplified landscape computation
            w_flat = model.weights['W1'].flatten()
            with st.spinner("Computing loss landscape..."):
                w1_grid, w2_grid, loss_grid = generate_loss_landscape(
                    lambda w: model.forward(X),  # Simplified
                    X, Y, w_flat, loss_range=0.3, resolution=30
                )
            
            fig_3d = plot_3d_loss_landscape(w1_grid, w2_grid, loss_grid)
            st.plotly_chart(fig_3d, use_container_width=True)
        
        with col1:
            fig_contour = plot_loss_landscape_contour(w1_grid, w2_grid, loss_grid)
            st.plotly_chart(fig_contour, use_container_width=True)
        
        with col2:
            st.markdown("### 📊 Landscape Analysis")
            analysis = analyze_loss_landscape(loss_grid)
            st.metric("Min Loss", f"{analysis.get('min_loss', 0):.4f}")
            st.metric("Max Loss", f"{analysis.get('max_loss', 0):.4f}")
            st.metric("Smoothness", f"{analysis.get('landscape_smoothness', 0):.4f}")
    
    # ========== FEATURE 4: MODEL DEBUGGER ==========
    elif exp_mode == "🔍 Model Debugger":
        st.markdown("## 🔍 Model Debugger - Forward/Backward Pass Inspection")
        st.markdown("Step through the network and inspect neuron values and gradients.")
        
        # Run forward/backward for debugging
        Y_pred_debug = model.forward(X, record_debug=True)
        model.backward(Y, learning_rate=0.01, record_debug=True)
        
        # Layer selector
        layer_names = [f"W{i+1}" for i in range(model.n_layers)]
        selected_layer = st.selectbox("Select Layer", layer_names)
        
        col1, col2 = st.columns(2)
        
        with col1:
            act_data = model.debugger.get_layer_activations(selected_layer)
            if 'output' in act_data:
                fig_act = plot_neuron_activations(selected_layer, act_data['output'][0])
                st.plotly_chart(fig_act, use_container_width=True)
        
        with col2:
            grad_data = model.debugger.get_layer_gradients(selected_layer)
            if 'weight_grad' in grad_data:
                fig_grad = plot_neuron_gradients(selected_layer, grad_data['weight_grad'])
                st.plotly_chart(fig_grad, use_container_width=True)
    
    # ========== FEATURE 5: LEARNING RATE ANALYSIS ==========
    elif exp_mode == "📈 Learning Rate Analysis":
        st.markdown("## 📈 Learning Rate Comparison - Convergence Analysis")
        st.markdown("Train multiple learning rates in parallel and compare convergence behavior.")
        
        lrs_to_compare = st.multiselect(
            "Learning Rates to Compare",
            [0.001, 0.01, 0.05, 0.1, 0.5],
            default=[0.01, 0.1]
        )
        
        if st.button("🔄 Train Multiple Learning Rates"):
            progress_bar = st.progress(0)
            lr_histories = {}
            
            for idx, lr in enumerate(lrs_to_compare):
                with st.spinner(f"Training with LR = {lr}..."):
                    model_temp = NeuralNetworkDebugger(2, [hidden_units], 1)
                    model_temp.train(X, Y, epochs=epochs, learning_rate=lr)
                    frames = model_temp.checkpoint_manager.get_all_frames()
                    train_losses = [f.train_loss for f in frames]
                    lr_histories[lr] = {
                        'train_loss': train_losses,
                        'epochs': np.arange(len(train_losses))
                    }
                progress_bar.progress((idx + 1) / len(lrs_to_compare))
            
            st.session_state.lr_histories = lr_histories
        
        if 'lr_histories' in st.session_state:
            lr_histories = st.session_state.lr_histories
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig_comparison = plot_learning_rate_comparison(lr_histories)
                st.plotly_chart(fig_comparison, use_container_width=True)
            
            with col2:
                fig_acceleration = plot_learning_curve_acceleration(lr_histories)
                st.plotly_chart(fig_acceleration, use_container_width=True)
            
            # Analysis
            st.markdown("### 🎯 Learning Rate Analysis")
            analysis = analyze_learning_rate_effects(lr_histories)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Optimal LR", f"{analysis['optimal_lr']}")
            with col2:
                st.metric("Best Final Loss", f"{analysis['best_final_loss']:.4f}")
            with col3:
                st.metric("Most Stable LR", f"{analysis['most_stable']}")


if __name__ == "__main__":
    ml_experimentation_hub()
