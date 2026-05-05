"""
Model Checkpoint Manager
Saves and loads neural network weights, activations, and gradients at each epoch.
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Any


@dataclass
class CheckpointFrame:
    """Single epoch snapshot"""
    epoch: int
    weights: Dict[str, np.ndarray]
    biases: Dict[str, np.ndarray]
    activations: Dict[str, np.ndarray] = field(default_factory=dict)  # Hidden layer activations
    gradients: Dict[str, np.ndarray] = field(default_factory=dict)    # Weight gradients
    train_loss: float = 0.0
    val_loss: float = 0.0
    train_acc: float = 0.0
    val_acc: float = 0.0
    learning_rate: float = 0.01


class CheckpointManager:
    """Manages training checkpoints for replay and analysis"""
    
    def __init__(self):
        self.frames: List[CheckpointFrame] = []
        self.metadata: Dict[str, Any] = {}
    
    def save_checkpoint(self, epoch: int, model_dict: Dict, metrics: Dict, 
                       activations: Dict = None, gradients: Dict = None):
        """Save a checkpoint at given epoch"""
        
        frame = CheckpointFrame(
            epoch=epoch,
            weights=model_dict.get('weights', {}),
            biases=model_dict.get('biases', {}),
            activations=activations or {},
            gradients=gradients or {},
            train_loss=metrics.get('train_loss', 0.0),
            val_loss=metrics.get('val_loss', 0.0),
            train_acc=metrics.get('train_acc', 0.0),
            val_acc=metrics.get('val_acc', 0.0),
            learning_rate=metrics.get('learning_rate', 0.01)
        )
        self.frames.append(frame)
    
    def get_frame(self, epoch_idx: int) -> CheckpointFrame:
        """Get checkpoint at specific epoch index"""
        if 0 <= epoch_idx < len(self.frames):
            return self.frames[epoch_idx]
        return None
    
    def get_all_frames(self) -> List[CheckpointFrame]:
        """Get all checkpoints"""
        return self.frames
    
    def get_weight_evolution(self, layer_name: str) -> np.ndarray:
        """Get weight values across all epochs for a specific layer"""
        weights = []
        for frame in self.frames:
            if layer_name in frame.weights:
                weights.append(frame.weights[layer_name].flatten())
        return np.array(weights) if weights else None
    
    def get_gradient_evolution(self, layer_name: str) -> np.ndarray:
        """Get gradient magnitudes across epochs for a specific layer"""
        grads = []
        for frame in self.frames:
            if layer_name in frame.gradients:
                grad_mag = np.linalg.norm(frame.gradients[layer_name])
                grads.append(grad_mag)
        return np.array(grads) if grads else None
    
    def get_loss_history(self) -> tuple:
        """Get train/val loss history"""
        train_loss = [f.train_loss for f in self.frames]
        val_loss = [f.val_loss for f in self.frames]
        return np.array(train_loss), np.array(val_loss)
    
    def get_accuracy_history(self) -> tuple:
        """Get train/val accuracy history"""
        train_acc = [f.train_acc for f in self.frames]
        val_acc = [f.val_acc for f in self.frames]
        return np.array(train_acc), np.array(val_acc)
    
    def get_layer_names(self) -> List[str]:
        """Get all layer names from first checkpoint"""
        if self.frames:
            return list(self.frames[0].weights.keys())
        return []
    
    def clear(self):
        """Clear all checkpoints"""
        self.frames.clear()
        self.metadata.clear()
