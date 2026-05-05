"""
Glowing Glass Buttons Showcase
Demonstrates all colorful glowing button styles with glass finish
"""

import streamlit as st
from utils.styles import (
    inject_global_css, gradient_header, section_header,
    glowing_button, glow_button_group,
    btn_indigo, btn_cyan, btn_emerald, btn_rose, btn_gold, btn_purple, btn_pink, btn_blue,
    btn_rainbow, btn_neon_pulse
)

inject_global_css()

gradient_header(
    "Glowing Buttons Showcase",
    "Colorful Glass Finish Buttons with Neon Effects",
    "✨",
    img_path="https://images.unsplash.com/photo-1614730321146-b6fa6a46bcb4?auto=format&fit=crop&q=90&w=1200"
)

st.markdown("""
This page demonstrates all available glowing button variants with glass morphism finish 
and neon glow effects. Use these buttons throughout your project for a modern, 
premium look with interactive animations.
""")

st.divider()

# ═════════════════════════════════════════════════════════════════════════════
# PRESET COLOR BUTTONS
# ═════════════════════════════════════════════════════════════════════════════
section_header("Preset Colored Buttons", "Single Color Variations")

col1, col2, col3, col4 = st.columns(4)

with col1:
    btn_indigo("Indigo Button", "🎨")
with col2:
    btn_cyan("Cyan Button", "💎")
with col3:
    btn_emerald("Emerald Button", "🌿")
with col4:
    btn_rose("Rose Button", "🌹")

st.markdown("")

col1, col2, col3, col4 = st.columns(4)

with col1:
    btn_gold("Gold Button", "⭐")
with col2:
    btn_purple("Purple Button", "🎭")
with col3:
    btn_pink("Pink Button", "💕")
with col4:
    btn_blue("Blue Button", "🌊")

st.divider()

# ═════════════════════════════════════════════════════════════════════════════
# BUTTON SIZES
# ═════════════════════════════════════════════════════════════════════════════
section_header("Button Sizes", "Small, Medium, and Large Variants")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Small Button**")
    glowing_button("Small", "🚀", "#818CF8", "#6366F1", size="small", key="btn_small")

with col2:
    st.markdown("**Medium Button**")
    glowing_button("Medium", "🎯", "#22D3EE", "#06B6D4", size="medium", key="btn_medium")

with col3:
    st.markdown("**Large Button**")
    glowing_button("Large", "💥", "#34D399", "#10B981", size="large", key="btn_large")

st.divider()

# ═════════════════════════════════════════════════════════════════════════════
# FULL WIDTH BUTTONS
# ═════════════════════════════════════════════════════════════════════════════
section_header("Full Width Buttons", "Spanning Entire Container")

st.markdown("**Cyan Full Width**")
glowing_button("Click Me - Full Width Button", "✨", "#22D3EE", "#06B6D4", use_container_width=True, key="btn_full_cyan")

st.markdown("")

st.markdown("**Rose Full Width**")
glowing_button("Action Button - Full Width", "⚡", "#FB7185", "#F43F5E", use_container_width=True, key="btn_full_rose")

st.divider()

# ═════════════════════════════════════════════════════════════════════════════
# BUTTON GROUPS
# ═════════════════════════════════════════════════════════════════════════════
section_header("Button Groups", "Multiple Buttons in Grid Layout")

buttons_grid = [
    {"label": "Explore", "icon": "🔍", "color": "#818CF8", "glow_color": "#6366F1", "key": "btn_explore"},
    {"label": "Analyze", "icon": "📊", "color": "#22D3EE", "glow_color": "#06B6D4", "key": "btn_analyze"},
    {"label": "Deploy", "icon": "🚀", "color": "#34D399", "glow_color": "#10B981", "key": "btn_deploy"},
    {"label": "Optimize", "icon": "⚡", "color": "#FB7185", "glow_color": "#F43F5E", "key": "btn_optimize"},
    {"label": "Monitor", "icon": "📡", "color": "#F59E0B", "glow_color": "#D97706", "key": "btn_monitor"},
    {"label": "Report", "icon": "📝", "color": "#A855F7", "glow_color": "#7C3AED", "key": "btn_report"},
]

glow_button_group(buttons_grid, columns=3, spacing="medium")

st.divider()

# ═════════════════════════════════════════════════════════════════════════════
# SPECIAL EFFECTS
# ═════════════════════════════════════════════════════════════════════════════
section_header("Special Effects", "Advanced Button Animations")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Rainbow Gradient**")
    btn_rainbow("Rainbow Button", "🌈")

with col2:
    st.markdown("**Neon Pulse**")
    btn_neon_pulse("Neon Pulse", "💫", "#22D3EE")

with col3:
    st.markdown("**Without Animation**")
    glowing_button("Static Glow", "🔲", "#FB7185", "#F43F5E", animated=False, key="btn_static")

st.divider()

# ═════════════════════════════════════════════════════════════════════════════
# USAGE EXAMPLES
# ═════════════════════════════════════════════════════════════════════════════
section_header("Code Examples", "How to Use in Your Project")

st.markdown("### Basic Usage")
st.code("""
from utils.styles import glowing_button

glowing_button(
    label="Click Me",
    icon="🚀",
    color="#818CF8",
    glow_color="#6366F1",
    use_container_width=True
)
""", language="python")

st.markdown("### Preset Colors")
st.code("""
from utils.styles import btn_cyan, btn_emerald, btn_rose

col1, col2, col3 = st.columns(3)
with col1:
    btn_cyan("Cyan Button", "💎")
with col2:
    btn_emerald("Emerald Button", "🌿")
with col3:
    btn_rose("Rose Button", "🌹")
""", language="python")

st.markdown("### Button Groups")
st.code("""
from utils.styles import glow_button_group

buttons = [
    {"label": "Save", "icon": "💾", "color": "#818CF8", "glow_color": "#6366F1"},
    {"label": "Delete", "icon": "🗑️", "color": "#FB7185", "glow_color": "#F43F5E"},
    {"label": "Export", "icon": "📤", "color": "#22D3EE", "glow_color": "#06B6D4"},
]

glow_button_group(buttons, columns=3)
""", language="python")

st.markdown("### Special Effects")
st.code("""
from utils.styles import btn_rainbow, btn_neon_pulse

btn_rainbow("Rainbow", "🌈")
btn_neon_pulse("Pulse", "💫", "#22D3EE")
""", language="python")

st.divider()

# ═════════════════════════════════════════════════════════════════════════════
# COLOR PALETTE
# ═════════════════════════════════════════════════════════════════════════════
section_header("Color Palette Reference", "Available Glow Colors")

colors_info = {
    "🎨 Indigo": {"primary": "#818CF8", "glow": "#6366F1"},
    "💎 Cyan": {"primary": "#22D3EE", "glow": "#06B6D4"},
    "🌿 Emerald": {"primary": "#34D399", "glow": "#10B981"},
    "🌹 Rose": {"primary": "#FB7185", "glow": "#F43F5E"},
    "⭐ Gold": {"primary": "#F59E0B", "glow": "#D97706"},
    "🎭 Purple": {"primary": "#A855F7", "glow": "#7C3AED"},
    "💕 Pink": {"primary": "#EC4899", "glow": "#DB2777"},
    "🌊 Blue": {"primary": "#3B82F6", "glow": "#1D4ED8"},
}

col1, col2, col3, col4 = st.columns(4)
for idx, (name, colors) in enumerate(colors_info.items()):
    with [col1, col2, col3, col4][idx % 4]:
        st.markdown(f"""
        <div style="background: rgba({colors['primary'][:7]}, 0.2); padding: 15px; border-radius: 12px; border: 1px solid {colors['primary']}; margin-bottom: 10px;">
            <div style="font-weight: 800; color: {colors['primary']};">{name}</div>
            <div style="font-size: 12px; color: #94A3B8; font-family: monospace; margin-top: 5px;">
                {colors['primary']}<br>
                {colors['glow']}
            </div>
        </div>
        """, unsafe_allow_html=True)

st.divider()

st.markdown("""
### 🎨 Features

✨ **Glass Morphism** - Frosted glass effect with backdrop blur  
🌟 **Neon Glow** - Animated glowing effects synchronized with movement  
🎭 **Multiple Sizes** - Small, medium, large button variants  
🌈 **Rainbow Animations** - Gradient shifting effects  
💫 **Pulse Effects** - Heartbeat and breathing animations  
⚡ **Interactive** - Smooth hover and click animations  
📱 **Responsive** - Works on all screen sizes  
🔧 **Customizable** - Easy to adjust colors and effects

---

*Created for Aura AI Studio - Premium Neural Network Visualization Platform*
""")
