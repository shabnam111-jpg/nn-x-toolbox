"""
Gradient Flow Analyzer
Tracks and visualizes gradients through layers for debugging training.
"""

import numpy as np
from typing import Dict, List, Tuple


class GradientTracker:
    """Tracks gradient flow through network layers"""
    
    def __init__(self):
        self.layer_stats = {}  # layer_name -> {grad_mag, grad_std, grad_min, grad_max}
        self.gradient_history = {}  # layer_name -> list of gradient magnitudes
    
    def update_gradients(self, gradients: Dict[str, np.ndarray], layer_names: List[str]):
        """
        Update gradient statistics
        
        Args:
            gradients: Dict of layer_name -> gradient_array
            layer_names: List of layer names in order
        """
        for layer_name in layer_names:
            if layer_name not in self.layer_stats:
                self.layer_stats[layer_name] = []
                self.gradient_history[layer_name] = []
            
            if layer_name in gradients:
                grad = gradients[layer_name]
                grad_magnitude = np.linalg.norm(grad)
                grad_std = np.std(grad)
                grad_min = np.min(np.abs(grad))
                grad_max = np.max(np.abs(grad))
                
                stats = {
                    'magnitude': grad_magnitude,
                    'std': grad_std,
                    'min': grad_min,
                    'max': grad_max,
                    'n_elements': grad.size,
                    'ratio': grad_magnitude / (grad.size ** 0.5) if grad.size > 0 else 0
                }
                
                self.layer_stats[layer_name].append(stats)
                self.gradient_history[layer_name].append(grad_magnitude)
    
    def get_gradient_stats(self, layer_name: str) -> Dict:
        """Get current gradient statistics for a layer"""
        if layer_name in self.layer_stats and self.layer_stats[layer_name]:
            return self.layer_stats[layer_name][-1]
        return {}
    
    def get_gradient_history(self, layer_name: str) -> np.ndarray:
        """Get gradient magnitude history for a layer"""
        if layer_name in self.gradient_history:
            return np.array(self.gradient_history[layer_name])
        return np.array([])
    
    def detect_vanishing_gradients(self, layer_name: str, threshold: float = 1e-5) -> bool:
        """Detect if gradients are vanishing for a layer"""
        history = self.get_gradient_history(layer_name)
        if len(history) > 10:
            recent_grads = history[-10:]
            return np.all(recent_grads < threshold)
        return False
    
    def detect_exploding_gradients(self, layer_name: str, threshold: float = 10.0) -> bool:
        """Detect if gradients are exploding for a layer"""
        history = self.get_gradient_history(layer_name)
        if len(history) > 10:
            recent_grads = history[-10:]
            return np.any(recent_grads > threshold)
        return False
    
    def get_all_layer_magnitudes(self) -> Dict[str, float]:
        """Get current gradient magnitude for all layers"""
        magnitudes = {}
        for layer_name in self.layer_stats:
            if self.layer_stats[layer_name]:
                magnitudes[layer_name] = self.layer_stats[layer_name][-1]['magnitude']
        return magnitudes
    
    def get_gradient_flow_ratio(self) -> List[Tuple[str, float]]:
        """Get gradient ratio (magnitude / sqrt(n_params)) for all layers"""
        ratios = []
        for layer_name in self.layer_stats:
            if self.layer_stats[layer_name]:
                ratio = self.layer_stats[layer_name][-1]['ratio']
                ratios.append((layer_name, ratio))
        return ratios
    
    def clear(self):
        """Clear all gradient history"""
        self.layer_stats.clear()
        self.gradient_history.clear()
