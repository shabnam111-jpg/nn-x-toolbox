"""
Quick Test - Glowing Buttons
Run this to see the buttons in action
"""

import streamlit as st
from utils.styles import inject_global_css, gradient_header, section_header
from utils.styles import btn_cyan, btn_emerald, btn_rose, btn_gold, btn_rainbow, glowing_button

# Initialize styling
inject_global_css()

# Header
gradient_header(
    "Glowing Buttons - Quick Test",
    "Try the colorful glass buttons",
    "✨"
)

st.markdown("### 🌟 Test These Glowing Buttons\n")

# Test 1: Preset Colors
section_header("1. Preset Color Buttons", "Eight Beautiful Colors")
col1, col2, col3, col4 = st.columns(4)

with col1:
    btn_cyan("Cyan", "💎")
with col2:
    btn_emerald("Emerald", "🌿")
with col3:
    btn_rose("Rose", "🌹")
with col4:
    btn_gold("Gold", "⭐")

st.markdown("")

# Test 2: Full Width
section_header("2. Full Width Buttons", "Spanning Entire Width")
btn_cyan("Click Me - Full Width", "✨", use_container_width=True, key="full_width")

st.markdown("")

# Test 3: Custom Colors
section_header("3. Custom Color Button", "With Full Customization")
glowing_button(
    "Custom Neon",
    "🔮",
    color="#EC4899",
    glow_color="#BE185D",
    use_container_width=True,
    key="custom"
)

st.markdown("")

# Test 4: Special Effects
section_header("4. Special Effects", "Rainbow & Neon Pulse")
col1, col2 = st.columns(2)

with col1:
    btn_rainbow("Rainbow 🌈")
with col2:
    from utils.styles import btn_neon_pulse
    btn_neon_pulse("Neon Pulse 💫", color="#22D3EE")

st.markdown("")

# Code Examples
section_header("5. How to Use", "Copy & Paste Examples")

st.markdown("**Simple Button:**")
st.code("""
from utils.styles import btn_cyan
btn_cyan("Click Me", "🚀")
""")

st.markdown("**Full Width Button:**")
st.code("""
btn_cyan("Action", "⚡", use_container_width=True)
""")

st.markdown("**Custom Colors:**")
st.code("""
from utils.styles import glowing_button

glowing_button(
    "My Button",
    "🎨",
    color="#EC4899",
    glow_color="#BE185D",
    use_container_width=True
)
""")

st.markdown("**Button Group:**")
st.code("""
from utils.styles import glow_button_group

buttons = [
    {"label": "Save", "icon": "💾", "color": "#818CF8"},
    {"label": "Delete", "icon": "🗑️", "color": "#FB7185"},
    {"label": "Export", "icon": "📤", "color": "#22D3EE"},
]
glow_button_group(buttons, columns=3)
""")

st.divider()

st.markdown("""
✨ **All glowing buttons are now available in your project!**

📁 **New Files:**
- Updated `utils/styles.py` - Added 8+ button functions
- `glowing_buttons_demo.py` - Complete showcase
- `GLOWING_BUTTONS_GUIDE.md` - Detailed guide

🎯 **Available Functions:**
- `glowing_button()` - Main customizable button
- `btn_indigo()`, `btn_cyan()`, `btn_emerald()`, `btn_rose()`, `btn_gold()`, `btn_purple()`, `btn_pink()`, `btn_blue()` - Preset colors
- `btn_rainbow()` - Rainbow effect
- `btn_neon_pulse()` - Neon pulse effect
- `glow_button_group()` - Button groups

🚀 **Next Steps:**
1. Run: `streamlit run glowing_buttons_demo.py` - See all styles
2. Read: `GLOWING_BUTTONS_GUIDE.md` - Full documentation
3. Use: Import and use in your pages
""")
