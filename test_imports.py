"""
Import Verification Script - Tests all critical imports
"""

import sys
sys.path.insert(0, '.')

print("Testing imports...")

# Test utils imports
try:
    from utils.nn_helpers import PLOTLY_BASE, plotly_layout, hex2rgba, draw_network
    from utils.styles import (
        inject_global_css, gradient_header, section_header, stat_card,
        render_theory_card, render_log, glowing_button
    )
    print("✓ utils imports OK")
except ImportError as e:
    print(f"✗ utils imports FAILED: {e}")
    sys.exit(1)

# Test core modules
try:
    from Perceptron.perceptron_ui import perceptron_page
    print("✓ Perceptron import OK")
except ImportError as e:
    print(f"✗ Perceptron import FAILED: {e}")
    sys.exit(1)

try:
    from Forward_Propagation.forward_propagation import forward_propagation_page
    print("✓ Forward Propagation import OK")
except ImportError as e:
    print(f"✗ Forward Propagation import FAILED: {e}")
    sys.exit(1)

try:
    from Backward_Propagation.backward_propagation import backward_propagation_page
    print("✓ Backward Propagation import OK")
except ImportError as e:
    print(f"✗ Backward Propagation import FAILED: {e}")
    sys.exit(1)

try:
    from Gradient_Descent.gradient_descent_ui import gradient_descent_page
    print("✓ Gradient Descent import OK")
except ImportError as e:
    print(f"✗ Gradient Descent import FAILED: {e}")
    sys.exit(1)

# Test AI modules
try:
    from Aura_AI.chatbot_ui import chatbot_ui
    print("✓ Chatbot UI import OK")
except ImportError as e:
    print(f"✗ Chatbot UI import FAILED: {e}")
    sys.exit(1)

try:
    from Aura_AI.playfield_ui import playfield_ui
    print("✓ Playfield UI import OK")
except ImportError as e:
    print(f"✗ Playfield UI import FAILED: {e}")
    sys.exit(1)

try:
    from Aura_AI.ai_assistant_ui import ai_assistant_page
    print("✓ AI Assistant UI import OK")
except ImportError as e:
    print(f"✗ AI Assistant UI import FAILED: {e}")
    sys.exit(1)

# Test app imports
try:
    from utils.ai_sidebar import render_global_ai_hub
    print("✓ AI Sidebar import OK")
except ImportError as e:
    print(f"✗ AI Sidebar import FAILED: {e}")
    sys.exit(1)

print("\n" + "="*50)
print("✓ ALL IMPORTS SUCCESSFUL!")
print("="*50)
